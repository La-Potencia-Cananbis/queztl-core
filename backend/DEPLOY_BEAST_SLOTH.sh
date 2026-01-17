#!/bin/bash
# BEAST & SLOTH - BARE METAL DEPLOYMENT
# Ultra-lightweight setup for maximum speed

set -e

cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║  ⚡ BEAST & SLOTH - BARE METAL SETUP                        ║
║  Goal: Maximum speed, minimal bloat                         ║
╚══════════════════════════════════════════════════════════════╝
EOF

echo ""
echo "📋 DEPLOYMENT OPTIONS:"
echo ""
echo "1. Ubuntu Server 24.04 LTS (RECOMMENDED)"
echo "   - No GUI, CLI only"
echo "   - ~512MB RAM usage"
echo "   - APT package manager"
echo "   - Boot time: 5-10 seconds"
echo ""
echo "2. Debian 12 (Bookworm) Minimal"
echo "   - Even lighter than Ubuntu"
echo "   - ~400MB RAM usage"
echo "   - Rock solid stable"
echo "   - Boot time: 3-8 seconds"
echo ""
echo "3. Alpine Linux"
echo "   - Ultra lightweight (~130MB RAM)"
echo "   - 5MB ISO size"
echo "   - Boot time: 2-5 seconds"
echo "   - Best for containers/Docker"
echo ""
echo "4. Current OS (Strip Down)"
echo "   - Remove bloat from existing install"
echo "   - Keep what works"
echo "   - Faster than reinstall"
echo ""

read -p "Choose option [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "🚀 Ubuntu Server 24.04 LTS Selected"
        echo ""
        echo "📥 Download ISO:"
        echo "   https://ubuntu.com/download/server"
        echo ""
        echo "💾 Installation Steps:"
        echo "   1. Create bootable USB (use balenaEtcher)"
        echo "   2. Boot from USB"
        echo "   3. Select: Install Ubuntu Server (minimized)"
        echo "   4. Network: Auto-configure"
        echo "   5. Storage: Use entire disk"
        echo "   6. Profile: Create user"
        echo "   7. SSH: Enable OpenSSH server"
        echo "   8. Packages: SKIP ALL (we'll install manually)"
        echo ""
        echo "⚡ Post-install commands (save these):"
        cat > /tmp/beast-post-install.sh << 'INSTALL'
#!/bin/bash
# Run this after Ubuntu Server installation

# Update system
sudo apt update && sudo apt upgrade -y

# Install only essentials
sudo apt install -y \
    python3.12 python3.12-venv python3-pip \
    git curl wget htop \
    build-essential

# Disable unnecessary services
sudo systemctl disable snapd --now || true
sudo systemctl disable cups --now || true
sudo systemctl disable bluetooth --now || true

# Install Docker (optional, lightweight)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Clone queztl-core
cd ~
git clone https://github.com/La-Potencia-Cananbis/queztl-core.git
cd queztl-core

# Setup Python
python3 -m venv venv
source venv/bin/activate
pip install torch torchvision pillow numpy --index-url https://download.pytorch.org/whl/cpu

echo ""
echo "✅ Beast/Sloth ready!"
echo "IP: $(hostname -I | awk '{print $1}')"
INSTALL
        
        echo "Saved to: /tmp/beast-post-install.sh"
        ;;
        
    2)
        echo ""
        echo "🚀 Debian 12 Minimal Selected"
        echo ""
        echo "📥 Download ISO:"
        echo "   https://www.debian.org/CD/netinst/"
        echo "   Use: debian-12.x.x-amd64-netinst.iso"
        echo ""
        echo "💾 Installation:"
        echo "   - Choose: Standard system utilities ONLY"
        echo "   - Deselect: Desktop environment, print server"
        echo "   - Enable: SSH server"
        echo ""
        echo "⚡ Post-install commands:"
        cat > /tmp/beast-post-install.sh << 'INSTALL'
#!/bin/bash
# Debian 12 post-install

sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip git curl wget htop

# Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone and setup
cd ~
git clone https://github.com/La-Potencia-Cananbis/queztl-core.git
cd queztl-core
python3 -m venv venv
source venv/bin/activate
pip install torch torchvision pillow numpy
INSTALL
        ;;
        
    3)
        echo ""
        echo "🚀 Alpine Linux Selected (HARDCORE MODE)"
        echo ""
        echo "📥 Download:"
        echo "   https://alpinelinux.org/downloads/"
        echo "   Use: alpine-standard-3.19.x-x86_64.iso"
        echo ""
        echo "⚠️  Warning: Alpine uses apk (not apt) and musl (not glibc)"
        echo "   Some Python packages may need compilation"
        echo ""
        echo "⚡ Post-install:"
        cat > /tmp/beast-post-install.sh << 'INSTALL'
#!/bin/sh
# Alpine post-install

# Enable community repo
echo "http://dl-cdn.alpinelinux.org/alpine/v3.19/community" | sudo tee -a /etc/apk/repositories

# Install packages
sudo apk update
sudo apk add python3 py3-pip git docker

# Start Docker
sudo rc-update add docker boot
sudo service docker start

# Clone and setup
cd ~
git clone https://github.com/La-Potencia-Cananbis/queztl-core.git
cd queztl-core
python3 -m venv venv
source venv/bin/activate
pip install torch torchvision pillow numpy
INSTALL
        ;;
        
    4)
        echo ""
        echo "🧹 Stripping Current OS"
        echo ""
        echo "Detecting current OS..."
        
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            echo "Current OS: $NAME $VERSION"
        fi
        
        echo ""
        echo "⚡ Quick cleanup script:"
        cat > /tmp/beast-cleanup.sh << 'CLEANUP'
#!/bin/bash
# Strip down current installation

echo "🧹 Removing bloat..."

# Stop unnecessary services
services_to_disable=(
    "snapd"
    "cups"
    "bluetooth"
    "ModemManager"
    "avahi-daemon"
)

for service in "${services_to_disable[@]}"; do
    sudo systemctl disable "$service" --now 2>/dev/null && echo "  Disabled: $service"
done

# Remove unnecessary packages (Ubuntu/Debian)
if command -v apt &> /dev/null; then
    sudo apt autoremove -y
    sudo apt clean
    
    # Optional: Remove GUI if present
    read -p "Remove GUI/Desktop? (y/n): " remove_gui
    if [ "$remove_gui" = "y" ]; then
        sudo apt remove --purge -y \
            ubuntu-desktop \
            gnome-* \
            kde-* \
            xfce4-* 2>/dev/null
        sudo apt autoremove -y
    fi
fi

# Clear logs
sudo journalctl --vacuum-time=1d

# Show results
echo ""
echo "📊 Current resource usage:"
free -h
df -h /

echo ""
echo "✅ Cleanup complete!"
CLEANUP

        chmod +x /tmp/beast-cleanup.sh
        
        read -p "Run cleanup now? (y/n): " run_now
        if [ "$run_now" = "y" ]; then
            bash /tmp/beast-cleanup.sh
        else
            echo "Saved to: /tmp/beast-cleanup.sh"
        fi
        ;;
        
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 NEXT STEPS:"
echo ""
echo "1. For Beast/Sloth machines:"
echo "   - Boot from USB installer"
echo "   - Run post-install script"
echo "   - Note IP addresses"
echo ""
echo "2. From your laptop:"
echo "   ssh user@beast-ip"
echo "   ssh user@sloth-ip"
echo ""
echo "3. Deploy agents:"
echo "   cd queztl-core"
echo "   source venv/bin/activate"
echo "   python backend/queztl_agents.py --spawn trainer"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
