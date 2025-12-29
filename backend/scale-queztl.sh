#!/bin/bash
# 🦅 QuetzalCore Core - Scale Workers for Mining Workloads

set -e

echo "🦅 QUETZALCORE CORE - SCALABLE DEPLOYMENT"
echo "======================================"
echo ""

# Show current architecture
cat << 'EOF'
Current Architecture:
┌─────────────────────────────────────────────────────┐
│  YOUR MAC (stops running services)                  │
│  - Just code editing                                │
│  - Git commits                                       │
│  - Deploy scripts                                    │
└─────────────────────────────────────────────────────┘
                    │
                    │ docker-compose up
                    ▼
┌─────────────────────────────────────────────────────┐
│  QUETZALCORE DOCKER SWARM (Cloud/Remote Servers)         │
│                                                      │
│  Master (orchestrator):                             │
│  ├─ FastAPI Backend (port 8000)                     │
│  ├─ Autoscaler (monitors load)                      │
│  ├─ PostgreSQL (metrics)                            │
│  └─ Redis (job queue)                               │
│                                                      │
│  Workers (scale 0-N):                               │
│  ├─ Worker 1: 2 CPU, 4GB, mining APIs               │
│  ├─ Worker 2: 4 CPU, 8GB, 3D generation             │
│  ├─ Worker 3: 8 CPU, 16GB, ML training              │
│  └─ Worker 4+: Auto-scaled based on load            │
└─────────────────────────────────────────────────────┘
EOF

echo ""
echo "Available Deployment Options:"
echo ""
echo "1️⃣  LOCAL TEST (Mac, lightweight)"
echo "   docker-compose -f docker-compose.mac.yml up"
echo "   - Minimal resources"
echo "   - No GPU"
echo "   - Development only"
echo ""

echo "2️⃣  FULL STACK (Cloud, production)"
echo "   docker-compose up -d"
echo "   - Backend + DB + Redis"
echo "   - Dashboard"
echo "   - Production ready"
echo ""

echo "3️⃣  TRAINING CLUSTER (ML workloads)"
echo "   docker-compose -f docker-compose.training.yml up -d"
echo "   - Orchestrator + 4 runners"
echo "   - Auto-scaling enabled"
echo "   - ML training optimized"
echo ""

echo "4️⃣  REMOTE WORKERS (Heavy compute)"
echo "   # On remote server/cloud:"
echo "   export HIVE_ORCHESTRATOR_URL=http://YOUR_MAC_IP:8000"
echo "   docker-compose -f docker-compose.worker.yml up -d --scale worker=5"
echo "   - 5 heavy compute workers"
echo "   - 32 CPU + 32GB RAM each"
echo "   - GPU support"
echo ""

echo "5️⃣  KUBERNETES (Enterprise)"
echo "   kubectl apply -f k8s/"
echo "   - Full K8s deployment"
echo "   - Horizontal Pod Autoscaling"
echo "   - Production grade"
echo ""

echo "======================================"
echo ""

# Interactive selection
echo "What do you want to deploy?"
echo ""
echo "[1] Test locally (Mac, stops after)"
echo "[2] Deploy to cloud (production)"
echo "[3] Start training cluster"
echo "[4] Add remote workers"
echo "[5] Check what's already running"
echo "[0] Exit"
echo ""
read -p "Select option (0-5): " choice

case $choice in
  1)
    echo ""
    echo "🚀 Starting local test deployment..."
    docker-compose -f docker-compose.mac.yml up
    ;;
    
  2)
    echo ""
    echo "🚀 Deploying full stack to cloud..."
    echo ""
    read -p "Enter cloud server IP: " SERVER_IP
    
    if [ -z "$SERVER_IP" ]; then
      echo "❌ Server IP required"
      exit 1
    fi
    
    echo "Copying files to $SERVER_IP..."
    scp -r . root@$SERVER_IP:/opt/quetzalcore/
    
    echo "Starting services on remote server..."
    ssh root@$SERVER_IP << 'ENDSSH'
      cd /opt/quetzalcore
      docker-compose up -d
      echo "✅ Services started"
      docker-compose ps
ENDSSH
    
    echo ""
    echo "✅ Deployed to http://$SERVER_IP:8000"
    echo "   Dashboard: http://$SERVER_IP:3000"
    ;;
    
  3)
    echo ""
    echo "🚀 Starting training cluster..."
    docker-compose -f docker-compose.training.yml up -d
    echo ""
    echo "✅ Training cluster started"
    docker-compose -f docker-compose.training.yml ps
    echo ""
    echo "To scale runners:"
    echo "  docker-compose -f docker-compose.training.yml up -d --scale training-runner-1=5"
    ;;
    
  4)
    echo ""
    echo "🚀 Adding remote workers..."
    echo ""
    read -p "Enter orchestrator URL (e.g., http://192.168.1.100:8000): " ORCH_URL
    read -p "How many workers to spawn: " NUM_WORKERS
    
    if [ -z "$ORCH_URL" ] || [ -z "$NUM_WORKERS" ]; then
      echo "❌ Orchestrator URL and worker count required"
      exit 1
    fi
    
    export HIVE_ORCHESTRATOR_URL=$ORCH_URL
    docker-compose -f docker-compose.worker.yml up -d --scale worker=$NUM_WORKERS
    
    echo ""
    echo "✅ Started $NUM_WORKERS workers"
    docker-compose -f docker-compose.worker.yml ps
    ;;
    
  5)
    echo ""
    echo "📊 Current deployments:"
    echo ""
    
    echo "=== Docker Containers ==="
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""
    
    echo "=== Docker Compose Services ==="
    if [ -f docker-compose.yml ]; then
      docker-compose ps
    fi
    echo ""
    
    echo "=== Resource Usage ==="
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
    ;;
    
  0)
    echo "👋 Exited"
    exit 0
    ;;
    
  *)
    echo "❌ Invalid option"
    exit 1
    ;;
esac

echo ""
echo "======================================"
echo "🎉 DONE!"
echo ""
echo "Useful commands:"
echo "  docker-compose logs -f              # View logs"
echo "  docker-compose ps                   # Check status"
echo "  docker-compose down                 # Stop all"
echo "  docker-compose up -d --scale worker=10  # Scale workers"
echo ""
echo "API Endpoints:"
echo "  http://localhost:8000/api/health    # Health check"
echo "  http://localhost:8000/api/mining/*  # Mining APIs"
echo "  http://localhost:9000/status        # Autoscaler status"
echo ""
