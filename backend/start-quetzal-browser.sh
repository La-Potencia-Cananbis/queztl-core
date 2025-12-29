#!/bin/bash
# QuetzalCore Native Browser Launcher
# Starts backend with QP protocol + opens native browser

echo "🚀 QuetzalCore Native Browser - Startup"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if backend is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${YELLOW}⚠️  Backend already running on port 8000${NC}"
    echo "   Stopping existing process..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    sleep 2
fi

# Start backend with QP protocol
echo -e "${BLUE}📡 Starting FastAPI backend with QP Protocol...${NC}"
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Start backend in background
.venv/bin/python -m uvicorn backend.main:app --reload --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!

echo "   Backend PID: $BACKEND_PID"
echo "   Waiting for backend to start..."

# Wait for backend to be ready
for i in {1..30}; do
    if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend ready!${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${YELLOW}⚠️  Backend taking longer than expected...${NC}"
        echo "   Check backend.log for errors"
    fi
    sleep 1
done

# Display endpoints
echo ""
echo "🌐 Available Endpoints:"
echo "   REST API:       http://localhost:8000"
echo "   API Docs:       http://localhost:8000/docs"
echo "   Health:         http://localhost:8000/api/health"
echo "   WebSocket:      ws://localhost:8000/ws/metrics"
echo -e "   ${GREEN}QP Protocol:    ws://localhost:8000/ws/qp${NC} ⭐"
echo ""

# Start frontend server
echo -e "${BLUE}🌐 Starting frontend server...${NC}"
cd frontend
python3 -m http.server 8080 > ../frontend.log 2>&1 &
FRONTEND_PID=$!

echo "   Frontend PID: $FRONTEND_PID"
sleep 2

# Check if frontend started
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${GREEN}✅ Frontend ready!${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend may not have started${NC}"
    echo "   Check frontend.log for errors"
fi

cd ..

echo ""
echo "🎨 Frontend URLs:"
echo "   Native Browser: http://localhost:8080/quetzal-browser.html"
echo "   QP Demo:        http://localhost:8080/queztl_demo.html"
echo ""

# Save PIDs for cleanup
echo "$BACKEND_PID" > .backend.pid
echo "$FRONTEND_PID" > .frontend.pid

# Open browser
echo -e "${GREEN}🚀 Opening QuetzalCore Native Browser...${NC}"
sleep 1

# Detect OS and open browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "http://localhost:8080/quetzal-browser.html"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "http://localhost:8080/quetzal-browser.html" 2>/dev/null || \
    sensible-browser "http://localhost:8080/quetzal-browser.html" 2>/dev/null
else
    echo "   Please open: http://localhost:8080/quetzal-browser.html"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ QuetzalCore is running!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Usage:"
echo "   1. Browser should open automatically"
echo "   2. Default URL: qp://localhost:8000/ws/qp"
echo "   3. Click 'Go' to connect via QP Protocol"
echo "   4. Try GPU or GIS operations from sidebar"
echo ""
echo "🛑 To stop:"
echo "   ./stop-quetzal.sh"
echo ""
echo "📚 Documentation:"
echo "   QUETZAL_BROWSER_GUIDE.md"
echo "   QUEZTL_PROTOCOL.md"
echo ""
echo "🎯 Quick Test:"
echo "   Click 'GPU Pool Status' in sidebar"
echo "   Or: 'Parallel MatMul' for benchmark"
echo ""
echo "Dale! 🚀"
echo ""

# Keep script running and show logs
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📜 Showing backend logs (Ctrl+C to exit):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
tail -f backend.log
