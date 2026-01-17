#!/bin/bash
# Beast/Sloth Post-Install Setup
# Run this ON Beast/Sloth after Ubuntu Server installation

set -e

cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║  ⚡ Queztl Agent Node - Post-Install Setup                  ║
╚══════════════════════════════════════════════════════════════╝
EOF

echo ""
echo "🚀 Starting bare metal setup..."
echo ""

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install essentials ONLY
echo ""
echo "📦 Installing essential packages..."
sudo apt install -y \
    python3.12 python3.12-venv python3-pip \
    git curl wget htop \
    build-essential \
    net-tools

# Disable unnecessary services
echo ""
echo "🧹 Disabling unnecessary services..."
services=(
    "snapd"
    "cups"
    "cups-browsed"
    "bluetooth"
    "ModemManager"
    "avahi-daemon"
)

for service in "${services[@]}"; do
    sudo systemctl disable "$service" --now 2>/dev/null && echo "  ✓ Disabled: $service" || echo "  - Skipped: $service (not found)"
done

# Install Docker
echo ""
echo "🐳 Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "  ✓ Docker installed"
else
    echo "  ✓ Docker already installed"
fi

# Clone queztl-core
echo ""
echo "📥 Cloning queztl-core repository..."
cd ~
if [ ! -d "queztl-core" ]; then
    git clone https://github.com/La-Potencia-Cananbis/queztl-core.git
    echo "  ✓ Repository cloned"
else
    echo "  ✓ Repository already exists, pulling latest..."
    cd queztl-core
    git pull
    cd ~
fi

# Setup Python environment
echo ""
echo "🐍 Setting up Python environment..."
cd ~/queztl-core

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  ✓ Virtual environment created"
else
    echo "  ✓ Virtual environment already exists"
fi

source venv/bin/activate

# Install CPU-only PyTorch (faster, smaller)
echo ""
echo "📦 Installing Python packages (this may take 2-3 minutes)..."
pip install --upgrade pip --quiet
pip install \
    torch torchvision \
    pillow numpy pandas \
    --index-url https://download.pytorch.org/whl/cpu \
    --quiet

echo "  ✓ Python packages installed"

# Test agent system
echo ""
echo "🧪 Testing agent system..."
python backend/queztl_agents.py --help > /dev/null 2>&1 && echo "  ✓ Agent system ready" || echo "  ✗ Agent system test failed"

# Get system info
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 System Information:"
echo "   Hostname:  $(hostname)"
echo "   IP:        $(hostname -I | awk '{print $1}')"
echo "   OS:        $(lsb_release -d | cut -f2)"
echo "   Kernel:    $(uname -r)"
echo "   Python:    $(python3 --version)"
echo "   Disk:      $(df -h / | tail -1 | awk '{print $4}') free"
echo "   RAM:       $(free -h | grep Mem | awk '{print $7}') available"
echo ""
echo "🎮 Control from laptop:"
echo "   ssh $(whoami)@$(hostname -I | awk '{print $1}')"
echo ""
echo "🤖 Test agents:"
echo "   cd ~/queztl-core"
echo "   source venv/bin/activate"
echo "   python backend/queztl_agents.py --demo"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
