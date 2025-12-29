#!/bin/bash
# 📊 CHECK AUTONOMOUS SYSTEM STATUS

echo "📊 Estado del sistema autónomo"
echo ""

check_service() {
    local name=$1
    local pid_file=$2
    local port=$3
    
    if [ -f $pid_file ]; then
        pid=$(cat $pid_file)
        if ps -p $pid > /dev/null 2>&1; then
            echo "✅ $name: CORRIENDO (PID: $pid, Puerto: $port)"
        else
            echo "❌ $name: DETENIDO (PID file exists but process dead)"
        fi
    else
        echo "⚠️  $name: NO INICIADO"
    fi
}

check_service "Backend  " "/tmp/autonomous_backend.pid" "8000"
check_service "Dashboard" "/tmp/autonomous_dashboard.pid" "3000"
check_service "Email    " "/tmp/autonomous_email.pid" "3001"

echo ""
echo "URLs:"
echo "  http://localhost:8000 - Backend"
echo "  http://localhost:3000 - Dashboard"
echo "  http://localhost:3001 - Email"
