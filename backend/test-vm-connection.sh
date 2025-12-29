#!/bin/bash

# GIS Studio - VM Connection Diagnostic Script
# Tests all aspects of VM connectivity

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  GIS Studio - VM Connection Diagnostics   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""

# Get IP from argument or use default
VM_IP="${1:-192.168.1.100}"
VM_USER="${2:-ubuntu}"

echo -e "${YELLOW}🔍 Testing connection to: $VM_USER@$VM_IP${NC}"
echo ""

# Test 1: Ping
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Test 1: Network Ping${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if ping -c 1 -W 2 $VM_IP &> /dev/null; then
    echo -e "${GREEN}✅ PASS${NC}: Network reachable ($VM_IP responds to ping)"
else
    echo -e "${RED}❌ FAIL${NC}: Network unreachable ($VM_IP does not respond to ping)"
    echo ""
    echo -e "${YELLOW}⚠️  DIAGNOSIS:${NC}"
    echo "  • VM may be powered off"
    echo "  • VM is not connected to network"
    echo "  • IP address 192.168.1.100 is incorrect"
    echo "  • Firewall is blocking ICMP"
    echo ""
    echo -e "${YELLOW}💡 SOLUTION:${NC}"
    echo "  1. Verify VM is powered on"
    echo "  2. Check correct IP: On Ubuntu VM, run 'hostname -I'"
    echo "  3. Check router DHCP table for actual VM IP"
    echo "  4. Update command: ./test-vm-connection.sh <correct-ip>"
    echo ""
    exit 1
fi
echo ""

# Test 2: SSH Port
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Test 2: SSH Port (22)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if nc -zv -w 2 $VM_IP 22 &> /dev/null; then
    echo -e "${GREEN}✅ PASS${NC}: SSH port 22 is open and listening"
else
    echo -e "${RED}❌ FAIL${NC}: SSH port 22 is not responding"
    echo ""
    echo -e "${YELLOW}⚠️  DIAGNOSIS:${NC}"
    echo "  • SSH service is not running on VM"
    echo "  • Port 22 is blocked by firewall"
    echo "  • Kernel is not accepting connections"
    echo ""
    echo -e "${YELLOW}💡 SOLUTION (on Ubuntu VM):${NC}"
    echo "  1. Check if SSH is running:"
    echo "     sudo systemctl status ssh"
    echo "  2. Start SSH if stopped:"
    echo "     sudo systemctl start ssh"
    echo "  3. Enable SSH to start on boot:"
    echo "     sudo systemctl enable ssh"
    echo "  4. Allow SSH in firewall:"
    echo "     sudo ufw allow 22/tcp"
    echo ""
    exit 1
fi
echo ""

# Test 3: SSH Connection (no auth)
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Test 3: SSH Connection${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if timeout 5 ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no \
    $VM_USER@$VM_IP 'echo "Connection test"' &> /dev/null; then
    echo -e "${GREEN}✅ PASS${NC}: SSH connection successful"
    echo "  User: $VM_USER"
    echo "  Host: $VM_IP"
else
    echo -e "${YELLOW}⚠️  WARN${NC}: SSH connection test inconclusive"
    echo "  (This might be due to key authentication or host verification)"
    echo ""
    echo -e "${YELLOW}💡 NEXT STEPS:${NC}"
    echo "  1. Try SSH with verbose output:"
    echo "     ssh -v $VM_USER@$VM_IP"
    echo ""
    echo "  2. If asked about host key, answer 'yes' to accept"
    echo ""
    echo "  3. If password prompt appears, enter your password"
    echo ""
    echo "  4. Try with explicit key if you have one:"
    echo "     ssh -i ~/.ssh/your-key.pem $VM_USER@$VM_IP"
fi
echo ""

# Test 4: System Resources Check
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Test 4: System Resources (if accessible)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if timeout 5 ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no \
    $VM_USER@$VM_IP 'true' &> /dev/null; then
    
    echo -e "${GREEN}✅ Can access VM - checking resources...${NC}"
    echo ""
    
    # Disk space
    DISK=$(ssh $VM_USER@$VM_IP 'df -h / | tail -1 | awk "{print \$4}"' 2>/dev/null || echo "N/A")
    if [[ "$DISK" != "N/A" ]]; then
        echo "  💾 Free disk space: $DISK"
    fi
    
    # RAM
    RAM=$(ssh $VM_USER@$VM_IP 'free -h | grep Mem | awk "{print \$7}"' 2>/dev/null || echo "N/A")
    if [[ "$RAM" != "N/A" ]]; then
        echo "  💾 Free RAM: $RAM"
    fi
    
    # OS Info
    OS=$(ssh $VM_USER@$VM_IP 'lsb_release -ds' 2>/dev/null || echo "N/A")
    if [[ "$OS" != "N/A" ]]; then
        echo "  🐧 OS: $OS"
    fi
else
    echo -e "${YELLOW}⚠️  SKIP${NC}: Could not authenticate to VM"
    echo "  (This is OK - you may still be able to deploy)"
fi
echo ""

# Summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Summary${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}✅ Your VM at $VM_IP is accessible!${NC}"
echo ""
echo -e "${YELLOW}🚀 You can now run deployment:${NC}"
echo "   ./deploy-to-ubuntu-vm.sh $VM_IP"
echo ""
echo -e "${YELLOW}Or with custom username:${NC}"
echo "   ./deploy-to-ubuntu-vm.sh $VM_IP your_username"
echo ""
