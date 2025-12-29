# 🦅 QuetzalCore Core - Deployment Architecture

## Your Mac = Development Only ❌ No Services Running

```
┌─────────────────────────────────────┐
│      YOUR MAC (M1)                  │
│  ❌ NO backend running              │
│  ❌ NO Docker running                │
│  ❌ NO services running              │
│                                     │
│  ✅ VS Code (code editing)          │
│  ✅ Git (version control)           │
│  ✅ Deployment scripts              │
└─────────────────────────────────────┘
          │
          │ git push / deploy scripts
          ▼
┌─────────────────────────────────────┐
│   CLOUD (senasaitech.com)           │
│   ✅ FastAPI Gateway (port 443)     │
│   ✅ SSL Certificate                │
│   ✅ Nginx Reverse Proxy            │
│   ✅ Load Balancer                  │
│                                     │
│   Routes requests to QuetzalCore Core    │
└─────────────────────────────────────┘
          │
          │ API calls
          ▼
┌─────────────────────────────────────┐
│   QUETZALCORE CORE (Distributed)         │
│   Master Node: Orchestration        │
│   ├─ Task queue                     │
│   ├─ Worker assignment              │
│   └─ Result aggregation             │
└─────────────────────────────────────┘
          │
          │ Distribute workload
          ▼
┌──────────────────────────────────────────────────────────┐
│              QUETZALCORE WORKER NODES                          │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │
│  │  Worker 1    │ │  Worker 2    │ │  Worker 3    │     │
│  │              │ │              │ │              │     │
│  │ Native HV    │ │ Native HV    │ │ Native HV    │     │
│  │ ├─ VM Pool   │ │ ├─ VM Pool   │ │ ├─ VM Pool   │     │
│  │ ├─ GPU Sim   │ │ ├─ GPU Sim   │ │ ├─ GPU Sim   │     │
│  │ └─ Process   │ │ └─ Process   │ │ └─ Process   │     │
│  │    Isolation │ │    Isolation │ │    Isolation │     │
│  └──────────────┘ └──────────────┘ └──────────────┘     │
└──────────────────────────────────────────────────────────┘
```

---

## Request Flow

### Example: Mining MAG Survey Analysis

```
1. Client uploads survey
   ↓
2. Cloud API (senasaitech.com)
   POST /api/mining/mag-survey
   ↓
3. QuetzalCore Master receives task
   {
     "task_id": "mag_123",
     "type": "mineral_discrimination",
     "data": {...}
   }
   ↓
4. Master assigns to Worker 2
   ↓
5. Worker 2 Native HV creates VM
   - Allocate: 4 CPU cores, 8GB RAM
   - Assign: vGPU with 8,192 threads
   - Isolate: Process namespace
   ↓
6. VM runs computation
   - Load Rust WASM module
   - Process MAG data with GPU sim
   - Compute mineral signatures
   ↓
7. VM returns results to Master
   ↓
8. Master aggregates and returns to Cloud API
   ↓
9. Client receives results
```

---

## Component Locations

### Your Mac
```
/Users/xavasena/hive/
├── backend/                    # Source code
│   ├── native_hypervisor.py
│   ├── gpu_simulator.py
│   └── main.py
├── deploy-hv-to-quetzalcore.sh     # Deploy to workers
└── deploy-to-senasaitech.sh   # Deploy to cloud
```

**Purpose:** Development only. No services run here.

### Cloud Server (senasaitech.com)
```
/var/www/quetzalcore/
├── backend/
│   └── main.py                # FastAPI gateway only
├── nginx/
│   └── quetzalcore.conf           # SSL + reverse proxy
└── logs/
    └── access.log
```

**Purpose:** Public API gateway, SSL termination, load balancing.

### QuetzalCore Master Node
```
/opt/quetzalcore/
├── master.py                  # Task orchestration
├── task_queue/
├── worker_registry.json
└── results_cache/
```

**Purpose:** Distribute work to worker nodes, aggregate results.

### QuetzalCore Worker Nodes
```
/opt/quetzalcore/
├── native_hypervisor.py       # ⭐ RUNS HERE
├── gpu_simulator.py           # ⭐ RUNS HERE
├── webgpu_driver.py
├── wasm_runtime/
│   └── *.wasm modules
└── vm_instances/
    ├── vm_0/
    ├── vm_1/
    └── vm_2/
```

**Purpose:** Execute heavy computation in isolated VMs with virtual GPUs.

---

## Deployment Commands

### 1. Deploy Gateway to Cloud
```bash
export SERVER_IP="senasaitech.com"
./deploy-to-senasaitech.sh
```

This deploys:
- FastAPI gateway
- Nginx with SSL
- Load balancer config

