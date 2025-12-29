# Queztl Training System

**apt/yum-like ML training manager + Kubernetes-like distributed orchestration**

## Quick Start

```bash
# Simple training (in existing container)
./qtm list                    # See 8 available modules
./qtm install gis-lidar       # Train a module
./qtm status                  # Check progress

# Distributed training (parallel, sandboxed)
./hive-control init           # Build images (one-time)
./hive-control start          # Start orchestrator + 1 runner
./hive-control scale 4        # Scale to 4 runners
./hive-control submit image-to-3d high  # Submit job
./hive-control monitor        # Watch progress
```

## Components

| Component | Purpose | Command |
|-----------|---------|---------|
| **QTM** | apt-like training manager | `./qtm <cmd>` |
| **Hive** | Distributed orchestration | `./hive-control <cmd>` |
| **Orchestrator** | Manages queue & runners | Port 9000 API |
| **Runners** | Sandboxed training containers | 2 CPU, 4GB RAM each |

## Modules (8 Total)

| Module | Time | Competes With | Priority |
|--------|------|---------------|----------|
| image-to-3d | 60m | Hexa3D | HIGH |
| enhanced-3d | 40m | Premium 3D | HIGH |
| gis-lidar | 30m | Hexagon Geospatial | HIGH |
| geophysics-magnetic | 35m | Geosoft Oasis ($300K+) | HIGH |
| gis-buildings | 25m | Building extraction | MED |
| geophysics-resistivity | 30m | Resistivity inversion | MED |
| text-to-3d | 80m | Text-to-3D | MED |
| geophysics-seismic | 25m | Seismic analysis | LOW |

**Total sequential: 165min | Parallel (4 runners): 60min = 63% faster**

## Architecture

```
QTM (Simple)              Hive (Distributed)
─────────────             ──────────────────────
./qtm install             Orchestrator (9000)
    ↓                            ↓
Backend Container         Runner-1 Runner-2 Runner-3 Runner-4
    ↓                       ↓        ↓        ↓        ↓
 1 Model                  4 Models in Parallel
```

## Key Files

```
training_manager.py       # Core training logic (8 modules)
qtm                       # QTM wrapper
hive-control              # Hive orchestration CLI
docker-compose.training.yml  # Infrastructure
training-runner/          # Orchestrator + Runner images
  ├── orchestrator.py     # Queue manager, auto-scaler
  ├── runner.py           # Sandboxed executor
  └── Dockerfile.*        # Minimal Python images
```

## Usage Patterns

**Development** - Single module, test quickly:
```bash
./qtm info gis-lidar && ./qtm install gis-lidar
```

**Production** - All high-priority, maximum speed:
```bash
./hive-control init && ./hive-control start
./hive-control scale 4
for m in image-to-3d enhanced-3d gis-lidar geophysics-magnetic; do
  ./hive-control submit $m high
done
```

**Monitoring**:
```bash
./qtm status              # QTM progress
./hive-control monitor    # Hive real-time dashboard
```

## When to Use Which

| Scenario | Use | Command |
|----------|-----|---------|
| Test 1 module | QTM | `./qtm install <module>` |
| Train all modules fast | Hive | `./hive-control scale 4` |
| Limited resources | Hive | Resource limits enforced |
| Development | QTM | No setup needed |
| CI/CD | Hive | Isolated, reproducible |

## Troubleshooting

```bash
# QTM not working?
./qtm check-deps          # Check Python packages
docker exec hive-backend-1 tail -f /workspace/training_logs/*.log

# Hive not working?
./hive-control status     # Check orchestrator
./hive-control restart    # Restart all
docker logs queztl-orchestrator  # Debug orchestrator
```

## Documentation

- **This file** - Overview
- `QTM_QUICKREF.md` - QTM command reference
- `training-runner/README.md` - Hive deep dive
- `./qtm --help` - Inline help
- `./hive-control` - Command list
