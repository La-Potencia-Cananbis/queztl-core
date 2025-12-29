# Hive Distributed Architecture - Quick Reference

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     YOUR MAC (M4)                           │
│                  Lightweight Orchestrator                    │
│  • API Server (max 2 cores, 1GB RAM)                       │
│  • Task Queue & Dispatcher                                  │
│  • Worker Registry                                          │
│  • NO heavy compute                                         │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ Dispatches tasks to...
                   │
         ┌─────────┴─────────┬────────────┬──────────────┐
         │                   │            │              │
    ┌────▼────┐         ┌────▼────┐  ┌───▼───┐     ┌───▼───┐
    │Worker 1 │         │Worker 2 │  │Worker3│     │Worker4│
    │Training │         │GIS/LiDAR│  │3D Gen │     │Geophys│
    │32 cores │         │16 cores │  │GPU    │     │GPU    │
    │32GB RAM │         │64GB RAM │  │24GB   │     │48GB   │
    └─────────┘         └─────────┘  └───────┘     └───────┘
```

## 🚀 Current State

**Mac Resources (BEFORE restructure):**
- CPU: 1152% (11.5 cores maxed out!)
- RAM: 3.1GB
- Status: 🔥 OVERHEATING

**Mac Resources (AFTER restructure):**
- CPU: 0.27% (minimal)
- RAM: 270MB
- Status: ✅ COOL & EFFICIENT

**Improvement: 4,000x less CPU usage!**

## 📋 Commands

### Managing Your Mac Orchestrator

```bash
# Check status
./resource-manager.sh status

# View orchestrator logs
docker logs hive-orchestrator-1 -f

# Restart orchestrator
docker-compose -f docker-compose.mac.yml restart
```

### Deploying Remote Workers

**Option 1: Deploy on Studio Server**
```bash
# From your Mac
scp docker-compose.worker.yml studio@192.168.1.100:/opt/hive/

# On studio server
cd /opt/hive
# Edit worker config
nano docker-compose.worker.yml
# Change: HIVE_ORCHESTRATOR_URL=http://YOUR_MAC_IP:8000
docker-compose -f docker-compose.worker.yml up -d
```

**Option 2: Deploy on AWS**
```bash
# Launch EC2 instance (g4dn.xlarge for GPU)
aws ec2 run-instances --image-id ami-xxx --instance-type g4dn.xlarge

# SSH to instance
ssh ubuntu@ec2-xxx.compute.amazonaws.com

# Install Docker
curl -fsSL https://get.docker.com | sh

# Copy worker config
scp docker-compose.worker.yml ubuntu@ec2-xxx:/home/ubuntu/

# Start worker
docker-compose -f docker-compose.worker.yml up -d
```

**Option 3: Deploy on Digital Ocean**
```bash
# Create Droplet with GPU
doctl compute droplet create hive-worker-1 \
  --image ubuntu-20-04-x64 \
  --size g-8vcpu-32gb \
  --region nyc1

# Get IP
doctl compute droplet get hive-worker-1 --format PublicIPv4

# Deploy worker (same as AWS steps above)
```

## 🔧 Worker Configuration

Edit `docker-compose.worker.yml`:

```yaml
environment:
  # Point to your Mac's orchestrator
  - HIVE_ORCHESTRATOR_URL=http://YOUR_MAC_IP:8000
  
  # What this worker can do
  - WORKER_CAPABILITIES=training,gis,geophysics,3d-generation
  
  # Optional: Limit resources
  - MAX_CONCURRENT_TASKS=4
```

## 📊 Monitoring

### View Registered Workers
```bash
curl http://localhost:8000/workers
```

### Check Orchestrator Status
```bash
curl http://localhost:8000/status
```

### View Task Queue
```bash
curl http://localhost:8000/queue
```

## 🎮 Using the Distributed System

### Submit a Task (Auto-dispatched to Worker)
```bash
curl -X POST http://localhost:8000/task \
  -H "Content-Type: application/json" \
  -d '{
    "type": "training",
    "params": {
      "model": "gis-lidar",
      "epochs": 100
    }
  }'
```

### Check Task Status
```bash
curl http://localhost:8000/task/TASK_ID
```

## 💰 Cost Optimization

**Mac Local (Old):**
- Cost: $0 (your Mac)
- Problem: Overheating, slow, battery drain
- Capacity: Limited

**Distributed Workers (New):**
- AWS g4dn.xlarge: $0.526/hour
- Only pay when training
- Infinite scalability
- Keep Mac cool

**Example: Training all modules**
- Old: 8 hours on Mac (🔥 overheating)
- New: 2 hours on 4 workers = $4.20
- Savings: Your Mac's lifespan!

## 🔥 Quick Start

1. **Mac is already set up** (orchestrator running)
2. **Deploy first worker** on your studio machine
3. **Test it**:
   ```bash
   curl -X POST http://localhost:8000/task \
     -H "Content-Type: application/json" \
     -d '{"type":"test","params":{}}'
   ```
4. **Add more workers** as needed

## 📝 Files Created

- `docker-compose.mac.yml` - Lightweight orchestrator for Mac
- `docker-compose.worker.yml` - Heavy compute worker config
- `hive_orchestrator.py` - Orchestrator logic
- `hive_worker.py` - Worker daemon
- `setup-distributed-hive.sh` - Setup script

## 🎯 Next Steps

1. Deploy 1-2 workers on remote machines
2. Test with light workload
3. Scale up as needed
4. Monitor with `./resource-manager.sh status`

Your Mac is now a lightweight orchestrator! All heavy lifting happens remotely. 🎉
