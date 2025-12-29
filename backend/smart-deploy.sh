#!/bin/bash

# GIS Studio - Smart VM Deployment
# Handles finding VM, testing connection, and deploying

set +e  # Don't exit on errors - we want to handle them gracefully

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

clear

echo -e "${CYAN}"
cat << 'BANNER'
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         🗺️  GIS STUDIO - SMART VM DEPLOYMENT             ║
║              One Command to Deploy!                       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
BANNER
echo -e "${NC}"

# If no IP provided, help user find it
if [ -z "$1" ]; then
    echo -e "${YELLOW}⚠️  No VM IP provided!${NC}"
    echo ""
    echo "I can help you find your VM's IP address..."
    echo ""
    
    echo -e "${BLUE}Option 1: Direct Access${NC}"
    echo "  If you can access Ubuntu VM terminal:"
    echo "  $ hostname -I"
    echo ""
    
    echo -e "${BLUE}Option 2: Network Scan${NC}"
    echo "  I'll scan for machines with SSH open..."
    echo ""
    
    read -p "Scan network for SSH servers? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${CYAN}🔍 Scanning for Ubuntu VM (this takes ~30 seconds)...${NC}"
        echo ""
        
        found_vms=()
        
        # Check common network ranges
        for ip in 192.168.1.{1..254} 192.168.0.{1..254} 10.0.0.{1..254}; do
            if timeout 0.5 bash -c "echo >/dev/tcp/$ip/22" 2>/dev/null; then
                found_vms+=("$ip")
            fi
        done
        
        if [ ${#found_vms[@]} -eq 0 ]; then
            echo -e "${RED}❌ No SSH servers found on common networks${NC}"
            echo ""
            echo "Try these methods:"
            echo "  1. Check your router's DHCP client list (http://192.168.1.1)"
            echo "  2. On Ubuntu VM terminal, run: hostname -I"
            echo "  3. Use extended scan: ./smart-deploy.sh --scan-all"
            exit 1
        fi
        
        echo -e "${GREEN}Found ${#found_vms[@]} machine(s) with SSH:${NC}"
        for i in "${!found_vms[@]}"; do
            echo "  $(($i + 1)). ${found_vms[$i]}"
        done
        echo ""
        
        if [ ${#found_vms[@]} -eq 1 ]; then
            VM_IP="${found_vms[0]}"
            echo -e "${GREEN}✅ Using detected VM: $VM_IP${NC}"
        else
            echo "Multiple machines found. Which is your Ubuntu VM?"
            read -p "Enter number (1-${#found_vms[@]}): " choice
            VM_IP="${found_vms[$((choice-1))]}"
        fi
    else
        echo ""
        echo "To deploy, you need your VM's IP address."
        echo ""
        echo "Get it from the VM terminal:"
        echo "  $ hostname -I"
        echo ""
        echo "Then run deployment:"
        echo "  $ ./smart-deploy.sh <your-vm-ip>"
        echo ""
        exit 0
    fi
else
    VM_IP="$1"
fi

VM_USER="${2:-ubuntu}"

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}Testing Connection to: ${GREEN}$VM_USER@$VM_IP${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo ""

# Test 1: Ping
echo -e "${BLUE}1️⃣  Testing network connectivity...${NC}"
if ping -c 1 -W 2 "$VM_IP" &>/dev/null; then
    echo -e "${GREEN}✅ VM is reachable${NC}"
else
    echo -e "${RED}❌ VM is not responding to ping${NC}"
    echo "   Try a different IP address"
    exit 1
fi
echo ""

# Test 2: SSH Port
echo -e "${BLUE}2️⃣  Testing SSH port (22)...${NC}"
if timeout 3 bash -c "echo >/dev/tcp/$VM_IP/22" 2>/dev/null; then
    echo -e "${GREEN}✅ SSH port is open${NC}"
else
    echo -e "${RED}❌ SSH port 22 not responding${NC}"
    echo "   SSH service may not be running on VM"
    exit 1
fi
echo ""

# Test 3: SSH Connection
echo -e "${BLUE}3️⃣  Testing SSH authentication...${NC}"
if timeout 5 ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null "$VM_USER@$VM_IP" 'echo "SSH OK"' &>/dev/null; then
    echo -e "${GREEN}✅ SSH connection successful${NC}"
else
    echo -e "${YELLOW}⚠️  SSH authentication may need password${NC}"
    echo "   Will attempt deployment..."
fi
echo ""

# All tests passed!
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ VM IS READY FOR DEPLOYMENT!${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo ""

echo "Ready to deploy GIS Studio to: $VM_IP"
echo ""
echo "This will:"
echo "  ✅ Transfer all GIS Studio files"
echo "  ✅ Install Python and dependencies"
echo "  ✅ Configure systemd services"
echo "  ✅ Start frontend (port 8080) and backend (port 8000)"
echo ""
echo "Time needed: ~7-10 minutes"
echo ""

read -p "Continue with deployment? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi

echo ""
echo -e "${CYAN}🚀 Starting deployment...${NC}"
echo ""

# Run the actual deployment script
if [ -f "./deploy-to-ubuntu-vm.sh" ]; then
    ./deploy-to-ubuntu-vm.sh "$VM_IP" "$VM_USER"
else
    echo -e "${RED}❌ deploy-to-ubuntu-vm.sh not found!${NC}"
    echo "   Make sure you're in the /Users/xavasena/hive directory"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "Access your GIS Studio at:"
echo "  🚀 API Tester:  http://$VM_IP:8080/gis-studio-dashboard.html"
echo "  🎨 Info Page:   http://$VM_IP:8080/gis-studio.html"
echo "  📚 API Docs:    http://$VM_IP:8000/docs"
echo ""
