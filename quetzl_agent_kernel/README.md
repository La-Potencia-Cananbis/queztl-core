# Quetzl Agent Kernel V3

A durable, graph-native agent scaffold for Quetzl Core.

This is intentionally separate from the existing prototype agents. It preserves the original idea—specialized agents coordinated by a broker—but formalizes it as a small execution kernel.

## Design goals

- Durable task packets stored in SQLite
- Append-only event log
- Capability-based routing instead of hardcoded agent maps
- Bounded async workers per agent
- DAG/graph workflow execution
- Idempotency keys
- Safe task lifecycle: pending, running, completed, failed, cancelled
- Observable execution events
- Extensible local/phone/cloud agent backends

## Core vocabulary

```text
ActionPacket = durable task packet
Capability   = operation an agent can perform
Agent        = bounded worker that handles capabilities
EventLog     = append-only record of task/agent events
Scheduler    = routes packets and evaluates graphs
GraphSpec    = executable DAG of ActionPackets
```

## Quick start

```bash
cd quetzl_agent_kernel
python -m venv .venv
source .venv/bin/activate
pip install -e .[api]
quetzl-kernel demo
```

Run API server:

```bash
uvicorn quetzl_agent_kernel.api:app --reload
```

Submit a task:

```bash
curl -X POST http://localhost:8000/tasks \
  -H 'Content-Type: application/json' \
  -d '{"type":"echo.say","payload":{"text":"hello graph"}}'
```

## Why this differs from generic agent frameworks

Most current agent frameworks are prompt-loop first. This kernel is packet/graph first:

```text
prompt-loop agent: LLM decides next action
Quetzl kernel: graph scheduler routes typed packets across durable specialized agents
```

LLMs are just one capability type, not the runtime itself.

## Next targets

- Termux bridge agent
- Camera/mic/sensor packet ingestion
- LiteRT/Gemma local model agent
- FFmpeg render agent
- WebSocket graph cockpit
- Desktop/cloud worker registry
