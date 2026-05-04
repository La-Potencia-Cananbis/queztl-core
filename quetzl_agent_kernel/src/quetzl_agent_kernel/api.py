from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .agent import EchoAgent
from .models import ActionPacket, GraphSpec
from .scheduler import KernelScheduler
from .store import KernelStore

DB_PATH = str(Path(__file__).resolve().parents[3] / "quetzl_kernel.db")
store = KernelStore(DB_PATH)
scheduler = KernelScheduler(store)
scheduler.register_agent(EchoAgent(store))


class SubmitTaskRequest(BaseModel):
    type: str
    payload: dict[str, Any] = {}
    priority: int = 100
    idempotency_key: Optional[str] = None
    metadata: dict[str, Any] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    await scheduler.start_agents()
    try:
        yield
    finally:
        await scheduler.stop_agents()


app = FastAPI(
    title="Quetzl Agent Kernel V3",
    version="0.3.0",
    description="Graph-native durable agent kernel for Quetzl Core",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, Any]:
    return {
        "status": "healthy",
        "capabilities": scheduler.capabilities(),
    }


@app.post("/tasks")
async def submit_task(request: SubmitTaskRequest) -> dict[str, Any]:
    packet = scheduler.submit(
        request.type,
        request.payload,
        priority=request.priority,
        idempotency_key=request.idempotency_key,
        metadata=request.metadata,
    )
    return packet.model_dump(mode="json")


@app.get("/tasks/{packet_id}")
async def get_task(packet_id: str) -> dict[str, Any]:
    packet = store.get_packet(packet_id)
    if not packet:
        raise HTTPException(status_code=404, detail="packet not found")
    return packet.model_dump(mode="json")


@app.get("/tasks")
async def list_tasks(status: Optional[str] = None, limit: int = 100) -> list[dict[str, Any]]:
    return [packet.model_dump(mode="json") for packet in store.list_packets(status=status, limit=limit)]


@app.get("/events")
async def list_events(packet_id: Optional[str] = None, limit: int = 200) -> list[dict[str, Any]]:
    return [event.model_dump(mode="json") for event in store.list_events(packet_id=packet_id, limit=limit)]


@app.post("/graphs/run")
async def run_graph(graph: GraphSpec) -> dict[str, Any]:
    return await scheduler.run_graph(graph)
