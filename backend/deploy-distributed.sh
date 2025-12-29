#!/bin/bash
# 🚀 DEPLOY QUETZALCORE DISTRIBUTED SYSTEM
# Deploy master on YOUR domain, connect RGIS.com workers for training

set -e

echo "=========================================="
echo "🚀 QUETZALCORE DISTRIBUTED DEPLOYMENT"
echo "=========================================="

# YOUR CONFIGURATION - EDIT THESE
YOUR_DOMAIN="${YOUR_DOMAIN:-your-domain.com}"           # Your production domain
YOUR_MASTER_IP="${YOUR_MASTER_IP:-}"                    # Your master server IP
RGIS_TRAINING_NODES="${RGIS_TRAINING_NODES:-}"         # RGIS.com worker IPs for training (comma-separated)
DEPLOY_USER="${DEPLOY_USER:-root}"
INSTALL_DIR="/opt/quetzalcore"

echo ""
echo "📋 Configuration:"
echo "   YOUR Domain: $YOUR_DOMAIN"
echo "   YOUR Master: ${YOUR_MASTER_IP:-not set}"
echo "   RGIS Training Workers: ${RGIS_TRAINING_NODES:-none}"
echo ""

if [ -z "$YOUR_MASTER_IP" ]; then
    echo "❌ ERROR: Set YOUR_MASTER_IP environment variable"
    echo "   Example: export YOUR_MASTER_IP=192.168.1.100"
    echo "   Or: export YOUR_MASTER_IP=api.yourdomain.com"
    exit 1
fi

# 1. CREATE DEPLOYMENT PACKAGE
echo "📦 Creating deployment package..."
rm -rf /tmp/quetzalcore-deploy
mkdir -p /tmp/quetzalcore-deploy

# Copy backend
cp -r backend /tmp/quetzalcore-deploy/

# Create requirements.txt if missing
if [ ! -f requirements.txt ]; then
    cat > /tmp/quetzalcore-deploy/requirements.txt << 'EOF'
torch>=2.0.0
torchvision
fastapi>=0.104.0
uvicorn[standard]
websockets
sqlalchemy>=2.0.0
asyncpg
psutil
pillow
numpy
aiofiles
python-multipart
trimesh
transformers
diffusers
accelerate
scikit-learn
scipy
matplotlib
seaborn
plotly
redis
numba
shapely
rasterio
pyproj
opencv-python
EOF
else
    cp requirements.txt /tmp/quetzalcore-deploy/
fi

# Copy scripts
cp register_rgis_worker.py /tmp/quetzalcore-deploy/
cp sync_rgis_data.py /tmp/quetzalcore-deploy/
cp rgis_data_server.py /tmp/quetzalcore-deploy/
cp test_mining_api.py /tmp/quetzalcore-deploy/ 2>/dev/null || true

# Create master systemd service
cat > /tmp/quetzalcore-deploy/quetzalcore-master.service << 'EOF'
[Unit]
Description=QuetzalCore Master Coordinator
After=network.target

[Service]
Type=simple
User=quetzalcore
WorkingDirectory=/opt/quetzalcore
Environment="PATH=/opt/quetzalcore/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONPATH=/opt/quetzalcore"
ExecStart=/opt/quetzalcore/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Create worker systemd service
cat > /tmp/quetzalcore-deploy/quetzalcore-worker.service << 'EOF'
[Unit]
Description=QuetzalCore Worker Node (Training)
After=network.target

[Service]
Type=simple
User=quetzalcore
WorkingDirectory=/opt/quetzalcore
Environment="PATH=/opt/quetzalcore/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONPATH=/opt/quetzalcore"
Environment="MASTER_URL=__MASTER_URL__"
ExecStart=/opt/quetzalcore/venv/bin/python register_rgis_worker.py ${MASTER_URL} --domain RGIS.training --port 8001
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Create master install script
cat > /tmp/quetzalcore-deploy/install-master.sh << 'INSTALLMASTER'
#!/bin/bash
set -e

INSTALL_DIR="/opt/quetzalcore"

echo "🏠 Installing QuetzalCore MASTER on YOUR domain..."

# Create quetzalcore user
useradd -r -s /bin/bash -d $INSTALL_DIR quetzalcore 2>/dev/null || echo "User exists"

# Create directories
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

