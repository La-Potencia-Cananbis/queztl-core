#!/bin/bash

################################################################################
# 🗺️ GIS Studio - Quick Ubuntu VM Deploy
# One-command deployment to Ubuntu VM
################################################################################

set -e

if [ $# -lt 1 ]; then
    echo "Usage: ./deploy-to-ubuntu-vm.sh <vm-ip> [username]"
    echo ""
    echo "Examples:"
    echo "  ./deploy-to-ubuntu-vm.sh 192.168.1.100"
    echo "  ./deploy-to-ubuntu-vm.sh 192.168.1.100 ubuntu"
    echo ""
    exit 1
fi

VM_IP=$1
VM_USER=${2:-ubuntu}
VM_USER_AT_IP="${VM_USER}@${VM_IP}"
PROJECT_PATH="/opt/gis-studio"

echo "
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🚀 GIS STUDIO - DEPLOY TO UBUNTU VM                           ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"

echo "📍 Target VM: $VM_USER_AT_IP"
echo "📁 Install Path: $PROJECT_PATH"
echo ""

# Step 1: Test connection
echo "🔌 Testing connection to VM..."
if ! ssh -o ConnectTimeout=5 $VM_USER_AT_IP "echo '✅ Connected'" 2>/dev/null; then
    echo "❌ Cannot connect to $VM_USER_AT_IP"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check VM IP address is correct"
    echo "  2. Ensure SSH is enabled on the VM"
    echo "  3. Check firewall allows SSH (port 22)"
    echo ""
    exit 1
fi

echo "✅ SSH connection successful"
echo ""

# Step 2: Create directory and upload files
echo "📦 Uploading GIS Studio files..."
echo "   Creating directory on VM..."
ssh $VM_USER_AT_IP "mkdir -p $PROJECT_PATH && chmod 755 $PROJECT_PATH"

echo "   Uploading backend files..."
scp -r backend $VM_USER_AT_IP:$PROJECT_PATH/ 2>/dev/null || echo "   (backend may not exist yet)"

echo "   Uploading frontend files..."
scp -r frontend $VM_USER_AT_IP:$PROJECT_PATH/ 2>/dev/null || echo "   (frontend may not exist yet)"

echo "   Uploading launch scripts..."
scp start-gis-studio.sh launch-gis-studio.sh $VM_USER_AT_IP:$PROJECT_PATH/ 2>/dev/null || true

echo "✅ Files uploaded"
echo ""

# Step 3: Run installation script
echo "⚙️  Running installation script..."
echo "   This may take a few minutes..."
echo ""

ssh $VM_USER_AT_IP << 'EOF'
#!/bin/bash
set -e

PROJECT_DIR="/opt/gis-studio"
cd $PROJECT_DIR

# Update system
echo "📦 Updating system packages..."
sudo apt-get update -qq
sudo apt-get upgrade -y -qq

# Install Python
echo "🐍 Installing Python and dependencies..."
sudo apt-get install -y -qq \
    python3 python3-pip python3-venv \
    build-essential curl wget git

# Create venv
echo "🔧 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install packages
echo "📚 Installing Python packages..."
pip install --quiet --upgrade pip

pip install --quiet \
    fastapi uvicorn websockets python-multipart aiofiles \
    numpy scipy scikit-learn pandas matplotlib seaborn plotly \
    shapely rasterio pyproj opencv-python

echo "✅ Installation complete"
EOF

echo "✅ Installation finished"
echo ""

# Step 4: Create systemd services
echo "🔧 Configuring systemd services..."
ssh $VM_USER_AT_IP << EOF
sudo tee /etc/systemd/system/gis-studio.service > /dev/null <<'SERVICE'
[Unit]
Description=QuetzalCore GIS Studio
After=network.target

[Service]
Type=simple
User=$VM_USER
WorkingDirectory=$PROJECT_PATH
Environment="PATH=$PROJECT_PATH/venv/bin"
ExecStart=$PROJECT_PATH/venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

sudo tee /etc/systemd/system/gis-studio-frontend.service > /dev/null <<'SERVICE'
[Unit]
Description=QuetzalCore GIS Studio Frontend
After=network.target

[Service]
Type=simple
User=$VM_USER
WorkingDirectory=$PROJECT_PATH/frontend
ExecStart=python3 -m http.server 8080
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl daemon-reload
sudo systemctl enable gis-studio gis-studio-frontend

echo "✅ Services configured"
EOF

echo "✅ Systemd services created"
echo ""

# Step 5: Start services
echo "🚀 Starting services..."
ssh $VM_USER_AT_IP "sudo systemctl start gis-studio gis-studio-frontend"
sleep 3

# Step 6: Verify services
echo "✅ Verifying services..."
ssh $VM_USER_AT_IP "sudo systemctl status gis-studio --no-pager | head -5"
echo ""

echo "
╔═══════════════════════════════════════════════════════════════════╗
║                   ✅ DEPLOYMENT COMPLETE!                        ║
╚═══════════════════════════════════════════════════════════════════╝
"

echo "🎯 Access your GIS Studio:"
echo ""
echo "🚀 Interactive API Tester:"
echo "   http://$VM_IP:8080/gis-studio-dashboard.html"
echo ""
echo "🎨 Information Dashboard:"
echo "   http://$VM_IP:8080/gis-studio.html"
echo ""
echo "📚 API Documentation:"
echo "   http://$VM_IP:8000/docs"
echo ""
echo "📊 Useful Commands:"
echo ""
echo "   SSH into VM:"
echo "   ssh $VM_USER_AT_IP"
echo ""
echo "   View backend logs:"
echo "   ssh $VM_USER_AT_IP 'sudo journalctl -u gis-studio -f'"
echo ""
echo "   View frontend logs:"
echo "   ssh $VM_USER_AT_IP 'sudo journalctl -u gis-studio-frontend -f'"
echo ""
echo "   Restart services:"
echo "   ssh $VM_USER_AT_IP 'sudo systemctl restart gis-studio gis-studio-frontend'"
echo ""
echo "   Check service status:"
echo "   ssh $VM_USER_AT_IP 'sudo systemctl status gis-studio gis-studio-frontend'"
echo ""
echo "✨ Everything is JODIDO! 🔥"
echo ""
