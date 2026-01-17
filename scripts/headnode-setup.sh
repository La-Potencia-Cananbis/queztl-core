#!/bin/bash
# HEADNODE SETUP - Command Center Configuration
# Run this on the master control node (your main coordination machine)

set -e

cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║  🎮 QUEZTL HEADNODE - COMMAND CENTER SETUP                  ║
╚══════════════════════════════════════════════════════════════╝
EOF

echo ""
echo "This will configure this machine as the Queztl cluster headnode."
echo "The headnode coordinates all worker nodes and provides:"
echo "  • Central monitoring dashboard"
echo "  • Agent coordination"
echo "  • Job scheduling"
echo "  • API gateway"
echo ""

read -p "Continue? (y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo "🚀 Setting up headnode..."

# Update system
echo ""
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install headnode packages
echo ""
echo "📦 Installing headnode packages..."
sudo apt install -y \
    python3.12 python3.12-venv python3-pip \
    git curl wget htop \
    build-essential \
    net-tools \
    nginx \
    postgresql postgresql-contrib \
    redis-server

# Configure PostgreSQL
echo ""
echo "🗄️  Configuring PostgreSQL..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database
sudo -u postgres psql << PSQL
CREATE DATABASE queztl_core;
CREATE USER queztl WITH PASSWORD 'queztl_secure_password';
GRANT ALL PRIVILEGES ON DATABASE queztl_core TO queztl;
PSQL

echo "  ✓ PostgreSQL configured"

# Configure Redis
echo ""
echo "📦 Configuring Redis..."
sudo systemctl start redis-server
sudo systemctl enable redis-server
echo "  ✓ Redis configured"

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
echo "📥 Setting up queztl-core repository..."
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

# Install full dependencies (headnode needs everything)
echo ""
echo "📦 Installing Python packages (this may take 5-10 minutes)..."
pip install --upgrade pip --quiet
pip install -r backend/requirements.txt --quiet 2>/dev/null || {
    # Fallback: install core packages if requirements.txt fails
    pip install \
        fastapi uvicorn websockets \
        sqlalchemy psycopg2-binary redis \
        torch torchvision pillow numpy pandas \
        flask \
        --quiet
}

echo "  ✓ Python packages installed"

# Generate configuration
echo ""
echo "⚙️  Generating headnode configuration..."

mkdir -p ~/queztl-core/config

cat > ~/queztl-core/config/headnode.yaml << CONFIG
# Queztl Headnode Configuration
headnode:
  name: "$(hostname)"
  role: "master"
  ip: "$(hostname -I | awk '{print $1}')"
  
network:
  api_port: 8000
  dashboard_port: 3000
  websocket_port: 9999
  
database:
  host: "localhost"
  port: 5432
  name: "queztl_core"
  user: "queztl"
  password: "queztl_secure_password"
  
redis:
  host: "localhost"
  port: 6379
  
workers:
  # Worker nodes will register here
  nodes: []
CONFIG

echo "  ✓ Configuration created: ~/queztl-core/config/headnode.yaml"

# Setup systemd service for API
echo ""
echo "🔧 Setting up systemd service..."

sudo tee /etc/systemd/system/queztl-headnode.service > /dev/null << SERVICE
[Unit]
Description=Queztl Headnode API
After=network.target postgresql.service redis-server.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/queztl-core
Environment="PATH=$HOME/queztl-core/venv/bin"
ExecStart=$HOME/queztl-core/venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl daemon-reload
echo "  ✓ Systemd service created"

# Setup Nginx reverse proxy
echo ""
echo "🌐 Configuring Nginx..."

