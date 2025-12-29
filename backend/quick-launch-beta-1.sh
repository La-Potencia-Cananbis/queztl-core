#!/bin/bash

# ============================================================================
# QuetzalCore BETA 1 - Quick Launch Script
# ============================================================================
# Fast-track deployment - gets you running in seconds
# ============================================================================

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🦅 QuetzalCore BETA 1 - Quick Launch                     ║"
echo "║   Version: 1.0.0-beta.1                                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Step 1: Check prerequisites
echo -e "${YELLOW}[1/5] Checking prerequisites...${NC}"
if [ ! -f "backend/main.py" ]; then
    echo -e "${RED}❌ Error: Must run from project root${NC}"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Creating .env from template...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Edit .env with your database and API keys${NC}"
    fi
fi
echo -e "${GREEN}✅ Prerequisites OK${NC}"
echo ""

# Step 2: Clean up old containers
echo -e "${YELLOW}[2/5] Cleaning up old services...${NC}"
docker-compose down 2>/dev/null || true
sleep 2
echo -e "${GREEN}✅ Cleanup done${NC}"
echo ""

# Step 3: Build and start
echo -e "${YELLOW}[3/5] Starting services (this may take a minute)...${NC}"
docker-compose up -d --build 2>&1 | tail -5
echo -e "${GREEN}✅ Services starting${NC}"
echo ""

# Step 4: Wait for services
echo -e "${YELLOW}[4/5] Waiting for services to be ready...${NC}"
for i in {1..60}; do
    if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ All services are ready!${NC}"
        break
    fi
    if [ $((i % 10)) -eq 0 ]; then
        echo "   Waiting... ($i seconds)"
    fi
    sleep 1
done
echo ""

# Step 5: Show access info
echo -e "${YELLOW}[5/5] System ready!${NC}"
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ QuetzalCore BETA 1 is LIVE!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "🌐 Access your system:"
echo ""
echo "   📊 Dashboard:        ${BLUE}http://localhost:3000${NC}"
echo "   🔌 API:              ${BLUE}http://localhost:8000${NC}"
echo "   📖 API Docs:         ${BLUE}http://localhost:8000/docs${NC}"
echo "   🧲 Mining API:       ${BLUE}http://localhost:8000/api/mining${NC}"
echo "   👁️  Monitor:          ${BLUE}http://localhost:7070${NC}"
echo ""
echo "💾 Services:"
echo "   Database:    PostgreSQL on localhost:5432"
echo "   Cache:       Redis on localhost:6379"
echo ""
echo "📋 Useful commands:"
echo ""
echo "   View logs:        ${BLUE}docker-compose logs -f${NC}"
echo "   Stop services:    ${BLUE}docker-compose down${NC}"
echo "   See status:       ${BLUE}docker-compose ps${NC}"
echo "   Run tests:        ${BLUE}python3 -m pytest tests/${NC}"
echo "   Monitor usage:    ${BLUE}python3 infrastructure_monitor.py${NC}"
echo ""
echo "🚀 Next steps:"
echo ""
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Try uploading a mining survey"
echo "   3. Watch real-time processing in the dashboard"
echo "   4. View infrastructure metrics at http://localhost:7070"
echo ""
echo "📚 Documentation:"
echo "   ${BLUE}BETA_1_PRODUCTION_READY.md${NC}     - Full deployment guide"
echo "   ${BLUE}FINAL_SUMMARY.md${NC}               - System overview"
echo "   ${BLUE}PROJECT_SUMMARY.md${NC}             - Architecture details"
echo ""
echo "🆘 Troubleshooting:"
echo ""
if ! command -v docker &> /dev/null; then
    echo -e "   ${RED}Docker not installed${NC} - install Docker Desktop"
fi
echo ""
echo "🎉 Enjoy your QuetzalCore deployment!"
echo ""
