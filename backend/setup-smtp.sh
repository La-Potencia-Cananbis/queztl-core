#!/bin/bash
# Quick setup script for real email sending

echo "🚀 Queztl Email - Real SMTP Setup"
echo "===================================="
echo ""
echo "To send real emails, you need an app password from Microsoft."
echo ""
echo "📧 Steps:"
echo "1. Go to: https://account.live.com/proofs/manage/additional"
echo "2. Click 'Create a new app password'"
echo "3. Copy the password"
echo "4. Paste it below"
echo ""
read -sp "Enter your Microsoft App Password (or press Enter to skip): " SMTP_PASS
echo ""

if [ -z "$SMTP_PASS" ]; then
    echo ""
    echo "⚠️  No password entered. Emails will be logged but not sent."
    echo ""
    echo "Backend will run in LOCAL MODE:"
    echo "  - Emails stored in memory"
    echo "  - Visible in your email UI"
    echo "  - NOT sent to actual recipients"
    echo ""
    export USE_REAL_SMTP=false
else
    echo ""
    echo "✅ Password set! Emails will be sent for real."
    echo ""
    export SMTP_PASSWORD="$SMTP_PASS"
    export USE_REAL_SMTP=true
fi

# Kill existing backend
echo "🔄 Restarting backend..."
lsof -ti:8001 | xargs kill -9 2>/dev/null
sleep 1

# Start backend
cd /Users/xavasena/hive
python3 backend/email_service.py &

sleep 2

echo ""
echo "✅ Backend started!"
echo ""

# Test connection
if curl -s http://localhost:8001/ > /dev/null 2>&1; then
    echo "✅ Backend is responding on port 8001"
    
    if [ "$USE_REAL_SMTP" = "true" ]; then
        echo "✅ SMTP enabled - emails will be sent for real!"
    else
        echo "⚠️  SMTP disabled - emails will be logged only"
        echo ""
        echo "To enable real sending, get an app password from:"
        echo "https://account.live.com/proofs/manage/additional"
        echo ""
        echo "Then run: ./setup-smtp.sh"
    fi
else
    echo "❌ Backend failed to start. Check logs."
fi

echo ""
echo "🌐 Open your email UI: open /Users/xavasena/hive/my-email.html"
echo ""
