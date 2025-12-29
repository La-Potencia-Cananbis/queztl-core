#!/bin/bash

################################################################################
# 🗺️ GIS Studio - Ubuntu VM Installation Script
# Complete setup for Ubuntu testing environment
################################################################################

set -e

echo "
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🗺️  GIS STUDIO - UBUNTU VM INSTALLATION 🚀                    ║
║                                                                   ║
║      Installing QuetzalCore GIS Studio on Ubuntu                ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 STEP 1: System Update${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

echo -e "${BLUE}📋 STEP 2: Install Python & Dependencies${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Installing Python 3.9+ and essential tools..."
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    curl \
    wget \
    git \
    nano \
    tmux

echo -e "${GREEN}✅ Basic dependencies installed${NC}"

echo -e "${BLUE}📋 STEP 3: Create Project Directory${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
PROJECT_DIR="/opt/gis-studio"
echo "Creating project directory at $PROJECT_DIR..."
sudo mkdir -p $PROJECT_DIR
sudo chown -R $(whoami):$(whoami) $PROJECT_DIR
cd $PROJECT_DIR

echo -e "${BLUE}📋 STEP 4: Clone Repository${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Cloning GIS Studio repository..."
# If you have a git repo, uncomment below
# git clone <your-repo-url> .
# For now, we'll assume files are being transferred

echo -e "${BLUE}📋 STEP 5: Create Python Virtual Environment${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment created and activated${NC}"

echo -e "${BLUE}📋 STEP 6: Install Python Dependencies${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Installing Python packages..."
pip install --upgrade pip setuptools wheel

# Core dependencies
pip install \
    fastapi \
    uvicorn \
    websockets \
    python-multipart \
    aiofiles

# Data science & GIS dependencies
pip install \
    numpy \
    scipy \
    scikit-learn \
    pandas \
    matplotlib \
    seaborn \
    plotly

# Additional scientific tools
pip install \
    shapely \
    rasterio \
    pyproj \
    opencv-python

echo -e "${GREEN}✅ Python dependencies installed${NC}"

echo -e "${BLUE}📋 STEP 7: Verify Installation${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Checking Python version..."
python3 --version
echo ""
echo "Checking installed packages..."
pip list | head -20

echo -e "${BLUE}📋 STEP 8: Setup Systemd Service${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Creating systemd service for GIS Studio..."

# Create service file
sudo tee /etc/systemd/system/gis-studio.service > /dev/null <<EOF
[Unit]
Description=QuetzalCore GIS Studio
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✅ Systemd service created${NC}"
echo "   Start with: sudo systemctl start gis-studio"
echo "   Enable at boot: sudo systemctl enable gis-studio"

echo -e "${BLUE}📋 STEP 9: Create Frontend Service${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Creating systemd service for frontend..."

sudo tee /etc/systemd/system/gis-studio-frontend.service > /dev/null <<EOF
[Unit]
Description=QuetzalCore GIS Studio Frontend
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$PROJECT_DIR/frontend
ExecStart=python3 -m http.server 8080
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✅ Frontend service created${NC}"

echo -e "${BLUE}📋 STEP 10: Enable Services${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload
echo -e "${GREEN}✅ Services ready to start${NC}"

echo -e "${BLUE}📋 STEP 11: Firewall Configuration${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Opening firewall ports..."
sudo ufw allow 8000/tcp 2>/dev/null || echo "UFW not enabled (OK)"
sudo ufw allow 8080/tcp 2>/dev/null || echo "UFW not enabled (OK)"
echo -e "${GREEN}✅ Firewall configured${NC}"

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                  ✅ INSTALLATION COMPLETE                        ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

echo -e "${GREEN}📊 NEXT STEPS:${NC}"
echo ""
echo "1. Copy GIS Studio files to the server:"
echo "   scp -r . ubuntu@<your-vm-ip>:/opt/gis-studio/"
echo ""
echo "2. SSH into your Ubuntu VM:"
echo "   ssh ubuntu@<your-vm-ip>"
echo ""
echo "3. Navigate to project directory:"
echo "   cd /opt/gis-studio"
echo "   source venv/bin/activate"
echo ""
echo "4. Start the services:"
echo "   sudo systemctl start gis-studio"
echo "   sudo systemctl start gis-studio-frontend"
echo ""
echo "5. Check service status:"
echo "   sudo systemctl status gis-studio"
echo "   sudo systemctl status gis-studio-frontend"
echo ""
echo "6. Access the dashboards:"
echo "   🚀 API Tester: http://<your-vm-ip>:8080/gis-studio-dashboard.html"
echo "   🎨 Info Page: http://<your-vm-ip>:8080/gis-studio.html"
echo ""
echo "7. View logs:"
echo "   sudo journalctl -u gis-studio -f"
echo "   sudo journalctl -u gis-studio-frontend -f"
echo ""
echo "8. Enable services at boot:"
echo "   sudo systemctl enable gis-studio"
echo "   sudo systemctl enable gis-studio-frontend"
echo ""
echo -e "${YELLOW}⚠️  NOTES:${NC}"
echo "• Make sure your VM has ports 8000 and 8080 open"
echo "• Replace <your-vm-ip> with your actual Ubuntu VM IP address"
echo "• Services will auto-restart on failure"
echo "• Check logs if services don't start"
echo ""
echo -e "${GREEN}Happy testing! 🚀✨${NC}"
echo ""
