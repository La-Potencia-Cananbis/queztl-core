#!/bin/bash
# Deploy distributed failover system to Beast and Sloth

set -e

echo "╔═══════════════════════════════════════════════════════╗"
echo "║  🔄 DEPLOYING DISTRIBUTED FAILOVER SYSTEM            ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Configuration
BEAST_IP="192.168.1.105"
SLOTH_IP="192.168.1.102"
BEAST_USER="xava"
SLOTH_USER="xava"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to deploy to a node
deploy_to_node() {
    local NODE_NAME=$1
    local NODE_IP=$2
    local NODE_USER=$3
    
    echo -e "${BLUE}📦 Deploying to $NODE_NAME ($NODE_IP)${NC}"
    echo "─────────────────────────────────────────────────────────"
    
    # Check if node is reachable
    if ! ping -c 1 -W 2 $NODE_IP > /dev/null 2>&1; then
        echo -e "${RED}❌ $NODE_NAME is not reachable${NC}"
        return 1
    fi
    
    echo "✓ $NODE_NAME is reachable"
    
    # Check if SSH is available
    if ! ssh -o ConnectTimeout=5 $NODE_USER@$NODE_IP "echo 'SSH OK'" > /dev/null 2>&1; then
        echo -e "${RED}❌ Cannot SSH to $NODE_NAME${NC}"
        echo "   Make sure SSH key is set up: ssh-copy-id $NODE_USER@$NODE_IP"
        return 1
    fi
    
    echo "✓ SSH connection established"
    
    # Update repository
    echo "📥 Updating repository..."
    ssh $NODE_USER@$NODE_IP "cd ~/queztl-core && git pull origin main" || {
        echo -e "${YELLOW}⚠️  Could not pull, trying to clone...${NC}"
        ssh $NODE_USER@$NODE_IP "cd ~ && rm -rf queztl-core && git clone https://github.com/La-Potencia-Cananbis/queztl-core.git"
    }
    
    echo "✓ Repository updated"
    
    # Install dependencies
    echo "📦 Installing Python dependencies..."
    ssh $NODE_USER@$NODE_IP "cd ~/queztl-core && pip3 install -q fastapi uvicorn aiohttp python-multipart 2>&1 | grep -v 'already satisfied' || true"
    
    echo "✓ Dependencies installed"
    
    # Create systemd service
    echo "🔧 Creating systemd service..."
    
    ssh $NODE_USER@$NODE_IP "sudo tee /etc/systemd/system/queztl-coordinator.service > /dev/null" <<EOF
[Unit]
Description=Queztl Distributed Coordinator
After=network.target

[Service]
Type=simple
User=$NODE_USER
WorkingDirectory=/home/$NODE_USER/queztl-core
ExecStart=/usr/bin/python3 backend/distributed_roles.py --coordinator $NODE_NAME
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    echo "✓ Systemd service created"
    
    # Reload systemd
    echo "🔄 Reloading systemd..."
    ssh $NODE_USER@$NODE_IP "sudo systemctl daemon-reload"
    
    echo "✓ Systemd reloaded"
    
    # Enable service
    echo "✅ Enabling service..."
    ssh $NODE_USER@$NODE_IP "sudo systemctl enable queztl-coordinator"
    
    # Start/restart service
    echo "🚀 Starting service..."
    ssh $NODE_USER@$NODE_IP "sudo systemctl restart queztl-coordinator"
    
    # Wait a moment for startup
    sleep 3
    
    # Check status
    echo "🔍 Checking service status..."
    if ssh $NODE_USER@$NODE_IP "sudo systemctl is-active queztl-coordinator" | grep -q "active"; then
        echo -e "${GREEN}✅ Service is running on $NODE_NAME${NC}"
    else
        echo -e "${YELLOW}⚠️  Service may not be running, checking logs...${NC}"
        ssh $NODE_USER@$NODE_IP "sudo journalctl -u queztl-coordinator -n 20 --no-pager"
    fi
    
    echo ""
}

# Main deployment
echo "🎯 Starting deployment process..."
echo ""

# Deploy to Beast
if deploy_to_node "beast" "$BEAST_IP" "$BEAST_USER"; then
    echo -e "${GREEN}✅ Beast deployment complete${NC}"
else
    echo -e "${RED}❌ Beast deployment failed${NC}"
fi

echo ""

# Deploy to Sloth
if deploy_to_node "sloth" "$SLOTH_IP" "$SLOTH_USER"; then
    echo -e "${GREEN}✅ Sloth deployment complete${NC}"
else
    echo -e "${RED}❌ Sloth deployment failed${NC}"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║  ✅ DEPLOYMENT COMPLETE                              ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Wait for services to fully start
echo "⏳ Waiting for services to start (10 seconds)..."
sleep 10
echo ""

# Check cluster status
echo "🔍 Checking cluster status..."
echo ""

python3 backend/distributed_roles.py --status || {
    echo ""
    echo -e "${YELLOW}⚠️  Could not check cluster status automatically${NC}"
    echo "   Check manually with: python3 backend/distributed_roles.py --status"
}

echo ""
echo "📝 Service Management Commands:"
echo "─────────────────────────────────────────────────────────"
echo "  # Check status"
echo "  ssh $BEAST_USER@$BEAST_IP 'sudo systemctl status queztl-coordinator'"
echo "  ssh $SLOTH_USER@$SLOTH_IP 'sudo systemctl status queztl-coordinator'"
echo ""
echo "  # View logs"
echo "  ssh $BEAST_USER@$BEAST_IP 'sudo journalctl -u queztl-coordinator -f'"
echo "  ssh $SLOTH_USER@$SLOTH_IP 'sudo journalctl -u queztl-coordinator -f'"
echo ""
echo "  # Restart services"
echo "  ssh $BEAST_USER@$BEAST_IP 'sudo systemctl restart queztl-coordinator'"
echo "  ssh $SLOTH_USER@$SLOTH_IP 'sudo systemctl restart queztl-coordinator'"
echo ""
echo "  # Stop services"
echo "  ssh $BEAST_USER@$BEAST_IP 'sudo systemctl stop queztl-coordinator'"
echo "  ssh $SLOTH_USER@$SLOTH_IP 'sudo systemctl stop queztl-coordinator'"
echo ""
echo "🌐 API Endpoints:"
echo "─────────────────────────────────────────────────────────"
echo "  Beast Coordinator: http://$BEAST_IP:8005/status"
echo "  Sloth Coordinator: http://$SLOTH_IP:8005/status"
echo ""
echo "  # Test with:"
echo "  curl http://$BEAST_IP:8005/status | jq"
echo "  curl http://$SLOTH_IP:8005/status | jq"
echo ""
echo "🎉 Your cluster now runs independently!"
echo "   Unplug your Mac anytime - Beast and Sloth will handle everything."
echo ""