### 2. Deploy Hypervisor to QuetzalCore Workers
```bash
export QUETZALCORE_MASTER="master.quetzalcore.local:9000"
export WORKER_NODES="worker1.quetzalcore.local,worker2.quetzalcore.local,worker3.quetzalcore.local"
./deploy-hv-to-quetzalcore.sh
```

This deploys:
- Native hypervisor
- GPU simulator
- WASM runtime
- Systemd service

### 3. Stop Everything on Mac
```bash
# Kill all local processes
pkill -f "uvicorn|python.*backend"

# Stop Docker
docker stop $(docker ps -q)

# Your Mac is now clean ✅
```

---

## Configuration Files

### Cloud API Gateway (senasaitech.com)
```python
# /var/www/quetzalcore/backend/main.py

from fastapi import FastAPI
import httpx

app = FastAPI()

QUETZALCORE_MASTER = "http://master.quetzalcore.local:9000"

@app.post("/api/mining/mag-survey")
async def mag_survey(data: dict):
    # Forward to QuetzalCore Core
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{QUETZALCORE_MASTER}/process",
            json={"task": "mag_survey", "data": data}
        )
        return response.json()
```

### QuetzalCore Master Node
```python
# /opt/quetzalcore/master.py

from fastapi import FastAPI
from backend.distributed_network import QuetzalCoreMaster

app = FastAPI()
master = QuetzalCoreMaster()

@app.post("/process")
async def process_task(task: dict):
    # Assign to worker with HV
    worker_id = master.select_worker()
    result = await master.execute_on_worker(worker_id, task)
    return result
```

### QuetzalCore Worker Node
```python
# /opt/quetzalcore/worker.py

from backend.native_hypervisor import QuetzalCoreHypervisor
from fastapi import FastAPI

app = FastAPI()
hv = QuetzalCoreHypervisor(num_gpus=4)

@app.post("/execute")
async def execute(task: dict):
    # Create VM
    vm = hv.create_vm(
        cpu_cores=4,
        memory_mb=8192,
        gpu_enabled=True
    )
    
    # Run workload
    result = await hv.start_vm(vm.vm_id, task)
    
    # Cleanup
    hv.stop_vm(vm.vm_id)
    
    return result
```

---

## Resource Allocation

### Per Worker Node (Recommended):
- **CPUs:** 16 cores (4 VMs × 4 cores each)
- **RAM:** 64GB (4 VMs × 16GB each)
- **vGPUs:** 4 virtual GPUs (8,192 threads each)
- **Storage:** 500GB SSD

### Per VM Instance:
- **CPUs:** 2-8 cores (configurable)
- **RAM:** 4-16GB (configurable)
- **vGPU:** 1 virtual GPU (8,192 threads)
- **Isolation:** Full process namespace

---

## Monitoring

### Check Worker Status
```bash
# SSH to any worker
ssh quetzalcore@worker1.quetzalcore.local

# Check hypervisor service
systemctl status quetzalcore-hv

# Check running VMs
ps aux | grep "vm_process_worker"

# Check resource usage
htop
```

### Check Master Status
```bash
curl http://master.quetzalcore.local:9000/status
```

Response:
```json
{
  "workers": 3,
  "active_vms": 8,
  "queue_depth": 2,
  "total_cores": 48,
  "total_memory_gb": 192
}
```

### Check Cloud Gateway
```bash
curl https://senasaitech.com/api/health
```

---

## Advantages of This Architecture

### ✅ Your Mac Stays Clean
- No services running
- No resource usage
- Just code editing

### ✅ Scalable Compute
- Add more QuetzalCore workers anytime
- Each worker = 4-8 VMs
- Horizontal scaling

### ✅ Isolated Workloads
- Each VM = isolated process
- Crash in one VM ≠ crash all
- Security boundaries

### ✅ Efficient Resource Usage
- Native processes (not Docker)
- 5-10% overhead (vs Docker 30-50%)
- Virtual GPU simulation

### ✅ Cloud + On-Prem Hybrid
- Cloud: Public API, SSL, auth
- QuetzalCore: Heavy computation, VMs
- Best of both worlds

---

## Next Steps

1. **Set up QuetzalCore worker nodes** (Linux servers/VMs)
2. **Deploy Native HV** to workers with `./deploy-hv-to-quetzalcore.sh`
3. **Deploy API Gateway** to cloud with `./deploy-to-senasaitech.sh`
4. **Configure Master Node** with worker registry
5. **Test end-to-end** MAG survey request

---

## Summary

**Your Mac:** 
- Code only, no services ❌

**Cloud (senasaitech.com):**
- API gateway, SSL, public access ✅

**QuetzalCore Core Workers:**
- Native HV, GPU simulator, VMs ✅⭐

**Everything runs on the QuetzalCore network, not your Mac!** 🦅
