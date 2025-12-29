#!/bin/bash
# Hive Distributed Architecture Setup
# Mac = Lightweight orchestrator only
# Remote runners = Heavy compute workloads

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     🌐 HIVE DISTRIBUTED ARCHITECTURE SETUP                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Stop all heavy processes on Mac
echo -e "${YELLOW}Step 1: Cleaning up local Mac processes...${NC}"
docker exec hive-backend-1 bash -c 'pkill -f "train_" 2>/dev/null || true'
docker exec hive-backend-1 bash -c 'pkill -f "queztl_auto_optimizer" 2>/dev/null || true'
docker exec hive-backend-1 bash -c 'pkill -f "queztl_ml_optimizer" 2>/dev/null || true'
docker exec hive-backend-1 bash -c 'pkill -f "enhanced_training" 2>/dev/null || true'
echo -e "${GREEN}✅ Local processes stopped${NC}"

# Step 2: Configure Mac as orchestrator only
echo -e "\n${YELLOW}Step 2: Configuring Mac as lightweight orchestrator...${NC}"

cat > /tmp/hive_orchestrator.py << 'EOF'
#!/usr/bin/env python3
"""
Hive Orchestrator - Runs on Mac
Dispatches work to remote runners, doesn't do heavy compute locally
"""

import asyncio
import aiohttp
import json
from datetime import datetime
from typing import List, Dict

