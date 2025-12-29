#!/bin/bash
# AIOSC Platform - Quick Deployment

echo "🚀 Deploying AIOSC Platform..."
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
docker exec hive-backend-1 pip install -q pyjwt bcrypt python-multipart || echo "Dependencies may already be installed"

# Copy platform code
echo "📁 Copying platform code..."
docker cp /Users/xavasena/hive/backend/aiosc_platform.py hive-backend-1:/workspace/

# Start AIOSC platform (background)
echo "🌟 Starting AIOSC platform on port 8001..."
docker exec -d hive-backend-1 bash -c 'cd /workspace && python3 aiosc_platform.py > aiosc.log 2>&1'

sleep 3

# Test health
echo "🔍 Testing platform..."
if curl -sf http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ AIOSC Platform is live!"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  AIOSC PLATFORM READY"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📊 API Endpoints:"
    echo "  Health:        http://localhost:8001/health"
    echo "  Docs:          http://localhost:8001/docs"
    echo "  Register:      POST /auth/register"
    echo "  Login:         POST /auth/login"
    echo "  Capabilities:  GET /capabilities"
    echo "  Execute:       POST /execute/{capability}"
    echo ""
    echo "🧪 Quick Test:"
    echo '  curl -X POST http://localhost:8001/auth/register \\'
    echo '    -H "Content-Type: application/json" \\'
    echo '    -d '"'"'{"email":"test@example.com","password":"test123","tier":"creator"}'"'"
    echo ""
    echo "📚 Full docs: See AIOSC_ARCHITECTURE.md"
    echo ""
else
    echo "❌ Platform failed to start. Check logs:"
    echo "   docker exec hive-backend-1 tail -20 /workspace/aiosc.log"
fi
