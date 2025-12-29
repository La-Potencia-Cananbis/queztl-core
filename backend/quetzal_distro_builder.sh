#!/bin/bash
"""
Quetzal Distro Builder (QDB)
Automated distro builder and BM (Build Manager) rebuilder for various Linux distributions
Supports: Alpine, Arch, Debian, Fedora, NixOS, Ubuntu
"""

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
QUETZAL_REPO="${QUETZAL_REPO:-https://github.com/SalChicanoLoco/queztl-core.git}"
BUILD_DIR="${BUILD_DIR:-/tmp/quetzal-build}"
INSTALL_DIR="${INSTALL_DIR:-/opt/quetzal}"

# Distro detection
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo $ID
    else
        echo "unknown"
    fi
}

# Distro-specific installers
install_alpine() {
    echo -e "${BLUE}Installing on Alpine Linux...${NC}"
    
    apk add --no-cache \
        python3 py3-pip \
        git build-base \
        linux-headers \
        gcc g++ \
        curl wget \
        bash \
        py3-numpy py3-scipy \
        gdal-dev geos-dev proj-dev \
        sqlite-dev postgresql-client
    
    pip3 install --upgrade pip
}

install_arch() {
    echo -e "${BLUE}Installing on Arch Linux...${NC}"
    
    pacman -Syu --noconfirm
    pacman -S --noconfirm \
        python python-pip \
        git base-devel \
        gcc \
        curl wget \
        bash \
        gdal geos proj \
        postgresql \
        sqlite
    
    pip install --upgrade pip
}

install_debian() {
    echo -e "${BLUE}Installing on Debian...${NC}"
    
    apt-get update
    apt-get install -y \
        python3 python3-pip python3-dev \
        git build-essential \
        gcc g++ \
        curl wget \
        bash \
        python3-numpy python3-scipy \
        gdal-bin libgdal-dev \
        libgeos-dev libproj-dev \
        sqlite3 postgresql-client
}

install_fedora() {
    echo -e "${BLUE}Installing on Fedora...${NC}"
    
    dnf update -y
    dnf install -y \
        python3 python3-pip \
        git gcc gcc-c++ \
        make \
        curl wget \
        bash \
        python3-numpy scipy \
        gdal-devel geos-devel proj-devel \
        sqlite-devel postgresql
}

install_nixos() {
    echo -e "${BLUE}Installing on NixOS...${NC}"
    
    # NixOS uses nix shell or configuration.nix
    echo "Please add the following to your configuration.nix:"
    cat << 'EOF'
environment.systemPackages = with pkgs; [
  python3 python3Packages.pip
  git gcc gnumake
  gdal geos proj
  postgresql sqlite
  fastapi uvicorn
];
EOF
    
    echo "Then run: sudo nixos-rebuild switch"
}

install_ubuntu() {
    echo -e "${BLUE}Installing on Ubuntu...${NC}"
    
    apt-get update
    apt-get install -y \
        python3 python3-pip python3-dev \
        git build-essential \
        gcc g++ \
        curl wget \
        bash \
        python3-numpy python3-scipy \
        gdal-bin libgdal-dev \
        libgeos-dev libproj-dev \
        sqlite3 postgresql-client \
        systemd
}

# Install Quetzal Core
install_quetzal_core() {
    echo -e "${YELLOW}Installing Quetzal Core...${NC}"
    
    mkdir -p $BUILD_DIR
    cd $BUILD_DIR
    
    if [ ! -d "queztl-core" ]; then
        git clone $QUETZAL_REPO
    fi
    
    cd queztl-core
    
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate
    
    # Install Python dependencies
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Install Quetzal
    sudo mkdir -p $INSTALL_DIR
    sudo cp -r . $INSTALL_DIR/
    
    echo -e "${GREEN}✓ Quetzal Core installed${NC}"
}

# Setup GIS Studio
setup_gis_studio() {
    echo -e "${YELLOW}Setting up GIS Studio...${NC}"
    
    cd $INSTALL_DIR
    
    # Copy frontend files
    mkdir -p frontend
    cp gis-studio*.html frontend/ 2>/dev/null || true
    cp gis-studio.css frontend/ 2>/dev/null || true
    
    # Create systemd service
    sudo tee /etc/systemd/system/gis-studio.service > /dev/null << EOF
[Unit]
Description=GIS Studio Backend
After=network.target

[Service]
Type=simple
User=quetzal
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    
    sudo tee /etc/systemd/system/gis-studio-frontend.service > /dev/null << EOF
[Unit]
Description=GIS Studio Frontend
After=network.target

[Service]
Type=simple
User=quetzal
ExecStart=/usr/bin/python3 -m http.server 8080 --directory $INSTALL_DIR/frontend
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable gis-studio gis-studio-frontend
    
    echo -e "${GREEN}✓ GIS Studio configured${NC}"
}

# Create Quetzal user
create_quetzal_user() {
    if ! id -u quetzal > /dev/null 2>&1; then
        sudo useradd -m -s /bin/bash -G sudo quetzal
        echo -e "${GREEN}✓ Created quetzal user${NC}"
    fi
}

# Show system information
show_system_info() {
    echo -e "\n${BLUE}System Information:${NC}"
    echo "Distro: $(detect_distro)"
    echo "Kernel: $(uname -r)"
    echo "CPU Cores: $(nproc)"
    echo "RAM: $(free -h | awk 'NR==2 {print $2}')"
    echo "Disk: $(df -h / | awk 'NR==2 {print $2}')"
    echo ""
}

# Main installation flow
main() {
    echo -e "${BLUE}"
    cat << 'EOF'
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   🗺️  QUETZAL DISTRO BUILDER (QDB)                   ║
║      Rebuild BM with Your Preferred Distro           ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    show_system_info
    
    DISTRO=$(detect_distro)
    echo -e "${YELLOW}Detected: $DISTRO${NC}\n"
    
    # Install distro-specific packages
    case $DISTRO in
        alpine)
            install_alpine
            ;;
        arch)
            install_arch
            ;;
        debian)
            install_debian
            ;;
        fedora)
            install_fedora
            ;;
        nixos)
            install_nixos
            exit 0
            ;;
        ubuntu)
            install_ubuntu
            ;;
        *)
            echo -e "${RED}Unsupported distro: $DISTRO${NC}"
            exit 1
            ;;
    esac
    
    echo -e "${GREEN}✓ System packages installed${NC}\n"
    
    # Create quetzal user
    create_quetzal_user
    
    # Install Quetzal Core
    install_quetzal_core
    
    # Setup GIS Studio
    setup_gis_studio
    
    # Final status
    echo -e "\n${GREEN}"
    cat << EOF
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║          ✅ BUILD COMPLETE!                           ║
║                                                       ║
║  Your Quetzal system is ready on $DISTRO          ║
║                                                       ║
║  Next steps:                                         ║
║  1. Start services:                                  ║
║     sudo systemctl start gis-studio                  ║
║     sudo systemctl start gis-studio-frontend         ║
║                                                       ║
║  2. Access dashboards:                               ║
║     Frontend: http://localhost:8080                  ║
║     Backend API: http://localhost:8000               ║
║     API Docs: http://localhost:8000/docs             ║
║                                                       ║
║  3. View logs:                                        ║
║     sudo journalctl -u gis-studio -f                 ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Run main
main "$@"
