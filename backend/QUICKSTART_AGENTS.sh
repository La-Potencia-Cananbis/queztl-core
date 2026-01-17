#!/bin/bash
# QUEZTL AGENT SYSTEM - QUICK START
# One script to rule them all

set -e

echo "=============================================="
echo "🚀 QUEZTL AGENT SYSTEM - QUICK START"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "backend/queztl_agents.py" ]; then
    echo -e "${RED}Error: Run this from the queztl-core root directory${NC}"
    exit 1
fi

# Step 1: Python Dependencies
echo -e "${YELLOW}[1/4] Installing Python dependencies...${NC}"
echo "This may take a few minutes..."
pip3 install -r backend/requirements.txt --quiet --disable-pip-version-check || {
    echo -e "${RED}Warning: Some packages may have failed. Continuing...${NC}"
}
echo -e "${GREEN}✓ Python dependencies installed${NC}"
echo ""

# Step 2: Start Docker (optional, for full stack)
echo -e "${YELLOW}[2/4] Checking Docker...${NC}"
if ! docker ps &> /dev/null; then
    echo "Docker daemon not running. Opening Docker Desktop..."
    open -a Docker
    echo "Waiting 15 seconds for Docker to start..."
    sleep 15
    
    # Check again
    if docker ps &> /dev/null; then
        echo -e "${GREEN}✓ Docker is running${NC}"
    else
        echo -e "${YELLOW}⚠ Docker not available. Agents will run in standalone mode.${NC}"
    fi
else
    echo -e "${GREEN}✓ Docker is running${NC}"
fi
echo ""

# Step 3: Run diagnostic
echo -e "${YELLOW}[3/4] Running system diagnostic...${NC}"
python3 backend/LEVEL1_DIAGNOSTIC.py
DIAGNOSTIC_EXIT=$?
echo ""

# Step 4: Launch options
if [ $DIAGNOSTIC_EXIT -eq 0 ]; then
    echo -e "${GREEN}=============================================="
    echo "✅ ALL SYSTEMS GO!"
    echo "=============================================="
    echo -e "${NC}"
    echo "What would you like to do?"
    echo ""
    echo "  1) Run agent teaching demo (recommended first time)"
    echo "  2) Spawn a single trainer agent"
    echo "  3) Start training dashboard (web UI)"
    echo "  4) Start full Docker stack (backend + frontend + DB)"
    echo "  5) Exit"
    echo ""
    read -p "Enter choice [1-5]: " choice
    
    case $choice in
        1)
            echo ""
            echo "🎓 Starting agent teaching demo..."
            python3 backend/queztl_agents.py --demo
            ;;
        2)
            echo ""
            echo "🤖 Spawning trainer agent..."
            python3 backend/queztl_agents.py --spawn trainer
            ;;
        3)
            echo ""
            echo "📊 Starting dashboard on http://localhost:5000..."
            python3 backend/training_dashboard.py
            ;;
        4)
            echo ""
            echo "🐳 Starting full Docker stack..."
            cd infra
            docker-compose up -d
            echo ""
            echo "Services starting:"
            echo "  - Backend API: http://localhost:8000"
            echo "  - Dashboard:   http://localhost:3000"
            echo "  - PostgreSQL:  localhost:5432"
            echo "  - Redis:       localhost:6379"
            ;;
        5)
            echo "Goodbye! 👋"
            exit 0
            ;;
        *)
            echo "Invalid choice. Exiting."
            exit 1
            ;;
    esac
else
    echo -e "${YELLOW}=============================================="
    echo "⚠️  SETUP INCOMPLETE"
    echo "=============================================="
    echo -e "${NC}"
    echo "Some dependencies are missing. To install manually:"
    echo ""
    echo "  pip3 install -r backend/requirements.txt"
    echo ""
    echo "Then run this script again, or run agents directly:"
    echo ""
    echo "  python3 backend/queztl_agents.py --demo"
    echo ""
fi