class HiveOrchestrator:
    """Lightweight orchestrator that dispatches to remote workers"""
    
    def __init__(self):
        self.workers = []
        self.task_queue = asyncio.Queue()
        self.results = {}
        
    async def register_worker(self, worker_url: str, capabilities: List[str]):
        """Register a remote Hive worker"""
        worker = {
            "url": worker_url,
            "capabilities": capabilities,
            "status": "active",
            "tasks_completed": 0,
            "registered_at": datetime.now().isoformat()
        }
        self.workers.append(worker)
        print(f"✅ Registered worker: {worker_url} with {len(capabilities)} capabilities")
        
    async def dispatch_task(self, task_type: str, params: dict):
        """Dispatch task to available worker (not local)"""
        # Find worker with capability
        for worker in self.workers:
            if task_type in worker["capabilities"] and worker["status"] == "active":
                return await self._execute_on_worker(worker, task_type, params)
        
        # No remote worker available - queue it, DON'T run locally
        print(f"⚠️  No worker available for {task_type}, queuing...")
        await self.task_queue.put({"type": task_type, "params": params})
        return {"status": "queued", "message": "Waiting for worker"}
    
    async def _execute_on_worker(self, worker: dict, task_type: str, params: dict):
        """Execute task on remote worker via HTTP"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{worker['url']}/execute",
                    json={"task": task_type, "params": params},
                    timeout=aiohttp.ClientTimeout(total=300)
                ) as response:
                    result = await response.json()
                    worker["tasks_completed"] += 1
                    return result
        except Exception as e:
            worker["status"] = "error"
            return {"error": str(e), "worker": worker["url"]}
    
    async def get_status(self):
        """Get orchestrator status"""
        return {
            "role": "orchestrator",
            "local_compute": "disabled",
            "workers": len(self.workers),
            "active_workers": sum(1 for w in self.workers if w["status"] == "active"),
            "queued_tasks": self.task_queue.qsize(),
            "worker_details": self.workers
        }

# Global orchestrator instance
orchestrator = HiveOrchestrator()

if __name__ == "__main__":
    print("🎛️  Hive Orchestrator (Lightweight Mode)")
    print("=" * 60)
    print("This Mac runs ORCHESTRATION ONLY")
    print("All heavy compute is dispatched to remote Hive workers")
    print("=" * 60)
EOF

docker cp /tmp/hive_orchestrator.py hive-backend-1:/workspace/
echo -e "${GREEN}✅ Orchestrator configured${NC}"

# Step 3: Create lightweight docker-compose for Mac
echo -e "\n${YELLOW}Step 3: Creating lightweight Docker Compose configuration...${NC}"

cat > /tmp/docker-compose.mac.yml << 'EOF'
# Lightweight Docker Compose for Mac (Orchestrator Only)
version: '3.8'

services:
  # Lightweight orchestrator API
  orchestrator:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "8000:8000"  # API only
    environment:
      - HIVE_ROLE=orchestrator
      - HIVE_MODE=lightweight
      - MAX_LOCAL_WORKERS=0  # No local compute
    volumes:
      - ./backend:/workspace/backend
    deploy:
      resources:
        limits:
          cpus: '2.0'      # Max 2 CPU cores
          memory: 1G       # Max 1GB RAM
    command: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 1
    
  # Lightweight DB for orchestration metadata only
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: hive_orchestrator
    ports:
      - "5432:5432"
    volumes:
      - postgres_data_mac:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
          
  # Redis for job queue (lightweight)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 128M

volumes:
  postgres_data_mac:
EOF

cp /tmp/docker-compose.mac.yml docker-compose.mac.yml
echo -e "${GREEN}✅ Lightweight config created${NC}"

# Step 4: Create remote worker configuration
echo -e "\n${YELLOW}Step 4: Creating remote worker configuration...${NC}"

cat > /tmp/docker-compose.worker.yml << 'EOF'
# Heavy Compute Worker (Deploy on remote machines/cloud)
version: '3.8'

services:
  worker:
    build:
      context: .
      dockerfile: backend/Dockerfile.worker
    environment:
      - HIVE_ROLE=worker
      - HIVE_ORCHESTRATOR_URL=http://YOUR_MAC_IP:8000
      - WORKER_CAPABILITIES=training,gis,geophysics,3d-generation
    ports:
      - "9000:9000"  # Worker API
    volumes:
      - ./models:/workspace/models
      - worker_data:/workspace/data
    deploy:
      resources:
        # Workers can use ALL resources
        limits:
          cpus: '32.0'      # Use all available CPUs
          memory: 32G       # Use all available RAM
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    command: python3 /workspace/hive_worker.py

volumes:
  worker_data:
EOF

cp /tmp/docker-compose.worker.yml docker-compose.worker.yml
echo -e "${GREEN}✅ Worker config created${NC}"

# Step 5: Create worker daemon
echo -e "\n${YELLOW}Step 5: Creating worker daemon...${NC}"

cat > /tmp/hive_worker.py << 'EOF'
#!/usr/bin/env python3
"""
Hive Worker - Runs on remote machines with heavy compute
Pulls tasks from orchestrator and executes them
"""

import asyncio
import aiohttp
import torch
import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class WorkerConfig:
    orchestrator_url = os.getenv("HIVE_ORCHESTRATOR_URL")
    capabilities = os.getenv("WORKER_CAPABILITIES", "").split(",")
    worker_id = os.getenv("HOSTNAME", "worker-1")
    
config = WorkerConfig()

class Task(BaseModel):
    task: str
    params: dict

@app.on_event("startup")
async def register_with_orchestrator():
    """Register this worker with orchestrator"""
    if not config.orchestrator_url:
        print("⚠️  No orchestrator URL configured, running standalone")
        return
        
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{config.orchestrator_url}/register_worker",
                json={
                    "worker_id": config.worker_id,
                    "url": f"http://{config.worker_id}:9000",
                    "capabilities": config.capabilities,
                    "gpu_available": torch.cuda.is_available(),
                    "cpu_count": os.cpu_count()
                }
            ) as response:
                print(f"✅ Registered with orchestrator: {await response.json()}")
    except Exception as e:
        print(f"⚠️  Could not register with orchestrator: {e}")

@app.post("/execute")
async def execute_task(task: Task):
    """Execute a task on this worker"""
    print(f"🔥 Executing task: {task.task}")
    
    # Import heavy modules only when needed
    if task.task == "training":
        from train_gis_geophysics import train_model
        result = await train_model(**task.params)
    elif task.task == "gis":
        from gis_processor import process_lidar
        result = await process_lidar(**task.params)
    elif task.task == "3d-generation":
        from text_to_3d import generate_model
        result = await generate_model(**task.params)
    else:
        result = {"error": f"Unknown task: {task.task}"}
    
    return {"status": "completed", "result": result}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "worker_id": config.worker_id,
        "capabilities": config.capabilities,
        "gpu": torch.cuda.is_available()
    }

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Hive Worker {config.worker_id} starting...")
    print(f"Capabilities: {config.capabilities}")
    print(f"GPU Available: {torch.cuda.is_available()}")
    uvicorn.run(app, host="0.0.0.0", port=9000)
EOF

docker cp /tmp/hive_worker.py hive-backend-1:/workspace/
echo -e "${GREEN}✅ Worker daemon created${NC}"

# Step 6: Restart with lightweight config
echo -e "\n${YELLOW}Step 6: Switching to lightweight orchestrator mode...${NC}"

# Stop current setup
docker-compose down

# Start lightweight orchestrator
docker-compose -f docker-compose.mac.yml up -d

sleep 3

echo ""
echo -e "${GREEN}✅ HIVE RESTRUCTURED FOR DISTRIBUTED COMPUTE${NC}"
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                 🎯 ARCHITECTURE SUMMARY                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}YOUR MAC (Orchestrator Only):${NC}"
echo "  • Lightweight API server (max 2 CPU cores, 1GB RAM)"
echo "  • Task dispatcher and queue manager"
echo "  • Worker registry and health monitoring"
echo "  • No heavy compute or ML training"
echo ""
echo -e "${YELLOW}REMOTE WORKERS (Heavy Compute):${NC}"
echo "  • Full CPU/GPU access for training"
echo "  • GIS/Geophysics processing"
echo "  • 3D model generation"
echo "  • Protocol optimization"
echo ""
echo -e "${YELLOW}TO DEPLOY WORKERS:${NC}"
echo "  1. On remote machine: scp docker-compose.worker.yml user@remote:/path/"
echo "  2. Edit HIVE_ORCHESTRATOR_URL to your Mac's IP"
echo "  3. Run: docker-compose -f docker-compose.worker.yml up -d"
echo ""
echo -e "${YELLOW}WORKER DEPLOYMENT OPTIONS:${NC}"
echo "  • AWS EC2 instances (g4dn.xlarge for GPU)"
echo "  • Digital Ocean Droplets with GPU"
echo "  • Your studio servers"
echo "  • Other team members' machines"
echo ""
echo -e "${GREEN}Your Mac is now running in lightweight orchestrator mode! 🎉${NC}"
