#!/bin/bash
# Resource Manager - Control Hive workloads

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

show_status() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║          🎛️  HIVE RESOURCE MANAGER STATUS                  ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Check which mode we're in
    if docker ps --format "{{.Names}}" | grep -q "orchestrator"; then
        echo -e "${GREEN}Mode: Distributed (Orchestrator)${NC}"
        echo -e "${GREEN}Your Mac: Lightweight orchestrator only${NC}"
        echo ""
    else
        echo -e "${YELLOW}Mode: Monolithic (All-in-one)${NC}"
        echo -e "${RED}Warning: Running heavy compute on Mac${NC}"
        echo ""
    fi
    
    echo -e "${YELLOW}📊 Docker Containers:${NC}"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null || echo "Docker not available"
    
    echo ""
    echo -e "${YELLOW}🔥 CPU & Memory Usage:${NC}"
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemPerc}}" 2>/dev/null || echo "Stats not available"
    
    echo ""
    if docker ps --format "{{.Names}}" | grep -q "orchestrator"; then
        echo -e "${YELLOW}🌐 Registered Workers:${NC}"
        curl -s http://localhost:8000/workers 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "Orchestrator not responding"
        echo ""
        echo -e "${YELLOW}📋 Task Queue:${NC}"
        curl -s http://localhost:8000/queue 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "No tasks queued"
    fi
}

stop_training() {
    echo -e "${YELLOW}🛑 Stopping training processes...${NC}"
    docker exec hive-backend-1 bash -c 'pkill -f "train_" || true' 2>/dev/null || echo "No training processes found"
    docker exec hive-backend-1 bash -c 'pkill -f "queztl_auto_optimizer" || true' 2>/dev/null || echo "No optimizer running"
    echo -e "${GREEN}✅ Training stopped${NC}"
}

stop_monitors() {
    echo -e "${YELLOW}🛑 Stopping monitoring processes...${NC}"
    docker exec hive-backend-1 bash -c 'pkill -f "queztl_monitor" || true' 2>/dev/null || echo "No monitors running"
    docker exec hive-backend-1 bash -c 'pkill -f "queztl_ml_optimizer" || true' 2>/dev/null || echo "No ML optimizer running"
    echo -e "${GREEN}✅ Monitors stopped${NC}"
}

stop_web_interfaces() {
    echo -e "${YELLOW}🛑 Stopping web interfaces...${NC}"
    docker stop gen3d-frontend hive-dashboard-1 gen3d-backend 2>/dev/null || echo "Already stopped"
    echo -e "${GREEN}✅ Web interfaces stopped${NC}"
}

start_minimal() {
    echo -e "${YELLOW}🚀 Starting minimal services only...${NC}"
    docker-compose up -d db redis backend
    echo -e "${GREEN}✅ Essential services running (DB, Redis, Backend API)${NC}"
}

stop_all() {
    echo -e "${RED}🛑 STOPPING ALL SERVICES...${NC}"
    docker-compose down
    echo -e "${GREEN}✅ All services stopped${NC}"
}

cleanup_logs() {
    echo -e "${YELLOW}🧹 Cleaning up log files...${NC}"
    docker exec hive-backend-1 bash -c 'rm -f /workspace/*.log' 2>/dev/null || true
    docker exec hive-backend-1 bash -c 'rm -f /workspace/protocol_data/*.db' 2>/dev/null || true
    echo -e "${GREEN}✅ Logs cleaned${NC}"
}

optimize_for_dev() {
    echo -e "${BLUE}⚡ Optimizing for development mode...${NC}"
    stop_training
    stop_monitors
    stop_web_interfaces
    echo ""
    echo -e "${GREEN}✅ Optimization complete!${NC}"
    echo ""
    echo -e "${YELLOW}Services running:${NC}"
    echo "  • Backend API (port 8000) - Core API services"
    echo "  • PostgreSQL (port 5432) - Database"
    echo "  • Redis (port 6379) - Caching"
    echo ""
    echo -e "${YELLOW}Services stopped:${NC}"
    echo "  • Frontend UIs (ports 3000, 3001) - Not needed for backend work"
    echo "  • Training processes - Heavy CPU usage"
    echo "  • Monitoring daemons - Background overhead"
    echo ""
    show_status
}

restart_all() {
    echo -e "${BLUE}🔄 Restarting all services...${NC}"
    docker-compose restart
    sleep 5
    show_status
}

case "${1}" in
    status|"")
        show_status
        ;;
    stop-training)
        stop_training
        show_status
        ;;
    stop-monitors)
        stop_monitors
        show_status
        ;;
    stop-web)
        stop_web_interfaces
        show_status
        ;;
    minimal)
        start_minimal
        show_status
        ;;
    optimize)
        optimize_for_dev
        ;;
    cleanup)
        cleanup_logs
        ;;
    stop-all)
        stop_all
        ;;
    restart)
        restart_all
        ;;
    *)
        echo "Hive Resource Manager"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  status          Show current resource usage (default)"
        echo "  optimize        Optimize for development (stop heavy processes)"
        echo "  stop-training   Stop all training processes"
        echo "  stop-monitors   Stop monitoring daemons"
        echo "  stop-web        Stop web interfaces"
        echo "  minimal         Start only essential services"
        echo "  cleanup         Clean up log files"
        echo "  stop-all        Stop all Docker services"
        echo "  restart         Restart all services"
        echo ""
        exit 1
        ;;
esac
