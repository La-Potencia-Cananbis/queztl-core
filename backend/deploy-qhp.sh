#!/bin/bash
# QHP Protocol - Complete Deployment Script

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}"
cat << 'EOF'
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     ⚡ QHP - QUEZTL HYBRID PROTOCOL™                    ║
║        Quantized Action Packets™ (QAPs)                 ║
║                                                          ║
║     "Quantized. Hybrid. Powerful."                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${YELLOW}Starting QHP Protocol System...${NC}\n"

# Step 1: Ensure lightweight orchestrator is running
echo -e "${GREEN}[1/5] Starting Lightweight Orchestrator...${NC}"
docker-compose -f docker-compose.mac.yml up -d
sleep 3

# Step 2: Deploy QHP server
echo -e "${GREEN}[2/5] Deploying QHP Protocol Server...${NC}"
docker cp backend/qhp_server.py hive-orchestrator-1:/workspace/
docker cp backend/qhp_monitor.py hive-orchestrator-1:/workspace/
docker cp backend/qhp_ml_optimizer.py hive-orchestrator-1:/workspace/

# Kill any existing QHP servers
docker exec hive-orchestrator-1 bash -c 'ps aux | grep qhp | grep -v grep | awk "{print \$2}" | xargs kill -9 2>/dev/null || true'
sleep 2

# Start QHP server
docker exec -d hive-orchestrator-1 bash -c 'cd /workspace && python3 qhp_server.py > qhp.log 2>&1 &'
sleep 3

# Step 3: Check QHP server status
echo -e "${GREEN}[3/5] Checking QHP Server Status...${NC}"
if docker exec hive-orchestrator-1 cat /workspace/qhp.log 2>/dev/null | grep -q "Server started"; then
    echo -e "${GREEN}✅ QHP Server is running!${NC}"
else
    echo -e "${YELLOW}⚠️  QHP Server may not have started. Check logs:${NC}"
    echo "   docker exec hive-orchestrator-1 cat /workspace/qhp.log"
fi

# Step 4: Show system status
echo -e "\n${GREEN}[4/5] System Status:${NC}"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Step 5: Show resource usage
echo -e "\n${GREEN}[5/5] Resource Usage:${NC}"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo -e "\n${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                QHP PROTOCOL DEPLOYED!                   ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}\n"

echo -e "${YELLOW}🎯 QHP Protocol Services:${NC}"
echo "   • Orchestrator API:    http://localhost:8000"
echo "   • QHP WebSocket:       ws://localhost:9999"
echo "   • Demo Interface:      file://$(pwd)/backend/qhp_demo.html"
echo ""

echo -e "${YELLOW}📊 QHP Commands:${NC}"
echo "   • Status:              ./resource-manager.sh status"
echo "   • View QHP logs:       docker exec hive-orchestrator-1 tail -f /workspace/qhp.log"
echo "   • Stress test:         python3 quick-stress-test.py"
echo "   • Stop all:            docker-compose -f docker-compose.mac.yml down"
echo ""

echo -e "${YELLOW}💰 Legal Filing:${NC}"
echo "   1. File trademarks:    cat USPTO_TRADEMARK_FILING.md"
echo "   2. File patent:        cat USPTO_PATENT_FILING.md"
echo "   3. Total cost:         \$900 (\$750 + \$150)"
echo ""

echo -e "${YELLOW}📖 Documentation:${NC}"
echo "   • Protocol spec:       cat QHP_PROTOCOL_SPECIFICATION.md"
echo "   • Registration:        cat QHP_REGISTRATION.md"
echo "   • Distributed arch:    cat DISTRIBUTED_ARCHITECTURE.md"
echo ""

echo -e "${GREEN}✅ QHP Protocol is live! Start building with QAPs! 🚀${NC}\n"
