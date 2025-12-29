#!/bin/bash

set -e

echo "🤖 Deploying Queztl Protocol with ML Auto-Optimization..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if backend container is running
if ! docker ps | grep -q hive-backend; then
    echo "❌ Backend container not running. Starting AIOSC platform first..."
    ./deploy-aiosc.sh
fi

echo -e "${YELLOW}📦 Installing required packages...${NC}"
docker exec hive-backend-1 pip install websockets numpy scikit-learn joblib psutil -q > /dev/null 2>&1 || true

echo -e "${YELLOW}📁 Copying protocol files to container...${NC}"
docker cp backend/queztl_server.py hive-backend-1:/workspace/
docker cp backend/queztl_monitor.py hive-backend-1:/workspace/
docker cp backend/queztl_ml_optimizer.py hive-backend-1:/workspace/
docker cp backend/queztl_auto_optimizer.py hive-backend-1:/workspace/

echo -e "${YELLOW}🔌 Starting Queztl Protocol server with monitoring...${NC}"
docker exec -d hive-backend-1 bash -c 'cd /workspace && python3 queztl_server.py > queztl.log 2>&1 &'

# Wait for server to start
sleep 3

echo -e "${YELLOW}🤖 Starting Auto-Optimizer daemon...${NC}"
docker exec -d hive-backend-1 bash -c 'cd /workspace && python3 queztl_auto_optimizer.py > optimizer.log 2>&1 &'

sleep 2

# Check if services are running
if docker exec hive-backend-1 ps aux | grep -q "[q]ueztl_server.py"; then
    echo -e "${GREEN}✅ Queztl Protocol server is running!${NC}"
else
    echo "⚠️  Server may not have started. Checking logs..."
    docker exec hive-backend-1 cat /workspace/queztl.log || echo "No logs yet"
fi

if docker exec hive-backend-1 ps aux | grep -q "[q]ueztl_auto_optimizer.py"; then
    echo -e "${GREEN}✅ Auto-optimizer daemon is running!${NC}"
else
    echo "⚠️  Optimizer may not have started. Checking logs..."
    docker exec hive-backend-1 cat /workspace/optimizer.log || echo "No logs yet"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  ⚡ QUEZTL PROTOCOL WITH ML AUTO-OPTIMIZATION DEPLOYED"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "${BLUE}Protocol Server:${NC}       ws://localhost:9999"
echo "${BLUE}Demo Page:${NC}             file://${PWD}/backend/queztl_demo.html"
echo "${BLUE}Auto-Optimizer:${NC}        Running in background"
echo ""
echo "${BLUE}Features Enabled:${NC}"
echo "  ✅ Real-time protocol monitoring"
echo "  ✅ Anomaly detection"
echo "  ✅ ML-driven optimization"
echo "  ✅ Auto-parameter tuning"
echo "  ✅ Performance prediction"
echo ""
echo "${BLUE}View Logs:${NC}"
echo "  Protocol Server:  docker exec hive-backend-1 tail -f /workspace/queztl.log"
echo "  Auto-Optimizer:   docker exec hive-backend-1 tail -f /workspace/optimizer.log"
echo ""
echo "${BLUE}Manual Commands:${NC}"
echo "  Monitor Stats:    docker exec hive-backend-1 python3 /workspace/queztl_monitor.py --stats"
echo "  Analyze Patterns: docker exec hive-backend-1 python3 /workspace/queztl_monitor.py --analyze"
echo "  Suggest Optimizations: docker exec hive-backend-1 python3 /workspace/queztl_monitor.py --suggest"
echo "  Train ML Models:  docker exec hive-backend-1 python3 /workspace/queztl_ml_optimizer.py --train"
echo "  Optimize Protocol: docker exec hive-backend-1 python3 /workspace/queztl_ml_optimizer.py --optimize"
echo "  Generate Report:  docker exec hive-backend-1 python3 /workspace/queztl_ml_optimizer.py --report"
echo ""
echo "═══════════════════════════════════════════════════════════"
