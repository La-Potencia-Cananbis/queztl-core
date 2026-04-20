#!/bin/bash
# AIOSC Platform - Quick Deployment (repo-relative)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONTAINER_NAME="${AIOSC_CONTAINER:-hive-backend-1}"
CONTAINER_WORKDIR="${AIOSC_CONTAINER_WORKDIR:-/workspace}"
LOCAL_PLATFORM_FILE="$REPO_ROOT/backend/aiosc_platform.py"

echo "🚀 Deploying AIOSC Platform..."
echo ""
echo "📂 Repo root: $REPO_ROOT"
echo "🐳 Container: $CONTAINER_NAME"
echo "📦 Container workdir: $CONTAINER_WORKDIR"
echo ""

if ! command -v docker >/dev/null 2>&1; then
    echo "❌ Docker is required for this deploy script"
    exit 1
fi

if [ ! -f "$LOCAL_PLATFORM_FILE" ]; then
    echo "❌ Missing local platform file: $LOCAL_PLATFORM_FILE"
    exit 1
fi

if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER_NAME"; then
    echo "❌ Container '$CONTAINER_NAME' is not running"
    echo "   Set AIOSC_CONTAINER to your backend container name if different."
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
docker exec "$CONTAINER_NAME" pip install -q pyjwt bcrypt python-multipart || echo "Dependencies may already be installed"

# Copy platform code
echo "📁 Copying platform code..."
docker cp "$LOCAL_PLATFORM_FILE" "$CONTAINER_NAME:$CONTAINER_WORKDIR/aiosc_platform.py"

# Start AIOSC platform (background)
echo "🌟 Starting AIOSC platform on port 8001..."
docker exec -d "$CONTAINER_NAME" bash -lc "cd '$CONTAINER_WORKDIR' && python3 aiosc_platform.py > aiosc.log 2>&1"

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
    echo '    -d '\''{"email":"test@example.com","password":"test123","tier":"creator"}'\'''
    echo ""
    echo "📚 Full docs: See backend/AIOSC_ARCHITECTURE.md"
    echo ""
else
    echo "❌ Platform failed to start. Check logs:"
    echo "   docker exec $CONTAINER_NAME tail -20 $CONTAINER_WORKDIR/aiosc.log"
fi
