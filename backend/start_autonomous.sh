#!/bin/bash
# 🤖 AUTONOMOUS STARTUP - TODO LOCAL

echo "🚀 Levantando sistema autónomo..."
echo ""

# Activar venv si existe, si no usar sistema
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activado"
else
    echo "⚠️  Usando Python del sistema"
fi

# Backend local
echo ""
echo "1. Backend (puerto 8000)..."
cd /Users/xavasena/hive/backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 > /tmp/backend_local.log 2>&1 &
BACKEND_PID=$!
echo "   ✅ Backend PID: $BACKEND_PID"

# Dashboard local  
echo ""
echo "2. Dashboard (puerto 3000)..."
cd /Users/xavasena/hive/dashboard
npm run dev > /tmp/dashboard_local.log 2>&1 &
DASHBOARD_PID=$!
echo "   ✅ Dashboard PID: $DASHBOARD_PID"

# Save PIDs
echo $BACKEND_PID > /tmp/autonomous_backend.pid
echo $DASHBOARD_PID > /tmp/autonomous_dashboard.pid

echo ""
echo "=" 
echo "=" 
echo "✅ SISTEMA AUTÓNOMO CORRIENDO"
echo "=" 
echo "=" 
echo ""
echo "URLs locales:"
echo "  • Backend:   http://localhost:8000"
echo "  • Dashboard: http://localhost:3000"
echo "  • Docs API:  http://localhost:8000/docs"
echo ""
echo "Logs:"
echo "  • Backend:   tail -f /tmp/backend_local.log"
echo "  • Dashboard: tail -f /tmp/dashboard_local.log"
echo ""
echo "Para detener:"
echo "  ./stop_autonomous.sh"
echo ""
echo "Para verificar:"
echo "  ./status_autonomous.sh"
echo ""
