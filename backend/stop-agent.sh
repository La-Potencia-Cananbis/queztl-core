#!/bin/bash
# Stop QuetzalCore Autonomous Agent

echo "🛑 Stopping QuetzalCore Autonomous Agent..."

if [ -f .agent.pid ]; then
    AGENT_PID=$(cat .agent.pid)
    
    if ps -p $AGENT_PID > /dev/null 2>&1; then
        echo "   Stopping agent (PID: $AGENT_PID)"
        kill -TERM $AGENT_PID 2>/dev/null
        
        # Wait for graceful shutdown
        for i in {1..10}; do
            if ! ps -p $AGENT_PID > /dev/null 2>&1; then
                break
            fi
            sleep 1
        done
        
        # Force kill if still running
        if ps -p $AGENT_PID > /dev/null 2>&1; then
            echo "   Force stopping..."
            kill -9 $AGENT_PID 2>/dev/null
        fi
        
        echo "✅ Agent stopped"
    else
        echo "⚠️  Agent not running (stale PID file)"
    fi
    
    rm .agent.pid
else
    # Try to find and kill by process name
    if pgrep -f "agent_runner.py" > /dev/null; then
        echo "   Found agent by process name, stopping..."
        pkill -f "agent_runner.py"
        echo "✅ Agent stopped"
    else
        echo "⚠️  No agent PID file found and agent not running"
    fi
fi

echo ""
echo "📊 Final status saved to: SYSTEM_STATUS_FINAL.md"
