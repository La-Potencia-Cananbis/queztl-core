#!/bin/bash
# Stop QuetzalCore services

echo "🛑 Stopping QuetzalCore..."

# Stop backend
if [ -f .backend.pid ]; then
    BACKEND_PID=$(cat .backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "   Stopping backend (PID: $BACKEND_PID)"
        kill $BACKEND_PID 2>/dev/null
    fi
    rm .backend.pid
fi

# Stop frontend
if [ -f .frontend.pid ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "   Stopping frontend (PID: $FRONTEND_PID)"
        kill $FRONTEND_PID 2>/dev/null
    fi
    rm .frontend.pid
fi

# Kill any remaining processes on ports
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:8080 | xargs kill -9 2>/dev/null

echo "✅ QuetzalCore stopped"
