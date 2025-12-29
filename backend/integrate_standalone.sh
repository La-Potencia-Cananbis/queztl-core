#!/bin/bash
# Integrate Standalone Endpoints to main.py
# Run this to add standalone mode to your backend

echo "🔧 INTEGRATING STANDALONE MODE"
echo "=============================="
echo ""

MAIN_FILE="backend/main.py"

if [ ! -f "$MAIN_FILE" ]; then
    echo "❌ main.py not found at $MAIN_FILE"
    exit 1
fi

# Check if already integrated
if grep -q "from backend.standalone_endpoints" "$MAIN_FILE"; then
    echo "✅ Standalone endpoints already integrated!"
    echo ""
    echo "Testing connection..."
    export XAVASENA_KEY="b8f3d9e7a6c5f1d2e4a9b7c6d8f3e1a2b4c7d9e6f8a1c3d5e7f9a2b4c6d8e1f3"
    curl -s "https://queztl-core-backend.onrender.com/api/standalone/status" \
      -H "X-Owner-Key: $XAVASENA_KEY"
    exit 0
fi

echo "📝 Adding standalone imports to main.py..."

# Backup first
cp "$MAIN_FILE" "${MAIN_FILE}.backup.$(date +%s)"

# Find the line with other router imports
IMPORT_LINE=$(grep -n "from backend.*import router" "$MAIN_FILE" | tail -1 | cut -d: -f1)

if [ -z "$IMPORT_LINE" ]; then
    echo "⚠️  Could not find router imports. Adding at top of file..."
    # Add after the other imports
    sed -i '' '1a\
from backend.standalone_endpoints import router as standalone_router
' "$MAIN_FILE"
else
    echo "✅ Found router imports at line $IMPORT_LINE"
    # Add after that line
    sed -i '' "${IMPORT_LINE}a\\
from backend.standalone_endpoints import router as standalone_router
" "$MAIN_FILE"
fi

# Find where routers are included
INCLUDE_LINE=$(grep -n "app.include_router" "$MAIN_FILE" | tail -1 | cut -d: -f1)

if [ -z "$INCLUDE_LINE" ]; then
    echo "⚠️  Could not find include_router calls"
else
    echo "✅ Found include_router at line $INCLUDE_LINE"
    # Add after that line
    sed -i '' "${INCLUDE_LINE}a\\
app.include_router(standalone_router)
" "$MAIN_FILE"
fi

echo ""
echo "✅ Integration complete!"
echo ""
echo "Now commit and push:"
echo "  git add backend/main.py"
echo "  git commit -m '🔧 Integrate standalone endpoints'"
echo "  git push origin main"
echo ""
echo "Then wait 30s for Render to deploy and test with:"
echo "  ./test_standalone.sh"
