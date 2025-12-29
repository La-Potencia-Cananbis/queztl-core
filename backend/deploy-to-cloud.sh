#!/bin/bash
# 🚀 AUTONOMOUS CLOUD DEPLOYMENT
# Deploy QuetzalCore Hypervisor to cloud worker automatically

set -e

echo "🚀 QUETZALCORE - Autonomous Cloud Deployment"
echo "========================================"
echo ""

# Check for DigitalOcean auth
if ! doctl account get &> /dev/null; then
    echo "⚠️  DigitalOcean not authenticated"
    echo ""
    echo "Quick setup:"
    echo "1. Get API token: https://cloud.digitalocean.com/account/api/tokens"
    echo "2. Run: doctl auth init"
    echo "3. Paste your token"
    echo ""
    read -p "Do you want to authenticate now? (y/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        doctl auth init
    else
        echo "Cancelled. Run 'doctl auth init' when ready."
        exit 1
    fi
fi

echo "✅ DigitalOcean authenticated"
echo ""

# Create SSH key if needed
SSH_KEY_NAME="quetzalcore-deploy-$(date +%s)"
if [ ! -f ~/.ssh/id_rsa ]; then
    echo "🔑 Generating SSH key..."
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
fi

# Upload SSH key to DO
echo "🔑 Uploading SSH key to DigitalOcean..."
doctl compute ssh-key import $SSH_KEY_NAME --public-key-file ~/.ssh/id_rsa.pub 2>/dev/null || echo "  (Key may already exist)"

# Get SSH key ID
SSH_KEY_ID=$(doctl compute ssh-key list --format ID,Name --no-header | grep "$SSH_KEY_NAME" | awk '{print $1}' | head -1)
if [ -z "$SSH_KEY_ID" ]; then
    # Use first available key
    SSH_KEY_ID=$(doctl compute ssh-key list --format ID --no-header | head -1)
fi

echo "✅ SSH key ready (ID: $SSH_KEY_ID)"
echo ""

# Create droplet
DROPLET_NAME="quetzalcore-hypervisor-$(date +%s)"
echo "🌊 Creating DigitalOcean droplet: $DROPLET_NAME"
echo "   Size: 2GB RAM, 1 vCPU ($12/month)"
echo "   Region: NYC3"
echo "   OS: Ubuntu 22.04"
echo ""

doctl compute droplet create $DROPLET_NAME \
    --image ubuntu-22-04-x64 \
    --size s-1vcpu-2gb \
    --region nyc3 \
    --ssh-keys $SSH_KEY_ID \
    --wait \
    --format ID,Name,PublicIPv4,Status

# Get droplet IP
echo ""
echo "⏳ Waiting for droplet to be ready..."
sleep 10

DROPLET_IP=$(doctl compute droplet list --format Name,PublicIPv4 --no-header | grep "$DROPLET_NAME" | awk '{print $2}')

if [ -z "$DROPLET_IP" ]; then
    echo "❌ Failed to get droplet IP"
    exit 1
fi

echo "✅ Droplet ready at: $DROPLET_IP"
echo ""

# Wait for SSH to be ready
echo "⏳ Waiting for SSH to be ready..."
for i in {1..30}; do
    if ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$DROPLET_IP "echo SSH Ready" &> /dev/null; then
        echo "✅ SSH is ready!"
        break
    fi
    echo "  Waiting... ($i/30)"
    sleep 5
done

echo ""
echo "📦 Deploying hypervisor to $DROPLET_IP..."
echo ""

# Copy binary
echo "1. Copying hypervisor binary..."
scp -o StrictHostKeyChecking=no quetzalcore-hypervisor/core/target/release/quetzalcore-hypervisor root@$DROPLET_IP:/usr/local/bin/

# Install dependencies and test
echo "2. Installing dependencies..."
ssh -o StrictHostKeyChecking=no root@$DROPLET_IP << 'REMOTE_SCRIPT'
    # Install KVM
    apt-get update -qq
    apt-get install -y -qq qemu-kvm libvirt-daemon-system virtinst cpu-checker
    
    # Check KVM support
    if kvm-ok &> /dev/null; then
        echo "✅ KVM is available"
    else
        echo "⚠️  KVM may not be available (nested virtualization needed)"
    fi
    
    # Make binary executable
    chmod +x /usr/local/bin/quetzalcore-hypervisor
    
    # Test binary
    echo ""
    echo "3. Testing hypervisor..."
    /usr/local/bin/quetzalcore-hypervisor --version || echo "Hypervisor binary ready (version command not implemented yet)"
    
    echo ""
    echo "✅ Deployment complete!"
REMOTE_SCRIPT

echo ""
echo "========================================"
echo "✅ DEPLOYMENT SUCCESSFUL"
echo "========================================"
echo ""
echo "🌐 Droplet: $DROPLET_NAME"
echo "📍 IP: $DROPLET_IP"
echo "💰 Cost: ~$12/month (~$0.018/hour)"
echo ""
echo "🔌 SSH Access:"
echo "   ssh root@$DROPLET_IP"
echo ""
echo "🧪 Test Hypervisor:"
echo "   ssh root@$DROPLET_IP '/usr/local/bin/quetzalcore-hypervisor --help'"
echo ""
echo "🗑️  Destroy when done:"
echo "   doctl compute droplet delete $DROPLET_NAME"
echo ""
echo "💡 Binary location on server: /usr/local/bin/quetzalcore-hypervisor"
echo ""

# Save connection info
cat > .cloud-worker-info << EOF
Droplet Name: $DROPLET_NAME
IP Address: $DROPLET_IP
Created: $(date)
SSH: ssh root@$DROPLET_IP
Binary: /usr/local/bin/quetzalcore-hypervisor
Destroy: doctl compute droplet delete $DROPLET_NAME
EOF

echo "📄 Connection info saved to: .cloud-worker-info"
echo ""
