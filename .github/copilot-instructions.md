# Queztl-Core AI Agent Instructions

## Project Overview
Queztl-Core is a **distributed computing system** with:
- **Agent-based architecture** (DNA/RNA pattern) - self-replicating, teachable agents
- **Multi-node cluster** (Beast/Sloth/Optiplex machines) with Ray distributed computing
- **Hybrid deployment** - bare metal Ubuntu servers + MacBook laptop command center
- **Multiple subsystems**: ML training, AI image generation, performance monitoring, GIS mining

## Critical Architecture Concepts

### The Agent System (Core Philosophy)
Agents are **living, self-organizing units** based on biological metaphors:
- **Agent DNA**: What the agent KNOWS (models, code, datasets) - persisted to disk, transferable
- **Agent RNA**: What the agent DOES (skills, behaviors) - runtime only
- **Agent Teaching**: Parent agents spawn and teach child agents, transferring knowledge
- **Agent Types**: Trainer, Coder, Runner, Fixer, Former, Seeder, Tester, Monitor, Coordinator

**Key Files**: `backend/queztl_agents.py`, `backend/README_AGENTS.md`

### Distributed Computing Topology
```
Laptop (macOS) → Command Center
  ├─ SSH → Beast (DHCP) - RTX 4090, 32GB RAM, image generation
  ├─ SSH → Sloth (DHCP) - Ray head node, coordination
  └─ SSH → Optiplex nodes (DNS at remote site) - Worker machines, expandable cluster
```

**Network Notes**:
- Beast/Sloth use DHCP - IPs may change, check with `nmap -sn 192.168.1.0/24` or router
- Optiplex cluster at remote site will have DNS configured (hostname resolution)
- Update `~/.ssh/config` when DHCP assigns new IPs
- **Never run heavy workloads on laptop** - always delegate to cluster nodes via SSH or Ray remote execution

### Key Technology Stack
- **Backend**: Python FastAPI, Ray (distributed), PyTorch, Stable Diffusion
- **Frontend**: Next.js 14, TypeScript, React, Recharts (deployed to Netlify)
- **Database**: PostgreSQL (metrics), Redis (caching)  
- **Deployment**: Docker Compose, bare metal Ubuntu Server 24.04 LTS
- **Communication**: WebSocket (real-time), REST API, SSH

## Essential Developer Workflows

### Starting Services
```bash
# Full stack (Docker Compose)
./backend/start.sh   # PostgreSQL + Redis + FastAPI + Dashboard

# Backend only (development)
cd backend && python3 -m uvicorn main:app --reload --port 8000

# Check service health
curl http://localhost:8000/api/health
```

### Working with the Cluster
```bash
# Find current IPs (Beast/Sloth on DHCP)
nmap -sn 192.168.1.0/24 | grep -B 2 "Host is up"

# Update SSH config when IPs change
# Edit ~/.ssh/config and update HostName entries for beast/sloth

# SSH to nodes
ssh beast   # Image generation (RTX 4090)
ssh sloth   # Ray head node
ssh optiplex1  # Remote site (uses DNS hostnames)

# Deploy code to remote node
scp -r backend/ beast:~/queztl-core/

# Run agent on remote node
ssh beast "cd ~/queztl-core && python3 backend/queztl_agents.py --spawn trainer"

# Check Ray cluster status
ssh sloth "docker exec ray-head ray status"
```

### Image Generation Workflow (Beast)
```bash
# Find Beast's current IP
BEAST_IP=$(nmap -sn 192.168.1.0/24 | grep -B 2 beast | grep "Nmap scan" | awk '{print $5}')

# Start Beast GPU server
ssh beast "cd ~/queztl-core && python3 backend/beast_image_generator.py"

# Generate image (from laptop - replace IP with current)
curl -X POST http://$BEAST_IP:8001/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"cyberpunk city","width":1024,"height":1024}'

# Images saved to: frontend/generated/ (auto-synced to website)
```

### Testing & Validation
```bash
# No formal test runner - use direct execution
python3 backend/simple_trainer.py --epochs 10   # Single-node ML training
python3 backend/test-api-routes.py              # API endpoint validation
./backend/demo-power.sh                         # Performance stress test
```

## Project-Specific Patterns

### FastAPI Application Structure
- **Main entry**: `backend/main.py` (FastAPI app, core endpoints)
- **Modular endpoints**: Scattered across many `*_endpoints.py` files (not centralized routing)
- **No middleware/interceptors** - CORS wildcard enabled for development
- **Health check pattern**: Every service has `/health` and `/api/health` endpoints