sudo tee /etc/nginx/sites-available/queztl > /dev/null << NGINX
server {
    listen 80;
    server_name $(hostname -I | awk '{print $1}');
    
    # API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
    
    # Dashboard
    location / {
        proxy_pass http://localhost:3000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
    
    # WebSocket
    location /ws {
        proxy_pass http://localhost:9999;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host \$host;
    }
}
NGINX

sudo ln -sf /etc/nginx/sites-available/queztl /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx
echo "  ✓ Nginx configured"

# Setup SSH key for worker management
echo ""
echo "🔐 Setting up SSH keys for worker management..."

if [ ! -f ~/.ssh/id_rsa ]; then
    ssh-keygen -t rsa -b 4096 -C "queztl-headnode@$(hostname)" -f ~/.ssh/id_rsa -N ""
    echo "  ✓ SSH key generated"
else
    echo "  ✓ SSH key already exists"
fi

echo ""
echo "📝 Public key for worker nodes:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat ~/.ssh/id_rsa.pub
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Copy this key to all worker nodes:"
echo "  ssh-copy-id user@worker-ip"
echo ""

# Create management scripts
echo ""
echo "📋 Creating management scripts..."

cat > ~/queztl-core/scripts/headnode-status.sh << 'STATUS'
#!/bin/bash
# Check headnode status

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🎮 QUEZTL HEADNODE STATUS                                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

echo "🖥️  System:"
echo "   Hostname:  $(hostname)"
echo "   IP:        $(hostname -I | awk '{print $1}')"
echo "   Uptime:    $(uptime -p)"
echo "   Load:      $(uptime | awk -F'load average:' '{print $2}')"
echo ""

echo "💾 Resources:"
echo "   CPU:       $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')% used"
echo "   RAM:       $(free -h | grep Mem | awk '{print $3 "/" $2}')"
echo "   Disk:      $(df -h / | tail -1 | awk '{print $3 "/" $2 " (" $5 " used)"}')"
echo ""

echo "🔧 Services:"
systemctl is-active --quiet postgresql && echo "   ✓ PostgreSQL running" || echo "   ✗ PostgreSQL stopped"
systemctl is-active --quiet redis-server && echo "   ✓ Redis running" || echo "   ✗ Redis stopped"
systemctl is-active --quiet nginx && echo "   ✓ Nginx running" || echo "   ✗ Nginx stopped"
systemctl is-active --quiet queztl-headnode && echo "   ✓ API running" || echo "   ✗ API stopped"
echo ""

echo "🌐 Endpoints:"
echo "   API:       http://$(hostname -I | awk '{print $1}'):8000"
echo "   Dashboard: http://$(hostname -I | awk '{print $1}'):3000"
echo "   WebSocket: ws://$(hostname -I | awk '{print $1}'):9999"
echo ""

echo "🤖 Worker Nodes:"
if [ -f ~/queztl-core/config/workers.txt ]; then
    while IFS= read -r worker; do
        ssh -o ConnectTimeout=2 -o StrictHostKeyChecking=no "$worker" "echo '   ✓ $worker - $(uptime -p)'" 2>/dev/null || echo "   ✗ $worker - offline"
    done < ~/queztl-core/config/workers.txt
else
    echo "   (no workers registered)"
fi
STATUS

chmod +x ~/queztl-core/scripts/headnode-status.sh

cat > ~/queztl-core/scripts/add-worker.sh << 'ADDWORKER'
#!/bin/bash
# Add a worker node to the cluster

read -p "Worker hostname or IP: " WORKER
read -p "Worker username: " USER

echo ""
echo "Adding worker: $USER@$WORKER"

# Copy SSH key
ssh-copy-id "$USER@$WORKER" || {
    echo "Failed to copy SSH key"
    exit 1
}

# Test connection
ssh "$USER@$WORKER" "echo 'Connection test successful'" || {
    echo "Failed to connect to worker"
    exit 1
}

# Add to workers list
mkdir -p ~/queztl-core/config
echo "$USER@$WORKER" >> ~/queztl-core/config/workers.txt

# Update config
echo "  - name: \"$WORKER\"" >> ~/queztl-core/config/headnode.yaml
echo "    ip: \"$WORKER\"" >> ~/queztl-core/config/headnode.yaml
echo "    user: \"$USER\"" >> ~/queztl-core/config/headnode.yaml

echo ""
echo "✓ Worker added: $WORKER"
ADDWORKER

chmod +x ~/queztl-core/scripts/add-worker.sh

cat > ~/queztl-core/scripts/deploy-to-workers.sh << 'DEPLOY'
#!/bin/bash
# Deploy code to all workers

if [ ! -f ~/queztl-core/config/workers.txt ]; then
    echo "No workers registered"
    exit 1
fi

echo "🚀 Deploying to all workers..."
echo ""

while IFS= read -r worker; do
    echo "📦 Deploying to $worker..."
    ssh "$worker" "cd queztl-core && git pull && source venv/bin/activate && pip install -q -r backend/requirements.txt" &
done < ~/queztl-core/config/workers.txt

wait
echo ""
echo "✅ Deployment complete!"
DEPLOY

chmod +x ~/queztl-core/scripts/deploy-to-workers.sh

echo "  ✓ Management scripts created"

# Get system info
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Headnode Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Headnode Information:"
echo "   Hostname:  $(hostname)"
echo "   IP:        $(hostname -I | awk '{print $1}')"
echo "   OS:        $(lsb_release -d | cut -f2)"
echo "   RAM:       $(free -h | grep Mem | awk '{print $7}') available"
echo ""
echo "🌐 Access Points:"
echo "   API:       http://$(hostname -I | awk '{print $1}'):8000"
echo "   Dashboard: http://$(hostname -I | awk '{print $1}'):3000"
echo "   WebSocket: ws://$(hostname -I | awk '{print $1}'):9999"
echo ""
echo "🔐 SSH Public Key (copy to workers):"
echo "   ~/.ssh/id_rsa.pub"
echo ""
echo "🎮 Management Commands:"
echo "   Start API:     sudo systemctl start queztl-headnode"
echo "   Check status:  bash ~/queztl-core/scripts/headnode-status.sh"
echo "   Add worker:    bash ~/queztl-core/scripts/add-worker.sh"
echo "   Deploy code:   bash ~/queztl-core/scripts/deploy-to-workers.sh"
echo ""
echo "📋 Next Steps:"
echo "   1. Start services:   sudo systemctl start queztl-headnode"
echo "   2. Add workers:      bash ~/queztl-core/scripts/add-worker.sh"
echo "   3. Check dashboard:  http://$(hostname -I | awk '{print $1}')"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
