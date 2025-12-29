# QuetzalCore Integration Plan
## Pulling Everything Together - December 10, 2025

### Current State
- **Backend**: Running on Render.com (rebuilding with 5K renderer)
- **Frontend**: Running on Netlify
- **Components**: 5K Renderer, 3D Workload, GIS Studio, VM Console, Mining
- **Status**: Distributed across cloud services

### Goal: Run Everything on QuetzalCore AIOS

## Phase 1: Fix & Verify Cloud Services (30 min)
1. **Wait for Render rebuild to complete** (10 min)
   - 5K renderer endpoint at `/api/render/5k`
   - Test all three scenes: photorealistic, fractal, benchmark

2. **Fix GIS Studio 500 error** (10 min)
   - Location: `backend/main.py` line ~3606
   - Issue: `gis_trainer.models.keys()` AttributeError
   - Fix: Add try-except wrapper

3. **Test full stack** (10 min)
   - Frontend → Backend connection
   - All endpoints working
   - Dashboard displaying data

## Phase 2: Integrate with QuetzalCore Hypervisor (1 hour)
1. **Compile QuetzalCore Hypervisor** (30 min)
   ```bash
   cd /Users/xavasena/hive/quetzalcore-hypervisor
   cargo build --release
   ```

2. **Create QuetzalCore OS Image** (30 min)
   - Base: Ubuntu or custom Linux
   - Include: Python runtime, backend code, dependencies
   - Package as bootable image

## Phase 3: Run VMs on QuetzalCore (1 hour)
1. **Boot VM with backend inside**
   ```bash
   qctl vm create --name backend-vm --image quetzalcore-os.img
   qctl vm start backend-vm
   ```

2. **Configure networking**
   - Bridge VM network to host
   - Expose backend ports
   - Connect frontend to VM backend

3. **Run dashboard in separate VM**
   ```bash
   qctl vm create --name frontend-vm --image quetzalcore-os.img
   qctl vm start frontend-vm
   ```

## Phase 4: Full QuetzalCore Stack (30 min)
1. **Multi-VM Architecture**
   - VM 1: Backend API (Python/FastAPI)
   - VM 2: Frontend Dashboard (Next.js)
   - VM 3: Database/Redis
   - VM 4: Worker nodes (mining, 3D, GIS)

2. **Orchestration**
   - QuetzalCore manages all VMs
   - Load balancing across workers
   - Auto-scaling based on workload

3. **Testing**
   - 5K render from VM
   - 3D workload benchmark
   - GIS processing
   - Mining operations

## Immediate Next Steps (Right Now)
1. ✅ 5K renderer deployed (waiting for Render)
2. 🔧 Fix GIS Studio 500 error
3. 📦 Compile QuetzalCore Hypervisor
4. 🖥️ Build QuetzalCore OS image
5. 🚀 Boot everything on QuetzalCore

## Commands to Execute

### Fix GIS Error
```python
# In backend/main.py around line 3606
try:
    "trainer": {"status": "ready", "models": list(gis_trainer.models.keys())},
except AttributeError:
    "trainer": {"status": "ready", "models": []},
```

### Compile Hypervisor
```bash
cd /Users/xavasena/hive/quetzalcore-hypervisor
cargo build --release
./target/release/quetzalcore-hv --version
```

### Build OS Image
```bash
cd /Users/xavasena/hive/quetzalcore-os
./build-quetzalcore-os.sh
```

### Run on QuetzalCore
```bash
# Start hypervisor
qctl hv start

# Create VMs
qctl vm create backend --cpu 4 --memory 8G --disk quetzalcore-backend.img
qctl vm create frontend --cpu 2 --memory 4G --disk quetzalcore-frontend.img

# Start services
qctl vm start backend
qctl vm start frontend

# Check status
qctl status
```

## Success Criteria
- [ ] 5K renderer working via API
- [ ] GIS Studio no 500 errors
- [ ] QuetzalCore HV compiled and running
- [ ] QuetzalCore OS bootable
- [ ] Backend running in QuetzalCore VM
- [ ] Frontend connected to VM backend
- [ ] All workloads (3D, mining, GIS, 5K) working in VMs
- [ ] Dashboard shows real-time VM metrics

## Timeline
- **Now**: Fix GIS, wait for Render
- **+30 min**: Compile hypervisor
- **+1 hour**: Build OS image
- **+1.5 hours**: Boot VMs and test
- **+2 hours**: Full QuetzalCore stack running

---
**¿Listo para hacerlo, ese?** Let's start with fixing GIS and compiling the hypervisor while Render finishes!
