from __future__ import annotations

import asyncio
from typing import Dict, Iterable, Optional

from .agent import KernelAgent
from .models import ActionPacket, EventRecord, EventType, GraphSpec, PacketStatus
from .store import KernelStore


class KernelScheduler:
    """Routes action packets and evaluates simple DAG workflows."""

    def __init__(self, store: KernelStore):
        self.store = store
        self.agents: dict[str, KernelAgent] = {}

    def register_agent(self, agent: KernelAgent) -> None:
        self.agents[agent.name] = agent

    async def start_agents(self) -> None:
        await asyncio.gather(*(agent.start() for agent in self.agents.values()))

    async def stop_agents(self) -> None:
        await asyncio.gather(*(agent.stop() for agent in self.agents.values()), return_exceptions=True)

    def capabilities(self) -> dict[str, list[str]]:
        return {name: sorted(agent.capability_names) for name, agent in self.agents.items()}

    def submit_packet(self, packet: ActionPacket) -> ActionPacket:
        return self.store.put_packet(packet)

    def submit(self, packet_type: str, payload: dict, **kwargs) -> ActionPacket:
        return self.submit_packet(ActionPacket(type=packet_type, payload=payload, **kwargs))

    async def wait_for_packet(self, packet_id: str, timeout: float = 30.0) -> ActionPacket:
        deadline = asyncio.get_running_loop().time() + timeout
        while asyncio.get_running_loop().time() < deadline:
            packet = self.store.get_packet(packet_id)
            if packet and packet.status in {PacketStatus.COMPLETED, PacketStatus.FAILED, PacketStatus.CANCELLED}:
                return packet
            await asyncio.sleep(0.1)
        packet = self.store.get_packet(packet_id)
        if not packet:
            raise TimeoutError(f"packet {packet_id} not found")
        raise TimeoutError(f"packet {packet_id} timed out with status {packet.status}")

    async def run_graph(self, graph: GraphSpec, timeout_per_node: float = 60.0) -> dict:
        """Run a simple dependency DAG.

        Node outputs are injected into downstream node metadata under dependency_results.
        """
        self.store.append_event(EventRecord(
            type=EventType.GRAPH_STARTED,
            graph_id=graph.id,
            payload={"name": graph.name, "nodes": len(graph.nodes)},
        ))

        nodes_by_id = {node.id: node for node in graph.nodes}
        completed: dict[str, ActionPacket] = {}
        pending = set(nodes_by_id.keys())

        try:
            while pending:
                ready = [
                    node_id for node_id in pending
                    if all(dep in completed for dep in nodes_by_id[node_id].depends_on)
                ]
                if not ready:
                    raise ValueError(f"graph has unresolved cycle or missing dependency: {sorted(pending)}")

                running: list[tuple[str, ActionPacket]] = []
                for node_id in ready:
                    node = nodes_by_id[node_id]
                    dependency_results = {
                        dep: completed[dep].result for dep in node.depends_on
                    }
                    packet = ActionPacket(
                        type=node.packet_type,
                        payload=node.payload,
                        graph_id=graph.id,
                        parent_id=None,
                        metadata={**node.metadata, "node_id": node.id, "dependency_results": dependency_results},
                    )
                    self.store.put_packet(packet)
                    running.append((node_id, packet))

                results = await asyncio.gather(*[
                    self.wait_for_packet(packet.id, timeout=timeout_per_node)
                    for _, packet in running
                ])

                for (node_id, _), packet in zip(running, results):
                    if packet.status != PacketStatus.COMPLETED:
                        raise RuntimeError(f"node {node_id} failed: {packet.error}")
                    completed[node_id] = packet
                    pending.remove(node_id)

            output = {
                "graph_id": graph.id,
                "name": graph.name,
                "results": {node_id: packet.result for node_id, packet in completed.items()},
            }
            self.store.append_event(EventRecord(
                type=EventType.GRAPH_COMPLETED,
                graph_id=graph.id,
                payload=output,
            ))
            return output
        except Exception as exc:
            self.store.append_event(EventRecord(
                type=EventType.GRAPH_FAILED,
                graph_id=graph.id,
                payload={"error": str(exc)},
            ))
            raise
