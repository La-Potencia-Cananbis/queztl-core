#!/bin/bash
# 🌐 DEPLOY QUETZALCORE TO RGIS.COM
# Full distributed deployment with hypervisor support

set -e

echo "=================================="
echo "🚀 DEPLOYING TO RGIS.COM"
echo "=================================="

# Configuration
RGIS_MASTER_IP="${RGIS_MASTER_IP:-rgis.com}"
RGIS_WORKER_IPS="${RGIS_WORKER_IPS:-}"  # Comma-separated list
DEPLOY_USER="${DEPLOY_USER:-root}"
INSTALL_DIR="/opt/quetzalcore"

echo ""
echo "📋 Configuration:"
echo "   Master: $RGIS_MASTER_IP"
echo "   Workers: ${RGIS_WORKER_IPS:-none specified}"
echo "   Install Dir: $INSTALL_DIR"
echo ""

# 1. PREPARE DEPLOYMENT PACKAGE
echo "📦 Creating deployment package..."
rm -rf /tmp/quetzalcore-deploy
mkdir -p /tmp/quetzalcore-deploy

# Copy essential files
cp -r backend /tmp/quetzalcore-deploy/
cp requirements.txt /tmp/quetzalcore-deploy/ 2>/dev/null || echo "requirements: torch fastapi uvicorn websockets sqlalchemy asyncpg psutil pillow numpy aiofiles python-multipart trimesh scikit-learn scipy matplotlib seaborn plotly redis numba shapely rasterio pyproj opencv-python" > /tmp/quetzalcore-deploy/requirements.txt

# Copy mining/GIS engines
cp register_rgis_worker.py /tmp/quetzalcore-deploy/
cp test_mining_api.py /tmp/quetzalcore-deploy/

# Create systemd service files
cat > /tmp/quetzalcore-deploy/quetzalcore-master.service << 'EOF'
[Unit]
Description=QuetzalCore Master Coordinator
After=network.target

[Service]
Type=simple
User=quetzalcore
WorkingDirectory=/opt/quetzalcore
Environment="PATH=/opt/quetzalcore/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/opt/quetzalcore/venv/bin/python -m backend.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

cat > /tmp/quetzalcore-deploy/quetzalcore-worker.service << 'EOF'
[Unit]
Description=QuetzalCore Worker Node
After=network.target

[Service]
Type=simple
User=quetzalcore
WorkingDirectory=/opt/quetzalcore
Environment="PATH=/opt/quetzalcore/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="MASTER_URL=http://MASTER_IP:8000"
ExecStart=/opt/quetzalcore/venv/bin/python register_rgis_worker.py $MASTER_URL --domain RGIS.com
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create install script
cat > /tmp/quetzalcore-deploy/install.sh << 'INSTALLEOF'
#!/bin/bash
set -e

INSTALL_DIR="/opt/quetzalcore"
NODE_TYPE="${1:-worker}"  # master or worker
MASTER_IP="${2:-localhost}"

echo "🔧 Installing QuetzalCore ($NODE_TYPE mode)..."

# Create user
useradd -r -s /bin/bash -d $INSTALL_DIR quetzalcore 2>/dev/null || true

# Create directories
mkdir -p $INSTALL_DIR
chown -R quetzalcore:quetzalcore $INSTALL_DIR

# Copy files
cp -r backend $INSTALL_DIR/
cp requirements.txt $INSTALL_DIR/
cp register_rgis_worker.py $INSTALL_DIR/
cp test_mining_api.py $INSTALL_DIR/

# Install Python 3.11+
if ! command -v python3.11 &> /dev/null; then
    echo "📥 Installing Python 3.11..."
    apt-get update
    apt-get install -y python3.11 python3.11-venv python3.11-dev build-essential
fi

# Create venv
cd $INSTALL_DIR
sudo -u quetzalcore python3.11 -m venv venv

# Install dependencies
echo "📦 Installing Python packages..."
sudo -u quetzalcore $INSTALL_DIR/venv/bin/pip install --upgrade pip
sudo -u quetzalcore $INSTALL_DIR/venv/bin/pip install -r requirements.txt

# Install systemd service
if [ "$NODE_TYPE" == "master" ]; then
    cp quetzalcore-master.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable quetzalcore-master
    systemctl start quetzalcore-master
    echo "✅ Master coordinator started on port 8000"
