from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

from .models import ActionPacket, EventRecord, EventType, PacketStatus, utc_now


class KernelStore:
    """SQLite-backed packet store and append-only event log."""

    def __init__(self, db_path: str = "quetzl_kernel.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True) if Path(db_path).parent != Path(".") else None
        self.init_db()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS packets (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    status TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    idempotency_key TEXT UNIQUE,
                    parent_id TEXT,
                    graph_id TEXT,
                    trace_id TEXT NOT NULL,
                    assigned_agent TEXT,
                    result_json TEXT,
                    error TEXT,
                    attempts INTEGER NOT NULL,
                    max_attempts INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    deadline_at TEXT,
                    tags_json TEXT NOT NULL,
                    metadata_json TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    packet_id TEXT,
                    agent_name TEXT,
                    graph_id TEXT,
                    trace_id TEXT,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_packets_status ON packets(status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_packets_type ON packets(type)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_events_packet ON events(packet_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_events_trace ON events(trace_id)")

    def put_packet(self, packet: ActionPacket) -> ActionPacket:
        existing = None
        if packet.idempotency_key:
            existing = self.get_by_idempotency_key(packet.idempotency_key)
        if existing:
            return existing

        packet.updated_at = utc_now()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO packets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                self._packet_to_row(packet),
            )
        self.append_event(EventRecord(
            type=EventType.PACKET_CREATED,
            packet_id=packet.id,
            graph_id=packet.graph_id,
            trace_id=packet.trace_id,
            payload={"type": packet.type},
        ))
        return packet

    def update_packet(self, packet: ActionPacket) -> ActionPacket:
        packet.updated_at = utc_now()
        with self.connect() as conn:
            conn.execute(
                """
                UPDATE packets SET
                  type=?, payload_json=?, status=?, priority=?, idempotency_key=?, parent_id=?,
                  graph_id=?, trace_id=?, assigned_agent=?, result_json=?, error=?, attempts=?,
                  max_attempts=?, created_at=?, updated_at=?, deadline_at=?, tags_json=?, metadata_json=?
                WHERE id=?
                """,
                self._packet_update_values(packet),
            )
        return packet

    def get_packet(self, packet_id: str) -> Optional[ActionPacket]:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM packets WHERE id = ?", (packet_id,)).fetchone()
        return self._row_to_packet(row) if row else None

    def get_by_idempotency_key(self, key: str) -> Optional[ActionPacket]:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM packets WHERE idempotency_key = ?", (key,)).fetchone()
        return self._row_to_packet(row) if row else None

    def list_packets(self, status: Optional[PacketStatus | str] = None, limit: int = 100) -> list[ActionPacket]:
        with self.connect() as conn:
            if status:
                rows = conn.execute(
                    "SELECT * FROM packets WHERE status = ? ORDER BY priority ASC, created_at ASC LIMIT ?",
                    (str(status.value if isinstance(status, PacketStatus) else status), limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM packets ORDER BY created_at DESC LIMIT ?",
                    (limit,),
                ).fetchall()
        return [self._row_to_packet(row) for row in rows]

    def claim_next_packet(self, capabilities: Iterable[str], agent_name: str) -> Optional[ActionPacket]:
        capability_list = list(capabilities)
        if not capability_list:
            return None

        placeholders = ",".join("?" for _ in capability_list)
        now = utc_now().isoformat()
        with self.connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                f"""
                SELECT * FROM packets
                WHERE status IN (?, ?) AND type IN ({placeholders})
                ORDER BY priority ASC, created_at ASC
                LIMIT 1
                """,
                [PacketStatus.PENDING.value, PacketStatus.QUEUED.value, *capability_list],
            ).fetchone()
            if not row:
                conn.commit()
                return None
            packet = self._row_to_packet(row)
            packet.status = PacketStatus.RUNNING
            packet.assigned_agent = agent_name
            packet.attempts += 1
            packet.updated_at = datetime.fromisoformat(now)
            conn.execute(
                "UPDATE packets SET status=?, assigned_agent=?, attempts=?, updated_at=? WHERE id=?",
                (packet.status.value, packet.assigned_agent, packet.attempts, now, packet.id),
            )
            conn.commit()

        self.append_event(EventRecord(
            type=EventType.PACKET_STARTED,
            packet_id=packet.id,
            agent_name=agent_name,
            graph_id=packet.graph_id,
            trace_id=packet.trace_id,
            payload={"attempts": packet.attempts},
        ))
        return packet

    def mark_completed(self, packet: ActionPacket, result: object) -> ActionPacket:
        packet.status = PacketStatus.COMPLETED
        packet.result = result
        packet.error = None
        self.update_packet(packet)
        self.append_event(EventRecord(
            type=EventType.PACKET_COMPLETED,
            packet_id=packet.id,
            agent_name=packet.assigned_agent,
            graph_id=packet.graph_id,
            trace_id=packet.trace_id,
            payload={"result": result},
        ))
        return packet

    def mark_failed(self, packet: ActionPacket, error: str) -> ActionPacket:
        packet.status = PacketStatus.FAILED
        packet.error = error
        self.update_packet(packet)
        self.append_event(EventRecord(
            type=EventType.PACKET_FAILED,
            packet_id=packet.id,
            agent_name=packet.assigned_agent,
            graph_id=packet.graph_id,
            trace_id=packet.trace_id,
            payload={"error": error},
        ))
        return packet

    def append_event(self, event: EventRecord) -> EventRecord:
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    event.id,
                    str(event.type.value if hasattr(event.type, "value") else event.type),
                    event.packet_id,
                    event.agent_name,
                    event.graph_id,
                    event.trace_id,
                    json.dumps(event.payload, default=str),
                    event.created_at.isoformat(),
                ),
            )
        return event

    def list_events(self, packet_id: Optional[str] = None, limit: int = 200) -> list[EventRecord]:
        with self.connect() as conn:
            if packet_id:
                rows = conn.execute(
                    "SELECT * FROM events WHERE packet_id = ? ORDER BY created_at ASC LIMIT ?",
                    (packet_id, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM events ORDER BY created_at DESC LIMIT ?",
                    (limit,),
                ).fetchall()
        return [self._row_to_event(row) for row in rows]

    def _packet_to_row(self, packet: ActionPacket) -> tuple:
        return (
            packet.id,
            packet.type,
            json.dumps(packet.payload, default=str),
            packet.status.value,
            packet.priority,
            packet.idempotency_key,
            packet.parent_id,
            packet.graph_id,
            packet.trace_id,
            packet.assigned_agent,
            json.dumps(packet.result, default=str) if packet.result is not None else None,
            packet.error,
            packet.attempts,
            packet.max_attempts,
            packet.created_at.isoformat(),
            packet.updated_at.isoformat(),
            packet.deadline_at.isoformat() if packet.deadline_at else None,
            json.dumps(packet.tags),
            json.dumps(packet.metadata, default=str),
        )

    def _packet_update_values(self, packet: ActionPacket) -> tuple:
        row = self._packet_to_row(packet)
        return row[1:] + (packet.id,)

    def _row_to_packet(self, row: sqlite3.Row) -> ActionPacket:
        return ActionPacket(
            id=row["id"],
            type=row["type"],
            payload=json.loads(row["payload_json"]),
            status=PacketStatus(row["status"]),
            priority=row["priority"],
            idempotency_key=row["idempotency_key"],
            parent_id=row["parent_id"],
            graph_id=row["graph_id"],
            trace_id=row["trace_id"],
            assigned_agent=row["assigned_agent"],
            result=json.loads(row["result_json"]) if row["result_json"] else None,
            error=row["error"],
            attempts=row["attempts"],
            max_attempts=row["max_attempts"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            deadline_at=datetime.fromisoformat(row["deadline_at"]) if row["deadline_at"] else None,
            tags=json.loads(row["tags_json"]),
            metadata=json.loads(row["metadata_json"]),
        )

    def _row_to_event(self, row: sqlite3.Row) -> EventRecord:
        return EventRecord(
            id=row["id"],
            type=row["type"],
            packet_id=row["packet_id"],
            agent_name=row["agent_name"],
            graph_id=row["graph_id"],
            trace_id=row["trace_id"],
            payload=json.loads(row["payload_json"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )
