#!/bin/bash
# 🌩️ CLOUD WORKER VM SETUP
# Creates remote Linux workers for compilation tasks
# No more local Mac compiling after initial VM!

set -e

echo "==============================================="
echo "🌩️ QUETZALCORE CLOUD WORKER SETUP"
echo "==============================================="
echo ""

# Cloud provider options
cat << 'PROVIDERS'
📋 Choose Your Cloud Provider:

1. DigitalOcean Droplet (Recommended for startups)
   - ARM64 droplet: $6/month ($0.009/hour)
   - Easy API, great docs
   - 1GB RAM, 1 vCPU, 25GB SSD
   - Setup: doctl compute droplet create

2. AWS EC2 (Enterprise-grade)
   - t4g.micro: $0.0084/hour (~$6/month)
   - ARM64 Graviton2
   - 1GB RAM, 2 vCPU
   - Setup: aws ec2 run-instances

3. Hetzner Cloud (Budget-friendly)
   - CAX11: €4.51/month (~$5/month)
   - ARM64, 2 vCPU, 4GB RAM
   - Best price/performance
   - Setup: hcloud server create

4. Railway.app (Hobby-friendly)
   - Pay-as-you-go: ~$0.02/hour
   - No idle charges when stopped
   - Easy web interface
   - Setup: railway up

5. Fly.io (Developer-focused)
   - Free tier: 3 shared-cpu VMs
   - ARM64 support
   - Global edge deployment
   - Setup: flyctl launch

PROVIDERS

echo ""
read -p "Enter choice (1-5, or 'skip'): " choice

case $choice in
    1)
        echo ""
        echo "🌊 Setting up DigitalOcean Worker..."
        echo ""
        
        # Check for doctl
        if ! command -v doctl &> /dev/null; then
            echo "Installing doctl..."
            brew install doctl
        fi
        
        # Check authentication
        if ! doctl account get &> /dev/null; then
            echo "⚠️  doctl not authenticated"
            echo ""
            echo "Steps:"
            echo "1. Get API token: https://cloud.digitalocean.com/account/api/tokens"
            echo "2. Run: doctl auth init"
            echo "3. Re-run this script"
            exit 1
        fi
        
        echo "Creating QuetzalCore worker droplet..."
        doctl compute droplet create quetzalcore-worker-1 \
            --image ubuntu-22-04-x64 \
            --size s-1vcpu-1gb \
            --region sfo3 \
            --ssh-keys $(doctl compute ssh-key list --format ID --no-header) \
            --wait
        
        WORKER_IP=$(doctl compute droplet get quetzalcore-worker-1 --format PublicIPv4 --no-header)
        
        echo "✅ Worker created at $WORKER_IP"
        ;;
        
    2)
        echo ""
        echo "☁️  Setting up AWS EC2 Worker..."
        echo ""
        
        if ! command -v aws &> /dev/null; then
            echo "Installing AWS CLI..."
            brew install awscli
        fi
        
        # Check authentication
        if ! aws sts get-caller-identity &> /dev/null; then
            echo "⚠️  AWS CLI not configured"
            echo ""
            echo "Run: aws configure"
            echo "Then re-run this script"
            exit 1
        fi
        
        echo "Creating EC2 instance..."
        aws ec2 run-instances \
            --image-id ami-0c55b159cbfafe1f0 \
            --instance-type t4g.micro \
            --key-name quetzalcore-worker \
            --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=quetzalcore-worker-1}]'
        
        echo "✅ EC2 instance launching..."
        ;;
        
    3)
        echo ""
        echo "🇩🇪 Setting up Hetzner Worker..."
        echo ""
        
        if ! command -v hcloud &> /dev/null; then
            echo "Installing hcloud CLI..."
            brew install hcloud
        fi
        
        if ! hcloud context list &> /dev/null; then
            echo "⚠️  hcloud not configured"
            echo ""
            echo "Steps:"
            echo "1. Get API token: https://console.hetzner.cloud/"
            echo "2. Run: hcloud context create quetzalcore"
            echo "3. Re-run this script"
            exit 1
        fi
        
        echo "Creating Hetzner server..."
        hcloud server create \
            --name quetzalcore-worker-1 \
            --type cax11 \
            --image ubuntu-22.04 \
            --ssh-key default
        
        WORKER_IP=$(hcloud server ip quetzalcore-worker-1)
        echo "✅ Worker created at $WORKER_IP"
        ;;
        
    4)
        echo ""
        echo "🚂 Railway.app Worker Setup"
        echo ""
        echo "📋 Manual Steps:"
        echo "1. Visit: https://railway.app"
        echo "2. Create new project"
        echo "3. Select 'Empty Service'"
        echo "4. Add environment: Ubuntu 22.04"
        echo "5. Note the SSH connection details"
        echo ""
        read -p "Press Enter when done..."
        ;;
        
    5)
        echo ""
        echo "🪰 Fly.io Worker Setup"
        echo ""
        
        if ! command -v flyctl &> /dev/null; then
            echo "Installing flyctl..."
            brew install flyctl
        fi
        
        if ! flyctl auth whoami &> /dev/null; then
            echo "⚠️  Not logged into Fly.io"
            echo "Run: flyctl auth login"
            exit 1
        fi
        
        echo "Creating Fly machine..."
        flyctl machines create \
            --name quetzalcore-worker-1 \
            --region sjc \
            --image ubuntu:22.04 \
            --memory 1024 \
            --cpus 1
        
        echo "✅ Fly machine created"
        ;;
        
    skip)
        echo "Skipping cloud worker setup"
        exit 0
        ;;
        
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

# Create worker bootstrap script
cat > bootstrap-worker.sh << 'BOOTSTRAP'
#!/bin/bash
# Run this on the cloud worker to set up build environment

# Update system
sudo apt update && sudo apt upgrade -y

# Install build tools
sudo apt install -y \
    build-essential \
    curl \
    git \
    qemu-kvm \
    libvirt-daemon-system

# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env

# Clone repo
git clone https://github.com/SalChicanoLoco/quetzalcore-core.git
cd quetzalcore-core/quetzalcore-hypervisor/core

# Build
cargo build --release

echo "✅ Worker ready!"
echo "Binary: $(pwd)/target/release/quetzalcore-hv"
BOOTSTRAP

chmod +x bootstrap-worker.sh

echo ""
echo "==============================================="
echo "✅ CLOUD WORKER SETUP COMPLETE"
echo "==============================================="
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. SSH into worker:"
if [ ! -z "$WORKER_IP" ]; then
    echo "   ssh root@$WORKER_IP"
else
    echo "   (Use connection details from provider)"
fi
echo ""
echo "2. Copy bootstrap script:"
echo "   scp bootstrap-worker.sh root@WORKER_IP:~/"
echo ""
echo "3. Run on worker:"
echo "   ssh root@WORKER_IP 'bash bootstrap-worker.sh'"
echo ""
echo "4. Future builds:"
echo "   ssh root@WORKER_IP 'cd quetzalcore-core && git pull && cargo build --release'"
echo ""
echo "💰 Remember to stop worker when not in use!"
echo "   (Saves money - most providers charge by the hour)"
echo ""
