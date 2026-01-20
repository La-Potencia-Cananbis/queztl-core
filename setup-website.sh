#!/bin/bash
# Quick Setup Wizard for Queztl Dynamic Website

echo "╔═══════════════════════════════════════════════════════╗"
echo "║  🦅 QUEZTL WEBSITE SETUP WIZARD                      ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create directories
echo "📁 Creating directories..."
mkdir -p ~/queztl-core/data
mkdir -p ~/queztl-core/frontend/generated
mkdir -p ~/queztl-core/logs
mkdir -p ~/queztl-core/.config
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

read -p "Configure email now? (y/n): " CONFIGURE_EMAIL

if [ "$CONFIGURE_EMAIL" = "y" ]; then
    read -p "SMTP Server [smtp.gmail.com]: " SMTP_SERVER
    SMTP_SERVER=${SMTP_SERVER:-smtp.gmail.com}
    
    read -p "SMTP Port [587]: " SMTP_PORT
    SMTP_PORT=${SMTP_PORT:-587}
    
    read -p "Sender Email: " SENDER_EMAIL
    
    read -s -p "Sender Password (hidden): " SENDER_PASSWORD
    echo ""
    
    read -p "Recipient Email (for notifications): " RECIPIENT_EMAIL
    
    # Save to config file
    cat > ~/queztl-core/.config/email.env <<EOF
export SMTP_SERVER="$SMTP_SERVER"
export SMTP_PORT="$SMTP_PORT"
export SENDER_EMAIL="$SENDER_EMAIL"
export SENDER_PASSWORD="$SENDER_PASSWORD"
export RECIPIENT_EMAIL="$RECIPIENT_EMAIL"
EOF
    
    chmod 600 ~/queztl-core/.config/email.env
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

read -p "Do you have a DynDNS domain? (y/n): " HAS_DYNDNS

if [ "$HAS_DYNDNS" = "y" ]; then
    read -p "Enter your DynDNS domain: " DYNDNS_DOMAIN
    
    cat > ~/queztl-core/.config/dyndns.env <<EOF
export DYNDNS_DOMAIN="$DYNDNS_DOMAIN"
EOF
    
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

read -p "Do you have a Meta API key? (y/n): " HAS_META_KEY

if [ "$HAS_META_KEY" = "y" ]; then
    read -p "Enter Meta API key: " META_API_KEY
    
    cat > ~/queztl-core/.config/meta.env <<EOF
export META_API_KEY="$META_API_KEY"
EOF
    
    chmod 600 ~/queztl-core/.config/meta.env
    echo -e "${GREEN}✅ Meta API key saved${NC}"
else
    echo -e "${YELLOW}⚠️  No Meta API key (Facebook posting disabled)${NC}"
fi
echo ""

# Generate startup script with configs
echo "🔧 Generating startup script..."

cat > ~/queztl-core/start.sh <<'EOFSTART'
#!/bin/bash
# Auto-generated startup script

# Load configurations
[ -f ~/.config/email.env ] && source ~/.config/email.env
[ -f ~/.config/dyndns.env ] && source ~/.config/dyndns.env
[ -f ~/.config/meta.env ] && source ~/.config/meta.env

# Start services
cd ~/queztl-core
./start-services.sh
EOFSTART

chmod +x ~/queztl-core/start.sh

echo -e "${GREEN}✅ Startup script created: ~/queztl-core/start.sh${NC}"
echo ""

# Summary
echo "╔═══════════════════════════════════════════════════════╗"
echo "║  ✅ SETUP COMPLETE                                    ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "📊 Configuration Summary:"
echo "─────────────────────────────────────────────────────────"

if [ -f ~/queztl-core/.config/email.env ]; then
    source ~/queztl-core/.config/email.env
    echo -e "${GREEN}✅ Email configured: $SENDER_EMAIL${NC}"
else
    echo -e "${YELLOW}⚠️  Email not configured${NC}"
fi

if [ -f ~/queztl-core/.config/dyndns.env ]; then
    source ~/queztl-core/.config/dyndns.env
    echo -e "${GREEN}✅ DynDNS: $DYNDNS_DOMAIN${NC}"
else
    echo -e "${YELLOW}⚠️  DynDNS not configured${NC}"
fi

if [ -f ~/queztl-core/.config/meta.env ]; then
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
echo "   cd ~/queztl-core && ./start.sh"
echo ""
echo "🌐 Access points (after starting):"
echo "   • Web:     http://localhost:8080"
echo "   • Contact: http://localhost:8080/contact.html"
echo "   • API:     http://localhost:8003/health"
echo ""
echo "📖 For more info: cat ~/queztl-core/WEBSITE_SETUP.md"
echo ""