# Copy files
cp -r /tmp/quetzalcore-deploy/backend .
cp /tmp/quetzalcore-deploy/requirements.txt .
cp /tmp/quetzalcore-deploy/*.py . 2>/dev/null || true

# Install Python 3.11+ if needed
if ! command -v python3.11 &> /dev/null && ! command -v python3.10 &> /dev/null; then
    echo "📥 Installing Python..."
    if command -v apt-get &> /dev/null; then
        apt-get update
        apt-get install -y python3.11 python3.11-venv python3.11-dev build-essential
        PYTHON_BIN=python3.11
    elif command -v yum &> /dev/null; then
        yum install -y python3.11 python3.11-devel gcc
        PYTHON_BIN=python3.11
    fi
else
    PYTHON_BIN=$(command -v python3.11 || command -v python3.10)
fi

# Create venv
echo "🐍 Creating virtual environment..."
sudo -u quetzalcore $PYTHON_BIN -m venv venv

# Install dependencies
echo "📦 Installing dependencies (this may take a while)..."
sudo -u quetzalcore $INSTALL_DIR/venv/bin/pip install --upgrade pip wheel
sudo -u quetzalcore $INSTALL_DIR/venv/bin/pip install -r requirements.txt

# Set permissions
chown -R quetzalcore:quetzalcore $INSTALL_DIR

# Install systemd service
echo "⚙️  Installing systemd service..."
cp /tmp/quetzalcore-deploy/quetzalcore-master.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable quetzalcore-master
systemctl restart quetzalcore-master

# Wait for startup
echo "⏳ Waiting for service to start..."
sleep 5

# Check status
if systemctl is-active --quiet quetzalcore-master; then
    echo ""
    echo "✅ MASTER INSTALLED AND RUNNING!"
    echo ""
    echo "🌐 Access Points:"
    echo "   API: http://$(hostname -I | awk '{print $1}'):8000"
    echo "   Health: http://$(hostname -I | awk '{print $1}'):8000/api/health"
    echo "   Network: http://$(hostname -I | awk '{print $1}'):8000/api/v1.2/network/status"
    echo "   Mining: http://$(hostname -I | awk '{print $1}'):8000/api/mining/mag-survey"
    echo ""
    echo "📊 Check logs:"
    echo "   journalctl -u quetzalcore-master -f"
    echo ""
else
    echo "❌ Service failed to start. Check logs:"
    echo "   journalctl -u quetzalcore-master -xe"
    exit 1
fi
INSTALLMASTER

# Create worker install script
cat > /tmp/quetzalcore-deploy/install-worker.sh << 'INSTALLWORKER'
#!/bin/bash
set -e

MASTER_URL="${1:-http://localhost:8000}"
INSTALL_DIR="/opt/quetzalcore"

echo "🔧 Installing QuetzalCore WORKER (training node)..."
echo "   Master: $MASTER_URL"

# Create quetzalcore user
useradd -r -s /bin/bash -d $INSTALL_DIR quetzalcore 2>/dev/null || echo "User exists"

# Create directories
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

# Copy files
cp -r /tmp/quetzalcore-deploy/backend .
cp /tmp/quetzalcore-deploy/requirements.txt .
cp /tmp/quetzalcore-deploy/register_rgis_worker.py .

# Install Python
if ! command -v python3.11 &> /dev/null && ! command -v python3.10 &> /dev/null; then
    echo "📥 Installing Python..."
    if command -v apt-get &> /dev/null; then
        apt-get update
        apt-get install -y python3.11 python3.11-venv python3.11-dev build-essential
        PYTHON_BIN=python3.11
    elif command -v yum &> /dev/null; then
        yum install -y python3.11 python3.11-devel gcc
        PYTHON_BIN=python3.11
    fi
else
    PYTHON_BIN=$(command -v python3.11 || command -v python3.10)
fi

# Create venv
echo "🐍 Creating virtual environment..."
sudo -u quetzalcore $PYTHON_BIN -m venv venv

# Install dependencies (lighter for workers)
echo "📦 Installing dependencies..."
sudo -u quetzalcore $INSTALL_DIR/venv/bin/pip install --upgrade pip wheel
sudo -u quetzalcore $INSTALL_DIR/venv/bin/pip install torch numpy psutil aiohttp

# Set permissions
chown -R quetzalcore:quetzalcore $INSTALL_DIR

# Install systemd service with master URL
echo "⚙️  Installing systemd service..."
sed "s|__MASTER_URL__|$MASTER_URL|g" /tmp/quetzalcore-deploy/quetzalcore-worker.service > /etc/systemd/system/quetzalcore-worker.service
systemctl daemon-reload
systemctl enable quetzalcore-worker
systemctl restart quetzalcore-worker

# Check status
sleep 3
if systemctl is-active --quiet quetzalcore-worker; then
    echo ""
    echo "✅ WORKER REGISTERED!"
    echo "   Connected to: $MASTER_URL"
    echo ""
    echo "📊 Check logs:"
    echo "   journalctl -u quetzalcore-worker -f"
    echo ""
else
    echo "❌ Worker failed to start. Check logs:"
    echo "   journalctl -u quetzalcore-worker -xe"
    exit 1
fi
INSTALLWORKER

chmod +x /tmp/quetzalcore-deploy/install-master.sh
chmod +x /tmp/quetzalcore-deploy/install-worker.sh

# Create deployment tarball
cd /tmp
tar czf quetzalcore-deploy.tar.gz quetzalcore-deploy/
echo "✅ Deployment package: /tmp/quetzalcore-deploy.tar.gz"

# 2. DEPLOY MASTER TO YOUR DOMAIN
echo ""
echo "=========================================="
echo "🏠 DEPLOYING MASTER TO YOUR DOMAIN"
echo "=========================================="
echo ""

echo "📤 Copying to $YOUR_MASTER_IP..."
scp /tmp/quetzalcore-deploy.tar.gz $DEPLOY_USER@$YOUR_MASTER_IP:/tmp/ || {
    echo "❌ Could not copy to $YOUR_MASTER_IP"
    echo ""
    echo "🔧 MANUAL DEPLOYMENT:"
    echo "   1. Copy /tmp/quetzalcore-deploy.tar.gz to your server"
    echo "   2. On server: cd /tmp && tar xzf quetzalcore-deploy.tar.gz"
    echo "   3. Run: sudo bash /tmp/quetzalcore-deploy/install-master.sh"
    echo ""
    exit 1
}

echo "🔧 Installing master..."
ssh $DEPLOY_USER@$YOUR_MASTER_IP << 'EOSSH'
cd /tmp
tar xzf quetzalcore-deploy.tar.gz
bash /tmp/quetzalcore-deploy/install-master.sh
EOSSH

MASTER_URL="http://$YOUR_MASTER_IP:8000"
echo ""
echo "✅ MASTER DEPLOYED!"
echo "   URL: $MASTER_URL"

# 3. DEPLOY WORKERS TO RGIS.COM (for training)
if [ -n "$RGIS_TRAINING_NODES" ]; then
    echo ""
    echo "=========================================="
    echo "🎓 DEPLOYING TRAINING WORKERS TO RGIS"
    echo "=========================================="
    echo ""
    
    IFS=',' read -ra WORKERS <<< "$RGIS_TRAINING_NODES"
    WORKER_COUNT=0
    
    for WORKER_IP in "${WORKERS[@]}"; do
        WORKER_IP=$(echo "$WORKER_IP" | xargs)  # Trim whitespace
        echo "📡 Deploying training worker to: $WORKER_IP"
        
        # Copy package
        scp /tmp/quetzalcore-deploy.tar.gz $DEPLOY_USER@$WORKER_IP:/tmp/ || {
            echo "⚠️  Could not reach $WORKER_IP, skipping..."
            continue
        }
        
        # Install worker
        ssh $DEPLOY_USER@$WORKER_IP << EOSSH
cd /tmp
tar xzf quetzalcore-deploy.tar.gz
bash /tmp/quetzalcore-deploy/install-worker.sh $MASTER_URL
EOSSH
        
        echo "✅ Worker $WORKER_IP deployed!"
        WORKER_COUNT=$((WORKER_COUNT + 1))
    done
    
    echo ""
    echo "✅ Deployed $WORKER_COUNT training workers"
else
    echo ""
    echo "⚠️  No RGIS training nodes specified"
    echo ""
    echo "🔧 TO ADD TRAINING WORKERS LATER:"
    echo "   1. SSH to RGIS.com worker node"
    echo "   2. Copy /tmp/quetzalcore-deploy.tar.gz to it"
    echo "   3. Extract: tar xzf quetzalcore-deploy.tar.gz"
    echo "   4. Run: sudo bash /tmp/quetzalcore-deploy/install-worker.sh $MASTER_URL"
fi

# 4. FINAL SUMMARY
echo ""
echo "=========================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "🏠 YOUR MASTER (Production):"
echo "   Domain: $YOUR_DOMAIN"
echo "   API: $MASTER_URL"
echo "   Health: $MASTER_URL/api/health"
echo "   Network Status: $MASTER_URL/api/v1.2/network/status"
echo ""
echo "🎓 RGIS.COM TRAINING WORKERS:"
echo "   Workers: ${RGIS_TRAINING_NODES:-none deployed yet}"
echo ""
echo "🧲 MINING/GIS APIS:"
echo "   Upload Survey: POST $MASTER_URL/api/mining/mag-survey"
echo "   Discriminate: POST $MASTER_URL/api/mining/discriminate"
echo "   Drill Targets: POST $MASTER_URL/api/mining/target-drills"
echo "   Cost Analysis: GET $MASTER_URL/api/mining/survey-cost"
echo ""
echo "📊 CHECK STATUS:"
echo "   curl $MASTER_URL/api/v1.2/network/status | jq"
echo ""
echo "🔧 MANAGE SERVICES:"
echo "   Master: ssh $DEPLOY_USER@$YOUR_MASTER_IP systemctl status quetzalcore-master"
echo "   Worker: ssh $DEPLOY_USER@WORKER_IP systemctl status quetzalcore-worker"
echo "   Logs: ssh $DEPLOY_USER@$YOUR_MASTER_IP journalctl -u quetzalcore-master -f"
echo ""
echo "🚀 READY FOR PRODUCTION!"
echo ""
