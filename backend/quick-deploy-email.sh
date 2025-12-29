#!/bin/bash
# 🚀 Queztl Email System - Quick Deploy
# Deploy everything to get funding ASAP

set -e

echo "=================================="
echo "🚀 QUEZTL EMAIL QUICK DEPLOY"
echo "=================================="
echo ""

# Check if backend is running
echo "1️⃣  Checking backend..."
if lsof -ti:8001 > /dev/null 2>&1; then
    echo "   ✅ Backend already running on port 8001"
else
    echo "   ⚠️  Backend not running. Starting now..."
    .venv/bin/python backend/email_service.py &
    BACKEND_PID=$!
    echo "   ✅ Backend started (PID: $BACKEND_PID)"
    sleep 2
fi

# Test backend
echo ""
echo "2️⃣  Testing backend API..."
if curl -s http://localhost:8001/ > /dev/null 2>&1; then
    echo "   ✅ Backend is responding"
else
    echo "   ❌ Backend not responding. Check logs."
    exit 1
fi

# Copy landing page to netlify directory
echo ""
echo "3️⃣  Preparing landing page for Netlify..."
mkdir -p netlify
cp email-landing.html netlify/index.html
echo "   ✅ Landing page ready in netlify/"

# Show deployment instructions
echo ""
echo "=================================="
echo "✅ SYSTEM READY FOR DEPLOYMENT"
echo "=================================="
echo ""
echo "Next steps:"
echo ""
echo "📧 Deploy Landing Page:"
echo "   cd netlify && netlify deploy --prod"
echo "   → This will be your public-facing site"
echo ""
echo "💻 Deploy Email App:"
echo "   cd email-app"
echo "   npm install"
echo "   npm run build"
echo "   netlify deploy --prod --dir=out"
echo "   → This will be your web app"
echo ""
echo "📤 Start Investor Outreach:"
echo "   python3 investor_outreach.py          # Test first"
echo "   python3 investor_outreach.py --live   # Send for real"
echo ""
echo "🎯 What investors will see:"
echo "   • Landing page with performance stats"
echo "   • Live demo of email system"
echo "   • Real autonomous testing results"
echo "   • GitHub repo with validated code"
echo ""
echo "💰 You're ready to raise funding!"
echo "=================================="