else
    # Update master IP in worker service
    sed "s/MASTER_IP/$MASTER_IP/g" quetzalcore-worker.service > /etc/systemd/system/quetzalcore-worker.service
    systemctl daemon-reload
    systemctl enable quetzalcore-worker
    systemctl start quetzalcore-worker
    echo "✅ Worker registered with master at $MASTER_IP"
fi

echo ""
echo "✅ QuetzalCore installed successfully!"
INSTALLEOF

chmod +x /tmp/quetzalcore-deploy/install.sh

# Create tarball
cd /tmp
tar czf quetzalcore-deploy.tar.gz quetzalcore-deploy/
echo "✅ Package created: /tmp/quetzalcore-deploy.tar.gz"

# 2. DEPLOY TO MASTER
echo ""
echo "🚀 Deploying to MASTER: $RGIS_MASTER_IP"
echo ""

if [ "$RGIS_MASTER_IP" != "localhost" ] && [ "$RGIS_MASTER_IP" != "rgis.com" ]; then
    # Copy to master
    scp /tmp/quetzalcore-deploy.tar.gz $DEPLOY_USER@$RGIS_MASTER_IP:/tmp/
    
    # Install on master
    ssh $DEPLOY_USER@$RGIS_MASTER_IP << 'EOSSH'
cd /tmp
tar xzf quetzalcore-deploy.tar.gz
cd quetzalcore-deploy
chmod +x install.sh
./install.sh master
EOSSH
    
    echo "✅ Master deployed!"
else
    echo "⚠️  Master IP is '$RGIS_MASTER_IP' - skipping remote deployment"
    echo "    To deploy manually:"
    echo "    1. Copy /tmp/quetzalcore-deploy.tar.gz to your RGIS master server"
    echo "    2. Extract: tar xzf quetzalcore-deploy.tar.gz"
    echo "    3. Run: cd quetzalcore-deploy && sudo ./install.sh master"
fi

# 3. DEPLOY TO WORKERS
if [ -n "$RGIS_WORKER_IPS" ]; then
    echo ""
    echo "🚀 Deploying to WORKERS..."
    echo ""
    
    IFS=',' read -ra WORKERS <<< "$RGIS_WORKER_IPS"
    for WORKER_IP in "${WORKERS[@]}"; do
        echo "📡 Deploying to worker: $WORKER_IP"
        
        # Copy to worker
        scp /tmp/quetzalcore-deploy.tar.gz $DEPLOY_USER@$WORKER_IP:/tmp/
        
        # Install on worker
        ssh $DEPLOY_USER@$WORKER_IP << EOSSH
cd /tmp
tar xzf quetzalcore-deploy.tar.gz
cd quetzalcore-deploy
chmod +x install.sh
./install.sh worker $RGIS_MASTER_IP
EOSSH
        
        echo "✅ Worker $WORKER_IP deployed!"
    done
else
    echo ""
    echo "⚠️  No worker IPs specified"
    echo "    To add workers later:"
    echo "    1. Copy /tmp/quetzalcore-deploy.tar.gz to worker server"
    echo "    2. Extract: tar xzf quetzalcore-deploy.tar.gz"
    echo "    3. Run: cd quetzalcore-deploy && sudo ./install.sh worker MASTER_IP"
fi

# 4. SETUP SUMMARY
echo ""
echo "=================================="
echo "✅ DEPLOYMENT COMPLETE"
echo "=================================="
echo ""
echo "🌐 Access Points:"
echo "   Master API: http://$RGIS_MASTER_IP:8000"
echo "   Health: http://$RGIS_MASTER_IP:8000/api/health"
echo "   Network Status: http://$RGIS_MASTER_IP:8000/api/v1.2/network/status"
echo "   Mining API: http://$RGIS_MASTER_IP:8000/api/mining/mag-survey"
echo ""
echo "📊 Check Status:"
echo "   curl http://$RGIS_MASTER_IP:8000/api/v1.2/network/status"
echo ""
echo "🔧 Management Commands:"
echo "   Master: systemctl status quetzalcore-master"
echo "   Worker: systemctl status quetzalcore-worker"
echo "   Logs: journalctl -u quetzalcore-master -f"
echo ""
echo "🧲 Mining APIs Ready:"
echo "   - POST /api/mining/mag-survey (upload surveys)"
echo "   - POST /api/mining/discriminate (mineral ID)"
echo "   - POST /api/mining/target-drills (drill targets)"
echo "   - GET  /api/mining/survey-cost (cost analysis)"
echo ""
