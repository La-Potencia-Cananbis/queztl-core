#!/bin/bash
# QuetzalCore Diagnostic Script - Check all routing and systems

echo "🔍 QuetzalCore System Diagnostic"
echo "=================================="
echo ""

# Check if backend is running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ Backend is running on port 8000"
    BACKEND_RUNNING=1
else
    echo "❌ Backend is NOT running on port 8000"
    echo "   Starting backend for testing..."
    BACKEND_RUNNING=0
    
    # Start backend
    cd "$(dirname "$0")"
    .venv/bin/python -m uvicorn backend.main:app --port 8000 > /tmp/diagnostic_backend.log 2>&1 &
    BACKEND_PID=$!
    echo "   Backend PID: $BACKEND_PID"
    
    # Wait for startup
    echo "   Waiting for backend to start..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
            echo "   ✅ Backend started successfully"
            BACKEND_RUNNING=1
            break
        fi
        sleep 1
    done
    
    if [ $BACKEND_RUNNING -eq 0 ]; then
        echo "   ❌ Backend failed to start"
        echo "   Check /tmp/diagnostic_backend.log for errors"
        exit 1
    fi
fi

echo ""
echo "📊 Testing Core Endpoints"
echo "-------------------------"

# Test health
echo -n "Health check... "
if curl -s http://localhost:8000/api/health | grep -q "healthy"; then
    echo "✅"
else
    echo "❌"
fi

# Test root
echo -n "Root endpoint... "
if curl -s http://localhost:8000/ | grep -q "QuetzalCore"; then
    echo "✅"
else
    echo "❌"
fi

# Test API docs
echo -n "API documentation... "
if curl -s http://localhost:8000/docs | grep -q "swagger"; then
    echo "✅"
else
    echo "❌"
fi

echo ""
echo "🚀 Testing GPU Operations"
echo "-------------------------"

# Test GPU status
echo -n "GPU pool status... "
if curl -s http://localhost:8000/api/gpu/parallel/status | grep -q "pool_status"; then
    echo "✅"
else
    echo "❌"
fi

# Test GPU matmul
echo -n "GPU parallel matmul... "
if curl -s -X POST http://localhost:8000/api/gpu/parallel/matmul \
    -H "Content-Type: application/json" \
    -d '{"size": 128, "num_units": 2}' | grep -q "result"; then
    echo "✅"
else
    echo "❌"
fi

echo ""
echo "🌐 Testing Network & System"
echo "---------------------------"

# Test network status
echo -n "Network status... "
if curl -s http://localhost:8000/api/v1.2/network/status | grep -q "status"; then
    echo "✅"
else
    echo "❌"
fi

# Test autoscaler
echo -n "Autoscaler status... "
if curl -s http://localhost:8000/api/v1.2/autoscaler/status | grep -q "status"; then
    echo "✅"
else
    echo "❌"
fi

echo ""
echo "🔌 Testing WebSocket Endpoints"
echo "-------------------------------"

# Check if websocket endpoints are registered
echo -n "WebSocket /ws/metrics... "
if curl -s http://localhost:8000/openapi.json | grep -q '"/ws/metrics"'; then
    echo "✅"
else
    echo "❌"
fi

echo -n "WebSocket /ws/qp... "
if curl -s http://localhost:8000/openapi.json | grep -q '"/ws/qp"'; then
    echo "✅"
else
    echo "❌"
fi

echo ""
echo "📋 Registered Routes Summary"
echo "----------------------------"

# Get route count
ROUTE_COUNT=$(curl -s http://localhost:8000/openapi.json | grep -o '"path"' | wc -l)
echo "Total routes: $ROUTE_COUNT"

# Show some key routes
echo ""
echo "Key GPU routes:"
curl -s http://localhost:8000/openapi.json | grep -o '"/api/gpu/[^"]*"' | head -5

echo ""
echo "Key GIS routes (if any):"
curl -s http://localhost:8000/openapi.json | grep -o '"/api/gis/[^"]*"' | head -5 || echo "  (None found via REST - use QP protocol)"

echo ""
echo "Key WebSocket routes:"
curl -s http://localhost:8000/openapi.json | grep -o '"/ws/[^"]*"'

echo ""
echo "=================================="
echo "📊 Diagnostic Complete"
echo "=================================="

# Cleanup if we started the backend
if [ -n "$BACKEND_PID" ]; then
    echo ""
    echo "Stopping test backend (PID: $BACKEND_PID)..."
    kill $BACKEND_PID 2>/dev/null
    echo "✅ Cleanup complete"
fi

echo ""
echo "💡 Tip: Run './test-api-routes.py' for detailed route testing"
echo "💡 Tip: Run './start-quetzal-browser.sh' to launch full system"
