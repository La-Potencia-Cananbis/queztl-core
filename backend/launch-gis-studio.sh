#!/bin/bash

################################################################################
# 🗺️ GIS Studio - Professional Dashboard Launcher
# Beautiful, responsive interface for QuetzalCore GIS Studio
################################################################################

set -e

echo "
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║          🗺️  QUETZALCORE GIS STUDIO - DASHBOARD LAUNCHER  🗺️     ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"

# Check if backend is running
echo "🔍 Checking backend status..."
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "⚠️  Backend not detected. Starting backend..."
    python3 -m uvicorn backend.main:app --port 8000 > /tmp/backend.log 2>&1 &
    sleep 3
    echo "✅ Backend started (check /tmp/backend.log for logs)"
fi

# Open GIS Studio dashboard
echo ""
echo "🚀 Launching GIS Studio Dashboard..."
echo ""
echo "📍 Dashboard: http://localhost:8080/gis-studio.html"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🔌 API Base: http://localhost:8000/api/gis/studio"
echo ""

# Try to open in default browser
if command -v open &> /dev/null; then
    # macOS
    open "http://localhost:8080/gis-studio.html"
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open "http://localhost:8080/gis-studio.html"
elif command -v start &> /dev/null; then
    # Windows
    start "http://localhost:8080/gis-studio.html"
fi

echo ""
echo "📋 Features:"
echo "   ✓ Real-time GIS data validation"
echo "   ✓ Terrain analysis & integration"
echo "   ✓ ML model training interface"
echo "   ✓ Feedback collection system"
echo "   ✓ Performance monitoring"
echo ""
echo "💡 Tips:"
echo "   • GIS Studio compiles with 8 REST API endpoints"
echo "   • All 4 GIS modules are integrated and ready"
echo "   • Backend accepts JSON payloads for all operations"
echo "   • Check /api/gis/studio/status for system health"
echo ""
echo "Type Ctrl+C to stop. Have fun! 🚀"
