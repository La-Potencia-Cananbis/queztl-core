#!/bin/bash
# Stop all Queztl services

echo "🛑 Stopping Queztl Services"
echo "================================"

PID_FILE="$HOME/queztl-core/logs/service_pids.txt"

if [ -f "$PID_FILE" ]; then
    source "$PID_FILE"
    
    echo "Stopping services..."
    
    if [ ! -z "$CONTACT_API" ]; then
        kill $CONTACT_API 2>/dev/null && echo "✅ Contact API stopped (PID: $CONTACT_API)" || echo "⚠️  Contact API not running"
    fi
    
    if [ ! -z "$CONTENT_RUNNER" ]; then
        kill $CONTENT_RUNNER 2>/dev/null && echo "✅ Content Runner stopped (PID: $CONTENT_RUNNER)" || echo "⚠️  Content Runner not running"
    fi
    
    if [ ! -z "$WEB_SERVER" ]; then
        kill $WEB_SERVER 2>/dev/null && echo "✅ Web Server stopped (PID: $WEB_SERVER)" || echo "⚠️  Web Server not running"
    fi
    
    rm "$PID_FILE"
    echo ""
    echo "✅ All services stopped"
else
    echo "⚠️  No PID file found. Searching for running processes..."
    
    # Try to find and kill processes
    pkill -f "contact_form_api.py" && echo "✅ Stopped contact_form_api.py"
    pkill -f "content_runner.py" && echo "✅ Stopped content_runner.py"
    pkill -f "python3 -m http.server 8080" && echo "✅ Stopped web server"
    
    echo ""
    echo "Done"
fi
