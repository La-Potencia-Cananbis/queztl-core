#!/bin/bash
# Setup SendGrid for real email sending

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$REPO_ROOT/.env.email"
LOG_FILE="$REPO_ROOT/email_backend.log"

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
read -r -s -p "Paste your SendGrid API Key (or press Enter to skip): " API_KEY
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
    cat > "$ENV_FILE" << EOF_ENV
SENDGRID_API_KEY=$API_KEY
FROM_EMAIL=salvador@senasaitech.com
FROM_NAME=Salvador Sena - Queztl
EOF_ENV
    echo "✅ SendGrid configured!"
    echo ""
fi

# Restart backend
echo "🔄 Restarting backend..."
lsof -ti:8001 | xargs kill -9 2>/dev/null || true
sleep 1

cd "$REPO_ROOT"
if [ -f "$ENV_FILE" ]; then
    set -a
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +a
fi

python3 backend/email_service.py > "$LOG_FILE" 2>&1 &
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
    echo "🌐 Open: $REPO_ROOT/my-email.html"
else
    echo "❌ Backend failed. Check: tail -f $LOG_FILE"
fi

echo ""
