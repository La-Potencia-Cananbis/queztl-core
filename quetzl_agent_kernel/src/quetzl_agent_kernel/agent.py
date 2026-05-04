from __future__ import annotations

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Iterable

from .models import Capability, EventRecord, EventType
from .store import KernelStore


class KernelAgent(ABC):
    """Bounded worker for one or more capabilities."""

    def __init__(
        self,
        name: str,
        capabilities: Iterable[Capability | str],
        store: KernelStore,
        max_concurrency: int = 1,
        poll_interval: float = 0.25,
    ):
        self.name = name
        self.capabilities = [
            c if isinstance(c, Capability) else Capability(name=c)
            for c in capabilities
        ]
        self.store = store
        self.max_concurrency = max(1, max_concurrency)
        self.poll_interval = poll_interval
        self.logger = logging.getLogger(f"quetzl.agent.{name}")
        self._running = False
        self._workers: list[asyncio.Task] = []

    @property
    def capability_names(self) -> set[str]:
        return {cap.name for cap in self.capabilities}

    async def start(self) -> None:
        self._running = True
        self.store.append_event(EventRecord(
            type=EventType.AGENT_REGISTERED,
            agent_name=self.name,
            payload={"capabilities": sorted(self.capability_names)},
        ))
        self._workers = [asyncio.create_task(self._worker_loop(i)) for i in range(self.max_concurrency)]
        self.logger.info("started with %s workers", self.max_concurrency)

    async def stop(self) -> None:
        self._running = False
        for worker in self._workers:
            worker.cancel()
        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers = []
        self.logger.info("stopped")

    async def _worker_loop(self, worker_id: int) -> None:
        while self._running:
            packet = self.store.claim_next_packet(self.capability_names, self.name)
            if packet is None:
                await asyncio.sleep(self.poll_interval)
                continue

            try:
                result = await self.handle(packet.type, packet.payload, packet.metadata)
                self.store.mark_completed(packet, result)
            except asyncio.CancelledError:
                self.store.mark_failed(packet, "worker cancelled")
                raise
            except Exception as exc:  # noqa: BLE001 - agent boundary must catch and record failures
                self.logger.exception("packet %s failed", packet.id)
                self.store.mark_failed(packet, str(exc))

    @abstractmethod
    async def handle(self, packet_type: str, payload: dict[str, Any], metadata: dict[str, Any]) -> Any:
        """Execute a claimed packet and return a JSON-serializable result."""
        raise NotImplementedError


class EchoAgent(KernelAgent):
    """Small built-in demo agent."""

    def __init__(self, store: KernelStore):
        super().__init__("echo", ["echo.say"], store, max_concurrency=2)

    async def handle(self, packet_type: str, payload: dict[str, Any], metadata: dict[str, Any]) -> Any:
        await asyncio.sleep(float(payload.get("delay", 0)))
        return {"echo": payload.get("text", ""), "metadata": metadata}
