#!/bin/bash
# Quick Setup Wizard for Queztl Dynamic Website

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
CONFIG_DIR="$REPO_ROOT/.config"
DATA_DIR="$REPO_ROOT/data"
LOG_DIR="$REPO_ROOT/logs"
GENERATED_DIR="$REPO_ROOT/frontend/generated"

echo "╔═══════════════════════════════════════════════════════╗"
echo "║  🦅 QUEZTL WEBSITE SETUP WIZARD                      ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "📂 Repo root: $REPO_ROOT"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create directories
echo "📁 Creating directories..."
mkdir -p "$DATA_DIR" "$GENERATED_DIR" "$LOG_DIR" "$CONFIG_DIR"
echo "✅ Directories created"
echo ""

# Check dependencies
echo "🔍 Checking dependencies..."
MISSING_DEPS=0

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    MISSING_DEPS=1
else
    echo -e "${GREEN}✅ Python 3 found${NC}"
fi

if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 not found${NC}"
    MISSING_DEPS=1
else
    echo -e "${GREEN}✅ pip3 found${NC}"
fi

if [ $MISSING_DEPS -eq 1 ]; then
    echo ""
    echo -e "${RED}Please install missing dependencies first${NC}"
    exit 1
fi
echo ""

# Install Python packages
echo "📦 Installing Python packages..."
pip3 install -q fastapi uvicorn aiohttp python-multipart 2>&1 | grep -v "already satisfied" || true
echo "✅ Python packages installed"
echo ""

# Test cluster connectivity
echo "🔌 Testing cluster connectivity..."

if curl -s --connect-timeout 2 http://192.168.1.105:8001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Beast online (192.168.1.105:8001)${NC}"
    BEAST_ONLINE=1
else
    echo -e "${YELLOW}⚠️  Beast offline (192.168.1.105:8001)${NC}"
    BEAST_ONLINE=0
fi

if curl -s --connect-timeout 2 http://192.168.1.102:8000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Sloth online (192.168.1.102:8000)${NC}"
    SLOTH_ONLINE=1
else
    echo -e "${YELLOW}⚠️  Sloth offline (192.168.1.102:8000)${NC}"
    SLOTH_ONLINE=0
fi
echo ""

# Email configuration
echo "📧 Email Configuration"
echo "─────────────────────────────────────────────────────────"
echo "For contact form to send emails, you need SMTP credentials."
echo "Gmail App Password recommended: https://support.google.com/accounts/answer/185833"
echo ""

read -r -p "Configure email now? (y/n): " CONFIGURE_EMAIL

if [ "$CONFIGURE_EMAIL" = "y" ]; then
    read -r -p "SMTP Server [smtp.gmail.com]: " SMTP_SERVER
    SMTP_SERVER=${SMTP_SERVER:-smtp.gmail.com}

    read -r -p "SMTP Port [587]: " SMTP_PORT
    SMTP_PORT=${SMTP_PORT:-587}

    read -r -p "Sender Email: " SENDER_EMAIL

    read -r -s -p "Sender Password (hidden): " SENDER_PASSWORD
    echo ""

    read -r -p "Recipient Email (for notifications): " RECIPIENT_EMAIL

    # Save to config file
    cat > "$CONFIG_DIR/email.env" <<EOF_EMAIL
export SMTP_SERVER="$SMTP_SERVER"
export SMTP_PORT="$SMTP_PORT"
export SENDER_EMAIL="$SENDER_EMAIL"
export SENDER_PASSWORD="$SENDER_PASSWORD"
export RECIPIENT_EMAIL="$RECIPIENT_EMAIL"
EOF_EMAIL

    chmod 600 "$CONFIG_DIR/email.env"
    echo -e "${GREEN}✅ Email configuration saved${NC}"
else
    echo -e "${YELLOW}⚠️  Skipping email configuration (can configure later)${NC}"
fi
echo ""

# DynDNS setup
echo "🌐 DynDNS Configuration"
echo "─────────────────────────────────────────────────────────"
echo "For public access, configure DynDNS."
echo "Popular providers: DuckDNS, No-IP, Dynu"
echo ""

read -r -p "Do you have a DynDNS domain? (y/n): " HAS_DYNDNS

if [ "$HAS_DYNDNS" = "y" ]; then
    read -r -p "Enter your DynDNS domain: " DYNDNS_DOMAIN

    cat > "$CONFIG_DIR/dyndns.env" <<EOF_DYNDNS
