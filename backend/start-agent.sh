#!/bin/bash
# Start QuetzalCore Autonomous Agent Runner

echo "🤖 Starting QuetzalCore Autonomous Agent..."
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found"
    echo "   Run: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi

# Check if agent is already running
if pgrep -f "agent_runner.py" > /dev/null; then
    echo "⚠️  Agent is already running"
    echo ""
    echo "To stop: ./stop-agent.sh"
    echo "To view logs: tail -f agent_runner.log"
    exit 0
fi

# Ensure psutil is installed
.venv/bin/pip install -q psutil requests 2>/dev/null

echo "✅ Starting autonomous agent in background..."
echo ""

# Start agent in background
nohup .venv/bin/python agent_runner.py > agent_runner_startup.log 2>&1 &
AGENT_PID=$!

echo "Agent PID: $AGENT_PID"
echo "$AGENT_PID" > .agent.pid

# Wait a moment to check if it started
sleep 3

if ps -p $AGENT_PID > /dev/null; then
    echo ""
    echo "✅ Agent is running!"
    echo ""
    echo "📋 Monitoring:"
    echo "   • Watch logs: tail -f agent_runner.log"
    echo "   • Live status: cat SYSTEM_STATUS_LIVE.md"
    echo "   • Stop agent: ./stop-agent.sh"
    echo ""
    echo "🔄 Agent performs:"
    echo "   ✓ Service health monitoring (every 30s)"
    echo "   ✓ Auto-restart failed services"
    echo "   ✓ Performance optimization (every 2.5min)"
    echo "   ✓ Code quality checks (every 5min)"
    echo "   ✓ Documentation updates (every 10min)"
    echo "   ✓ Security scanning (every 7.5min)"
    echo "   ✓ Load testing (every 15min)"
    echo ""
    echo "Dale! Agent is watching... 🤖👀"
else
    echo ""
    echo "❌ Agent failed to start"
    echo "   Check agent_runner_startup.log for errors"
    exit 1
fi
