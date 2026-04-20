#!/bin/bash
# Start all Queztl services - Web server + Content runner + Contact API

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
DATA_DIR="$REPO_ROOT/data"
GENERATED_DIR="$REPO_ROOT/frontend/generated"
LOG_DIR="$REPO_ROOT/logs"

echo "🚀 Starting Queztl Services"
echo "================================"
echo "📂 Repo root: $REPO_ROOT"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required"
    exit 1
fi

# Create directories
mkdir -p "$DATA_DIR" "$GENERATED_DIR" "$LOG_DIR"

# Set environment variables for email (update these!)
export SMTP_SERVER="${SMTP_SERVER:-smtp.gmail.com}"
export SMTP_PORT="${SMTP_PORT:-587}"
export SENDER_EMAIL="${SENDER_EMAIL:-your-email@gmail.com}"  # UPDATE THIS
export SENDER_PASSWORD="${SENDER_PASSWORD:-}"  # UPDATE THIS with app password
export RECIPIENT_EMAIL="${RECIPIENT_EMAIL:-your-email@gmail.com}"  # UPDATE THIS

# Set Sloth storage path (update when Sloth is mounted)
export SLOTH_DB_PATH="${SLOTH_DB_PATH:-$DATA_DIR/members.db}"

echo ""
echo "📦 Installing Python dependencies..."
pip3 install -q fastapi uvicorn aiohttp python-multipart 2>/dev/null || echo "⚠️  Some packages may already be installed"

echo ""
echo "🌐 Starting Contact Form API on port 8003..."
cd "$REPO_ROOT"
python3 backend/contact_form_api.py > "$LOG_DIR/contact_api.log" 2>&1 &
CONTACT_PID=$!
echo "   PID: $CONTACT_PID"

sleep 2

echo ""
echo "🎨 Starting Content Runner..."
python3 backend/content_runner.py --single > "$LOG_DIR/content_runner.log" 2>&1 &
CONTENT_PID=$!
echo "   PID: $CONTENT_PID"

sleep 2

echo ""
echo "🖥️  Starting web server on port 8080..."
cd "$REPO_ROOT/frontend"
python3 -m http.server 8080 > "$LOG_DIR/webserver.log" 2>&1 &
WEB_PID=$!
echo "   PID: $WEB_PID"

echo ""
echo "================================"
echo "✅ All services started!"
echo ""
echo "📍 Services running:"
echo "   • Web Server:    http://localhost:8080"
echo "   • Contact API:   http://localhost:8003"
echo "   • Contact Form:  http://localhost:8080/contact.html"
echo "   • Beast API:     http://192.168.1.105:8001"
echo ""
echo "📊 Process IDs:"
echo "   • Contact API: $CONTACT_PID"
echo "   • Content Runner: $CONTENT_PID"
echo "   • Web Server: $WEB_PID"
echo ""
echo "📝 Logs:"
echo "   • tail -f $LOG_DIR/contact_api.log"
echo "   • tail -f $LOG_DIR/content_runner.log"
echo "   • tail -f $LOG_DIR/webserver.log"
echo ""
echo "🛑 To stop all services:"
echo "   kill $CONTACT_PID $CONTENT_PID $WEB_PID"
echo ""

# Save PIDs to file for easy cleanup
cat > "$LOG_DIR/service_pids.txt" <<EOF_PIDS
CONTACT_API=$CONTACT_PID
CONTENT_RUNNER=$CONTENT_PID
WEB_SERVER=$WEB_PID
EOF_PIDS

echo "💾 PIDs saved to $LOG_DIR/service_pids.txt"
echo ""
echo "⚠️  IMPORTANT: Update email credentials in this script or environment"
echo "   Edit: $0"
echo "   Set SENDER_EMAIL and SENDER_PASSWORD"
echo ""
