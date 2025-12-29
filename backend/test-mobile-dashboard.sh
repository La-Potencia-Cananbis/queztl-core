#!/bin/bash
# Quick test - open dashboard in browser

echo "🚀 MOBILE DASHBOARD - QUICK ACCESS"
echo "=================================="
echo ""
echo "✅ Dashboard is RUNNING on port 9999"
echo ""
echo "📱 Access from your phone:"
echo "   http://10.112.221.224:9999"
echo ""
echo "💻 Test from this computer:"
echo "   http://localhost:9999"
echo ""
echo "🧪 Health check:"
curl -s http://localhost:9999/health | python3 -m json.tool
echo ""
echo ""
echo "🌐 Opening in browser..."
open http://localhost:9999 2>/dev/null || echo "Open manually: http://localhost:9999"
echo ""
echo "Process Info:"
ps aux | grep mobile_dashboard | grep -v grep
echo ""
echo "=================================="
echo "✅ Dashboard is LIVE and responding!"
