#!/bin/bash

set -e

echo "🚀 Deploying Queztl Protocol Server..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if backend container is running
if ! docker ps | grep -q hive-backend; then
    echo "❌ Backend container not running. Starting AIOSC platform first..."
    ./deploy-aiosc.sh
fi

echo -e "${YELLOW}📦 Installing Python WebSocket library...${NC}"
docker exec hive-backend-1 pip install websockets > /dev/null 2>&1 || true

echo -e "${YELLOW}📁 Copying Queztl Protocol server to container...${NC}"
docker cp backend/queztl_server.py hive-backend-1:/workspace/

echo -e "${YELLOW}🔌 Starting Queztl Protocol server (port 9999)...${NC}"
docker exec -d hive-backend-1 bash -c 'cd /workspace && python3 queztl_server.py > queztl.log 2>&1 &'

# Wait for server to start
sleep 3

# Check if server is running
if docker exec hive-backend-1 ps aux | grep -q "[q]ueztl_server.py"; then
    echo -e "${GREEN}✅ Queztl Protocol server is running!${NC}"
else
    echo "⚠️  Server may not have started. Checking logs..."
    docker exec hive-backend-1 cat /workspace/queztl.log || echo "No logs yet"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  ⚡ QUEZTL PROTOCOL SERVER DEPLOYED"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "WebSocket Endpoint:  ws://localhost:9999"
echo "Demo Page:          file://${PWD}/backend/queztl_demo.html"
echo ""
echo "To test the protocol:"
echo "  1. Open backend/queztl_demo.html in your browser"
echo "  2. Click 'Connect to Server'"
echo "  3. Try executing any capability"
echo ""
echo "To view server logs:"
echo "  docker exec hive-backend-1 tail -f /workspace/queztl.log"
echo ""
echo "To test from command line (requires websocat):"
echo "  brew install websocat"
echo "  echo -n 'test' | websocat ws://localhost:9999"
echo ""
echo "═══════════════════════════════════════════════════════"
