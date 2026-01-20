#!/bin/bash
# Check status of all Queztl services and cluster nodes

echo "╔═══════════════════════════════════════════════════════╗"
echo "║  🦅 QUEZTL SYSTEM STATUS                             ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check cluster nodes
echo -e "${BLUE}🔌 CLUSTER NODES${NC}"
echo "─────────────────────────────────────────────────────────"

if curl -s --connect-timeout 2 http://192.168.1.105:8001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Beast (192.168.1.105:8001) - ONLINE${NC}"
else
    echo -e "${RED}❌ Beast (192.168.1.105:8001) - OFFLINE${NC}"
fi

if curl -s --connect-timeout 2 http://192.168.1.102:8000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Sloth (192.168.1.102:8000) - ONLINE${NC}"
else
    echo -e "${YELLOW}⚠️  Sloth (192.168.1.102:8000) - OFFLINE${NC}"
fi

echo ""

# Check local services
echo -e "${BLUE}🚀 LOCAL SERVICES${NC}"
echo "─────────────────────────────────────────────────────────"

if pgrep -f "contact_form_api.py" > /dev/null; then
    PID=$(pgrep -f "contact_form_api.py")
    echo -e "${GREEN}✅ Contact API (PID: $PID) - RUNNING${NC}"
    if curl -s http://localhost:8003/health > /dev/null 2>&1; then
        echo "   → http://localhost:8003 - responding"
    fi
else
    echo -e "${RED}❌ Contact API - NOT RUNNING${NC}"
fi

if pgrep -f "content_runner.py" > /dev/null; then
    PID=$(pgrep -f "content_runner.py")
    echo -e "${GREEN}✅ Content Runner (PID: $PID) - RUNNING${NC}"
else
    echo -e "${YELLOW}⚠️  Content Runner - NOT RUNNING${NC}"
fi

if pgrep -f "python3 -m http.server 8080" > /dev/null; then
    PID=$(pgrep -f "python3 -m http.server 8080")
    echo -e "${GREEN}✅ Web Server (PID: $PID) - RUNNING${NC}"
    if curl -s http://localhost:8080 > /dev/null 2>&1; then
        echo "   → http://localhost:8080 - responding"
    fi
else
    echo -e "${RED}❌ Web Server - NOT RUNNING${NC}"
fi

echo ""

# Check database
echo -e "${BLUE}💾 DATABASE${NC}"
echo "─────────────────────────────────────────────────────────"

if [ -f ~/queztl-core/data/members.db ]; then
    SIZE=$(du -h ~/queztl-core/data/members.db | cut -f1)
    COUNT=$(sqlite3 ~/queztl-core/data/members.db "SELECT COUNT(*) FROM members;" 2>/dev/null || echo "0")
    echo -e "${GREEN}✅ Database exists ($SIZE)${NC}"
    echo "   → $COUNT members registered"
else
    echo -e "${YELLOW}⚠️  Database not found${NC}"
fi

echo ""

# Check generated content
echo -e "${BLUE}🎨 GENERATED CONTENT${NC}"
echo "─────────────────────────────────────────────────────────"

if [ -d ~/queztl-core/frontend/generated ]; then
    COUNT=$(ls -1 ~/queztl-core/frontend/generated/*.png 2>/dev/null | wc -l)
    if [ $COUNT -gt 0 ]; then
        SIZE=$(du -sh ~/queztl-core/frontend/generated 2>/dev/null | cut -f1)
        echo -e "${GREEN}✅ $COUNT images generated ($SIZE)${NC}"
        echo "   Latest:"
        ls -lt ~/queztl-core/frontend/generated/*.png 2>/dev/null | head -3 | awk '{print "   →", $9, "("$5")"}'
    else
        echo -e "${YELLOW}⚠️  No images generated yet${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Generated folder not found${NC}"
fi

echo ""

# Check configuration
echo -e "${BLUE}⚙️  CONFIGURATION${NC}"
echo "─────────────────────────────────────────────────────────"

if [ -f ~/.config/email.env ]; then
    echo -e "${GREEN}✅ Email configured${NC}"
else
    echo -e "${YELLOW}⚠️  Email not configured${NC}"
fi

if [ -f ~/.config/dyndns.env ]; then
    source ~/.config/dyndns.env
    echo -e "${GREEN}✅ DynDNS configured: $DYNDNS_DOMAIN${NC}"
else
    echo -e "${YELLOW}⚠️  DynDNS not configured${NC}"
fi

if [ -f ~/.config/meta.env ]; then
    echo -e "${GREEN}✅ Meta API configured${NC}"
else
    echo -e "${YELLOW}⚠️  Meta API not configured${NC}"
fi

echo ""

# Check logs
echo -e "${BLUE}📝 RECENT LOGS${NC}"
echo "─────────────────────────────────────────────────────────"

if [ -f ~/queztl-core/logs/contact_api.log ]; then
    LINES=$(wc -l < ~/queztl-core/logs/contact_api.log)
    echo "Contact API: $LINES log lines"
    tail -2 ~/queztl-core/logs/contact_api.log 2>/dev/null | sed 's/^/   → /'
fi

if [ -f ~/queztl-core/logs/content_runner.log ]; then
    LINES=$(wc -l < ~/queztl-core/logs/content_runner.log)
    echo "Content Runner: $LINES log lines"
    tail -2 ~/queztl-core/logs/content_runner.log 2>/dev/null | sed 's/^/   → /'
fi

echo ""

# ISO build status
echo -e "${BLUE}🏗️  ISO BUILD${NC}"
echo "─────────────────────────────────────────────────────────"

if [ -f /tmp/iso-build-current.log ]; then
    LINES=$(wc -l < /tmp/iso-build-current.log)
    echo "Build log: $LINES lines"
    echo "Last 2 lines:"
    tail -2 /tmp/iso-build-current.log | sed 's/^/   → /'
    
    if [ -f ~/queztl-core/output/queztl-os/QueztlOS-1.0.0-amd64.iso ]; then
        SIZE=$(du -h ~/queztl-core/output/queztl-os/QueztlOS-1.0.0-amd64.iso | cut -f1)
        echo -e "${GREEN}✅ ISO built: $SIZE${NC}"
    else
        echo -e "${YELLOW}⏳ ISO building...${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  No build log found${NC}"
fi

echo ""

# Summary
echo "╔═══════════════════════════════════════════════════════╗"
echo "║  📊 SUMMARY                                           ║"
echo "╚═══════════════════════════════════════════════════════╝"

# Count services
RUNNING=0
TOTAL=3

pgrep -f "contact_form_api.py" > /dev/null && ((RUNNING++))
pgrep -f "content_runner.py" > /dev/null && ((RUNNING++))
pgrep -f "python3 -m http.server 8080" > /dev/null && ((RUNNING++))

if [ $RUNNING -eq $TOTAL ]; then
    echo -e "${GREEN}✅ All services running ($RUNNING/$TOTAL)${NC}"
elif [ $RUNNING -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Some services running ($RUNNING/$TOTAL)${NC}"
else
    echo -e "${RED}❌ No services running ($RUNNING/$TOTAL)${NC}"
fi

# Quick actions
echo ""
echo "🎯 Quick Actions:"
if [ $RUNNING -eq 0 ]; then
    echo "   • Start services: ./start.sh"
fi
if [ $RUNNING -gt 0 ]; then
    echo "   • Stop services: ./stop-services.sh"
fi
echo "   • View logs: tail -f ~/queztl-core/logs/*.log"
echo "   • Full status: ./status.sh"
echo ""
