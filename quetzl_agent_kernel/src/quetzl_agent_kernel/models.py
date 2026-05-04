from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class PacketStatus(str, Enum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class EventType(str, Enum):
    PACKET_CREATED = "packet.created"
    PACKET_QUEUED = "packet.queued"
    PACKET_STARTED = "packet.started"
    PACKET_COMPLETED = "packet.completed"
    PACKET_FAILED = "packet.failed"
    PACKET_CANCELLED = "packet.cancelled"
    AGENT_REGISTERED = "agent.registered"
    AGENT_HEARTBEAT = "agent.heartbeat"
    GRAPH_STARTED = "graph.started"
    GRAPH_COMPLETED = "graph.completed"
    GRAPH_FAILED = "graph.failed"


class Capability(BaseModel):
    name: str = Field(..., examples=["echo.say", "model.predict", "render.video"])
    description: str = ""
    schema_name: Optional[str] = None


class ActionPacket(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    status: PacketStatus = PacketStatus.PENDING
    priority: int = 100
    idempotency_key: Optional[str] = None
    parent_id: Optional[str] = None
    graph_id: Optional[str] = None
    trace_id: str = Field(default_factory=lambda: str(uuid4()))
    assigned_agent: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    attempts: int = 0
    max_attempts: int = 1
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    deadline_at: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EventRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: EventType | str
    packet_id: Optional[str] = None
    agent_name: Optional[str] = None
    graph_id: Optional[str] = None
    trace_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)


class GraphNode(BaseModel):
    id: str
    packet_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    depends_on: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GraphSpec(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    nodes: List[GraphNode]
    metadata: Dict[str, Any] = Field(default_factory=dict)