```python
# Standard endpoint pattern
@app.get("/api/metrics")
async def get_metrics():
    return {"status": "ok", "data": [...]}
```

### Agent Spawning Pattern
```python
# Create agent node
node = AgentNode(workspace=Path("workspace"))

# Spawn agent by type
trainer = node.spawn_agent(AgentType.TRAINER, "trainer-1")

# Agent teaches another
child = trainer.spawn_child(AgentType.TRAINER)
trainer.teach_agent(child)  # Transfer DNA (models, skills)
```

### Distributed Execution (Ray)
```python
# DO NOT use multiprocessing directly - use Ray for distribution
import ray

@ray.remote
def process_task(data):
    return result

# Submit to cluster
futures = [process_task.remote(d) for d in dataset]
results = ray.get(futures)
```

### File Organization Conventions
- **Autonomous scripts**: `autonomous_*.py` - self-running multi-agent orchestration
- **Demo scripts**: `demo-*.sh` - interactive demonstrations of capabilities  
- **Deployment guides**: `*_DEPLOYMENT.md`, `*_GUIDE.md` - step-by-step setup instructions
- **Large backend/**: 200+ Python files - use grep/semantic search to find relevant code

## Integration Points

### Frontend ↔ Backend
- **Deployed separately**: Frontend on Netlify (static), Backend on local/cloud (API)
- **API calls**: Frontend → `http://localhost:8000` (dev) or production API URL
- **WebSocket**: `/ws/metrics` for real-time dashboard updates
- **Generated content**: Backend saves to `frontend/generated/` for display

### Beast GPU ↔ Cluster
- **Beast runs standalone FastAPI** on port 8001 (Stable Diffusion service) - DHCP, find IP with nmap
- **Sloth coordinates** via Ray on port 8265 (dashboard at `:8265`) - DHCP, find IP with nmap
- **Optiplex cluster** at remote site uses DNS hostnames (optiplex1, optiplex2, etc.)
- **Laptop orchestrates** all nodes via SSH + HTTP API calls

### Data Flow: Training Pipeline
```
1. Problem Generator → Creates training scenario
2. Training Engine → Executes on cluster (Ray distributed)
3. Metrics Collector → Stores to PostgreSQL
4. WebSocket → Broadcasts to dashboard
5. Frontend → Live chart updates
```

## Common Pitfalls to Avoid

1. **Don't run compute on laptop** - offload to Beast/Sloth via SSH or Ray
2. **Check node IPs** - Beast/Sloth use DHCP (IPs change), use `nmap` or check router, update `~/.ssh/config`
3. **Remote Optiplex cluster** - Uses DNS at remote site, reference by hostname not IP
4. **Docker vs bare metal** - cluster nodes run bare metal Ubuntu, not Docker containers
5. **Frontend requires backend** - Netlify frontend is static HTML, needs API running for functionality
6. **Ray cluster mode** - Always verify Ray head node is running before distributed tasks

## Quick Reference Commands

```bash
# Find current IPs (DHCP)
nmap -sn 192.168.1.0/24 | grep -B 2 "Host is up"

# Update SSH config with new IPs
nano ~/.ssh/config  # Update HostName for beast/sloth

# Cluster status
ssh sloth "docker exec ray-head ray status"

# Deploy to local nodes (DHCP)
for node in beast sloth; do scp -r backend/ $node:~/queztl-core/; done

# Deploy to remote Optiplex cluster (DNS)
for node in optiplex1 optiplex2 optiplex3; do scp -r backend/ $node:~/queztl-core/; done

# Beast GPU workload (find IP first)
BEAST_IP=$(ssh beast "hostname -I | awk '{print \$1}'")
python3 backend/beast_workload_runner.py 3 20   # 3 parallel, 20s interval

# Start full system
./backend/start.sh && cd frontend && python3 -m http.server 8080

# Monitor logs
tail -f /tmp/gis-studio-logs/backend.log
```

## Key Documentation Files
- `backend/README.md` - Full system overview
- `backend/README_AGENTS.md` - Agent system quick start  
- `backend/ARCHITECTURE.md` - Detailed component architecture
- `MULTI_SITE_DEPLOYMENT.md` - Cluster deployment topology
- `BEAST_SLOTH_DEPLOYMENT.md` - Bare metal setup guide

## Development Philosophy
This is a **proof-of-concept distributed AI system** prioritizing:
- **Autonomous operation** over manual configuration
- **Self-organization** over centralized control  
- **Expandability** over optimization (add nodes, not refactor)
- **Working demos** over comprehensive tests

When in doubt, follow the agent pattern: spawn, teach, distribute.
