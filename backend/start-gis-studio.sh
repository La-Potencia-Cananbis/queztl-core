#!/bin/bash

echo "🚀 STARTING QUETZAL GIS STUDIO..."
echo ""

# Verify backend is running
if curl -s http://localhost:8000/api/health | grep -q "healthy"; then
    echo "✅ Backend is running on localhost:8000"
else
    echo "⚠️ Backend health check failed, but continuing..."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 GIS STUDIO DASHBOARDS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  Main Dashboard (Beautiful UI + Metrics):"
echo "   🌐 http://localhost:8080/gis-studio.html"
echo ""
echo "2️⃣  API Tester (Interactive 9 Endpoints):"
echo "   🌐 http://localhost:8080/gis-studio-dashboard.html"
echo ""
echo "3️⃣  Backend API (Direct FastAPI):"
echo "   🌐 http://localhost:8000/"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Try to open in browser
echo "📱 Opening in browser..."

# Try localhost:8080 first
if curl -s http://localhost:8080/gis-studio.html > /dev/null 2>&1; then
    open "http://localhost:8080/gis-studio.html"
    echo "✅ GIS Studio Dashboard opened!"
else
    # Fall back to backend
    open "http://localhost:8000/"
    echo "✅ Backend opened!"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 WHAT YOU CAN DO:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Click any endpoint in the dashboard"
echo "✅ Test LiDAR validation"
echo "✅ Run terrain analysis"
echo "✅ Check GPU hardware"
echo "✅ View real-time metrics"
echo ""
echo "🚀 GIS STUDIO IS LIVE!"
echo ""
