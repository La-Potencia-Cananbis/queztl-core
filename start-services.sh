#!/bin/bash
# Start all Queztl services - Web server + Content runner + Contact API

echo "🚀 Starting Queztl Services"
echo "================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required"
    exit 1
fi

# Create directories
mkdir -p ~/queztl-core/data
mkdir -p ~/queztl-core/frontend/generated
mkdir -p ~/queztl-core/logs

# Set environment variables for email (update these!)
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SENDER_EMAIL="your-email@gmail.com"  # UPDATE THIS
export SENDER_PASSWORD=""  # UPDATE THIS with app password
export RECIPIENT_EMAIL="your-email@gmail.com"  # UPDATE THIS

# Set Sloth storage path (update when Sloth is mounted)
export SLOTH_DB_PATH="$HOME/queztl-core/data/members.db"

echo ""
echo "📦 Installing Python dependencies..."
pip3 install -q fastapi uvicorn aiohttp python-multipart 2>/dev/null || echo "⚠️  Some packages may already be installed"

echo ""
echo "🌐 Starting Contact Form API on port 8003..."
cd ~/queztl-core
python3 backend/contact_form_api.py > logs/contact_api.log 2>&1 &
CONTACT_PID=$!
echo "   PID: $CONTACT_PID"

sleep 2

echo ""
echo "🎨 Starting Content Runner..."
python3 backend/content_runner.py --single > logs/content_runner.log 2>&1 &
CONTENT_PID=$!
echo "   PID: $CONTENT_PID"

sleep 2

echo ""
echo "🖥️  Starting web server on port 8080..."
cd ~/queztl-core/frontend
python3 -m http.server 8080 > ../logs/webserver.log 2>&1 &
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
echo "   • tail -f ~/queztl-core/logs/contact_api.log"
echo "   • tail -f ~/queztl-core/logs/content_runner.log"
echo "   • tail -f ~/queztl-core/logs/webserver.log"
echo ""
echo "🛑 To stop all services:"
echo "   kill $CONTACT_PID $CONTENT_PID $WEB_PID"
echo ""

# Save PIDs to file for easy cleanup
cat > ~/queztl-core/logs/service_pids.txt <<EOF
CONTACT_API=$CONTACT_PID
CONTENT_RUNNER=$CONTENT_PID
WEB_SERVER=$WEB_PID
EOF

echo "💾 PIDs saved to ~/queztl-core/logs/service_pids.txt"
echo ""
echo "⚠️  IMPORTANT: Update email credentials in this script!"
echo "   Edit: $0"
echo "   Set SENDER_EMAIL and SENDER_PASSWORD"
echo ""
