#!/bin/bash
# Stop all Queztl services

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
PID_FILE="$REPO_ROOT/logs/service_pids.txt"

echo "🛑 Stopping Queztl Services"
echo "================================"

echo "📂 Repo root: $REPO_ROOT"

if [ -f "$PID_FILE" ]; then
    # shellcheck disable=SC1090
    source "$PID_FILE"

    echo "Stopping services..."

    if [ -n "${CONTACT_API:-}" ]; then
        kill "$CONTACT_API" 2>/dev/null && echo "✅ Contact API stopped (PID: $CONTACT_API)" || echo "⚠️  Contact API not running"
    fi

    if [ -n "${CONTENT_RUNNER:-}" ]; then
        kill "$CONTENT_RUNNER" 2>/dev/null && echo "✅ Content Runner stopped (PID: $CONTENT_RUNNER)" || echo "⚠️  Content Runner not running"
    fi

    if [ -n "${WEB_SERVER:-}" ]; then
        kill "$WEB_SERVER" 2>/dev/null && echo "✅ Web Server stopped (PID: $WEB_SERVER)" || echo "⚠️  Web Server not running"
    fi

    rm "$PID_FILE"
    echo ""
    echo "✅ All services stopped"
else
    echo "⚠️  No PID file found. Searching for running processes..."

    # Try to find and kill processes
    pkill -f "contact_form_api.py" && echo "✅ Stopped contact_form_api.py" || true
    pkill -f "content_runner.py" && echo "✅ Stopped content_runner.py" || true
    pkill -f "python3 -m http.server 8080" && echo "✅ Stopped web server" || true

    echo ""
    echo "Done"
fi
