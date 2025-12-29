#!/bin/bash
# 🛑 STOP AUTONOMOUS SYSTEM

echo "🛑 Deteniendo sistema autónomo..."
echo ""

if [ -f /tmp/autonomous_backend.pid ]; then
    kill $(cat /tmp/autonomous_backend.pid) 2>/dev/null
    echo "✅ Backend detenido"
fi

if [ -f /tmp/autonomous_dashboard.pid ]; then
    kill $(cat /tmp/autonomous_dashboard.pid) 2>/dev/null
    echo "✅ Dashboard detenido"
fi

if [ -f /tmp/autonomous_email.pid ]; then
    kill $(cat /tmp/autonomous_email.pid) 2>/dev/null
    echo "✅ Email detenido"
fi

rm -f /tmp/autonomous_*.pid
echo ""
echo "✅ Sistema autónomo detenido"
