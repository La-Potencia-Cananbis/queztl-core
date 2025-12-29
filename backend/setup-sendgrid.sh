#!/bin/bash
# Setup SendGrid for real email sending

echo "🚀 Queztl Email - SendGrid Setup"
echo "=================================="
echo ""
echo "SendGrid provides reliable email delivery with your domain."
echo ""
echo "📧 Quick Start:"
echo "1. Go to: https://sendgrid.com/ (Free 100 emails/day)"
echo "2. Sign up and verify your email"
echo "3. Settings → API Keys → Create API Key"
echo "4. Copy the API key (starts with SG.)"
echo ""
read -sp "Paste your SendGrid API Key (or press Enter to skip): " API_KEY
echo ""

if [ -z "$API_KEY" ]; then
    echo ""
    echo "⚠️  No API key entered. Running in LOCAL MODE."
    echo ""
    echo "To send real emails:"
    echo "1. Get SendGrid API key: https://sendgrid.com/"
    echo "2. Run: ./setup-sendgrid.sh"
    echo ""
else
    # Save to .env file
    cat > /Users/xavasena/hive/.env.email << EOF
SENDGRID_API_KEY=$API_KEY
FROM_EMAIL=salvador@senasaitech.com
FROM_NAME=Salvador Sena - Queztl
EOF
    echo "✅ SendGrid configured!"
    echo ""
fi

# Restart backend
echo "🔄 Restarting backend..."
lsof -ti:8001 | xargs kill -9 2>/dev/null
sleep 1

cd /Users/xavasena/hive
if [ -f .env.email ]; then
    export $(cat .env.email | xargs)
fi

python3 backend/email_service.py > email_backend.log 2>&1 &
BACKEND_PID=$!

sleep 3

if curl -s http://localhost:8001/ > /dev/null 2>&1; then
    echo "✅ Backend running (PID: $BACKEND_PID)"
    
    if [ -n "$API_KEY" ]; then
        echo "✅ SendGrid enabled - emails will be sent!"
        echo "📧 From: salvador@senasaitech.com"
    else
        echo "⚠️  Local mode - get SendGrid key to send real emails"
    fi
    
    echo ""
    echo "🌐 Open: /Users/xavasena/hive/my-email.html"
else
    echo "❌ Backend failed. Check: tail -f email_backend.log"
fi

echo ""
