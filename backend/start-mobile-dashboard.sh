#!/bin/bash
# Start Mobile Dashboard with SSL/TLS Support

echo "🔐 Starting Secure Mobile Dashboard..."

# Check if SSL certificates exist
if [ ! -f "ssl_certs/cert.pem" ] || [ ! -f "ssl_certs/key.pem" ]; then
    echo "⚠️  SSL certificates not found. Generating..."
    chmod +x generate_ssl_cert.sh
    ./generate_ssl_cert.sh
    echo ""
fi

# Kill existing dashboard
echo "🛑 Stopping existing dashboard..."
pkill -f "mobile_dashboard.py" 2>/dev/null
lsof -ti:9999 | xargs kill -9 2>/dev/null
sleep 1

# Start dashboard
echo "🚀 Starting dashboard with SSL..."
chmod +x mobile_dashboard.py
.venv/bin/python mobile_dashboard.py &

# Wait for startup
sleep 3

# Check if running
if lsof -Pi :9999 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo ""
    echo "✅ Dashboard started successfully!"
    echo ""
    
    # Get local IP
    LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | head -n1 | awk '{print $2}')
    
    # Check if SSL is enabled
    if [ -f "ssl_certs/cert.pem" ]; then
        echo "🔒 HTTPS Enabled"
        echo "📱 Access from your Samsung phone: https://$LOCAL_IP:9999"
        echo "💻 Test locally: https://localhost:9999"
        echo ""
        echo "⚠️  On first access, you'll see a security warning about the"
        echo "    self-signed certificate. Click 'Advanced' → 'Proceed' to continue."
    else
        echo "⚠️  HTTP Only (No SSL)"
        echo "📱 Access from your Samsung phone: http://$LOCAL_IP:9999"
        echo "💻 Test locally: http://localhost:9999"
    fi
    echo ""
    echo "🔍 To view logs: tail -f nohup.out"
    echo "🛑 To stop: pkill -f mobile_dashboard.py"
else
    echo "❌ Dashboard failed to start!"
    echo "Check logs for errors"
fi
