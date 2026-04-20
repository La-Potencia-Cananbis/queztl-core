#!/bin/bash
# Start email backend with persistent SMTP credentials

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$REPO_ROOT/.env.email"
LOG_FILE="$REPO_ROOT/email_backend.log"

echo "🚀 Starting Queztl Email Backend with SMTP"
echo "==========================================="
echo ""
echo "📂 Repo root: $REPO_ROOT"

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "⚠️  No .env.email file found. Creating one..."
    echo ""
    echo "Paste your Microsoft App Password:"
    read -r -s -p "> " SMTP_PASS
    echo ""

    # Save to .env file
    cat > "$ENV_FILE" << EOF_ENV
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=salvadorsena@live.com
SMTP_PASSWORD=$SMTP_PASS
USE_REAL_SMTP=true
EOF_ENV
    echo "✅ Credentials saved to $ENV_FILE"
else
    echo "✅ Using existing credentials from $ENV_FILE"
fi

echo ""

# Kill existing backend
lsof -ti:8001 | xargs kill -9 2>/dev/null || true
sleep 1

# Load env and start backend
echo "🔄 Starting backend..."
cd "$REPO_ROOT"

# Export variables from .env file
set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

# Start backend in background
python3 backend/email_service.py > "$LOG_FILE" 2>&1 &
BACKEND_PID=$!

sleep 2

# Test if it's running
if curl -s http://localhost:8001/ > /dev/null 2>&1; then
    echo "✅ Backend running on port 8001 (PID: $BACKEND_PID)"
    echo "✅ SMTP enabled with salvadorsena@live.com"
    echo ""
    echo "📧 Test it: open $REPO_ROOT/my-email.html"
    echo ""
    echo "📋 View logs: tail -f $LOG_FILE"
else
    echo "❌ Backend failed to start. Check logs:"
    tail -20 "$LOG_FILE"
fi