export DYNDNS_DOMAIN="$DYNDNS_DOMAIN"
EOF_DYNDNS

    echo -e "${GREEN}✅ DynDNS domain saved: $DYNDNS_DOMAIN${NC}"
    echo ""
    echo "📝 Next steps for DynDNS:"
    echo "   1. Set up DynDNS update client"
    echo "   2. Configure router port forwarding (80 -> 8080)"
    echo "   3. Set up SSL certificate (Let's Encrypt)"
else
    echo -e "${YELLOW}⚠️  No DynDNS configured (local access only)${NC}"
fi
echo ""

# Meta API (Facebook)
echo "📱 Facebook API Configuration"
echo "─────────────────────────────────────────────────────────"
echo "For auto-posting to Facebook, you need Meta API approval."
echo ""

read -r -p "Do you have a Meta API key? (y/n): " HAS_META_KEY

if [ "$HAS_META_KEY" = "y" ]; then
    read -r -p "Enter Meta API key: " META_API_KEY

    cat > "$CONFIG_DIR/meta.env" <<EOF_META
export META_API_KEY="$META_API_KEY"
EOF_META

    chmod 600 "$CONFIG_DIR/meta.env"
    echo -e "${GREEN}✅ Meta API key saved${NC}"
else
    echo -e "${YELLOW}⚠️  No Meta API key (Facebook posting disabled)${NC}"
fi
echo ""

# Generate startup script with configs
echo "🔧 Generating startup script..."

cat > "$REPO_ROOT/start.sh" <<'EOFSTART'
#!/bin/bash
# Auto-generated startup script

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load repository configurations
[ -f "$SCRIPT_DIR/.config/email.env" ] && source "$SCRIPT_DIR/.config/email.env"
[ -f "$SCRIPT_DIR/.config/dyndns.env" ] && source "$SCRIPT_DIR/.config/dyndns.env"
[ -f "$SCRIPT_DIR/.config/meta.env" ] && source "$SCRIPT_DIR/.config/meta.env"

# Start services
cd "$SCRIPT_DIR"
./start-services.sh
EOFSTART

chmod +x "$REPO_ROOT/start.sh"

echo -e "${GREEN}✅ Startup script created: $REPO_ROOT/start.sh${NC}"
echo ""

# Summary
echo "╔═══════════════════════════════════════════════════════╗"
echo "║  ✅ SETUP COMPLETE                                    ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "📊 Configuration Summary:"
echo "─────────────────────────────────────────────────────────"

if [ -f "$CONFIG_DIR/email.env" ]; then
    # shellcheck disable=SC1090
    source "$CONFIG_DIR/email.env"
    echo -e "${GREEN}✅ Email configured: $SENDER_EMAIL${NC}"
else
    echo -e "${YELLOW}⚠️  Email not configured${NC}"
fi

if [ -f "$CONFIG_DIR/dyndns.env" ]; then
    # shellcheck disable=SC1090
    source "$CONFIG_DIR/dyndns.env"
    echo -e "${GREEN}✅ DynDNS: $DYNDNS_DOMAIN${NC}"
else
    echo -e "${YELLOW}⚠️  DynDNS not configured${NC}"
fi

if [ -f "$CONFIG_DIR/meta.env" ]; then
    echo -e "${GREEN}✅ Meta API configured${NC}"
else
    echo -e "${YELLOW}⚠️  Meta API not configured${NC}"
fi

if [ $BEAST_ONLINE -eq 1 ]; then
    echo -e "${GREEN}✅ Beast cluster node online${NC}"
else
    echo -e "${YELLOW}⚠️  Beast cluster node offline${NC}"
fi

if [ $SLOTH_ONLINE -eq 1 ]; then
    echo -e "${GREEN}✅ Sloth cluster node online${NC}"
else
    echo -e "${YELLOW}⚠️  Sloth cluster node offline${NC}"
fi

echo ""
echo "🚀 To start all services:"
echo "   cd $REPO_ROOT && ./start.sh"
echo ""
echo "🌐 Access points (after starting):"
echo "   • Web:     http://localhost:8080"
echo "   • Contact: http://localhost:8080/contact.html"
echo "   • API:     http://localhost:8003/health"
echo ""
echo "📖 For more info: cat $REPO_ROOT/WEBSITE_SETUP.md"
echo ""
