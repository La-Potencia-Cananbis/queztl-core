#!/bin/bash
# Start email backend with persistent SMTP credentials

echo "🚀 Starting Queztl Email Backend with SMTP"
echo "==========================================="
echo ""

# Check if .env file exists
if [ ! -f /Users/xavasena/hive/.env.email ]; then
    echo "⚠️  No .env.email file found. Creating one..."
    echo ""
    echo "Paste your Microsoft App Password:"
    read -sp "> " SMTP_PASS
    echo ""
    
    # Save to .env file
    cat > /Users/xavasena/hive/.env.email << EOF
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=salvadorsena@live.com
SMTP_PASSWORD=$SMTP_PASS
USE_REAL_SMTP=true
EOF
    echo "✅ Credentials saved to .env.email"
else
    echo "✅ Using existing credentials from .env.email"
fi

echo ""

# Kill existing backend
lsof -ti:8001 | xargs kill -9 2>/dev/null
sleep 1

# Load env and start backend
echo "🔄 Starting backend..."
cd /Users/xavasena/hive

# Export variables from .env file
export $(cat .env.email | xargs)

# Start backend in background
python3 backend/email_service.py > email_backend.log 2>&1 &
BACKEND_PID=$!

sleep 2

# Test if it's running
if curl -s http://localhost:8001/ > /dev/null 2>&1; then
    echo "✅ Backend running on port 8001 (PID: $BACKEND_PID)"
    echo "✅ SMTP enabled with salvadorsena@live.com"
    echo ""
    echo "📧 Test it: open /Users/xavasena/hive/my-email.html"
    echo ""
    echo "📋 View logs: tail -f /Users/xavasena/hive/email_backend.log"
else
    echo "❌ Backend failed to start. Check logs:"
    tail -20 email_backend.log
fi
