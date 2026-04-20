#!/bin/bash
# Setup both Beast and Sloth quickly

set -euo pipefail

BEAST_IP="192.168.1.105"
SLOTH_IP="${1:-PENDING}"
REMOTE_DIR="${REMOTE_DIR:-~/queztl-core}"

echo "🔧 Beast & Sloth Quick Setup"
echo "================================"
echo "Beast IP: $BEAST_IP"
echo "Sloth IP: $SLOTH_IP"
echo "Remote dir: $REMOTE_DIR"
echo ""

if [ "$SLOTH_IP" = "PENDING" ]; then
    echo "Usage: $0 <sloth-ip>"
    echo ""
    echo "Once Sloth boots, get its IP and run:"
    echo "  ./quick-setup.sh <sloth-ip>"
    exit 1
fi

echo "📋 Setting up SSH keys..."
echo ""

# Setup SSH key for Sloth
echo "Setting up Sloth SSH key..."
ssh-copy-id "xava@$SLOTH_IP"

echo ""
echo "✅ SSH keys configured!"
echo ""
echo "📥 Installing on Sloth..."
ssh "xava@$SLOTH_IP" "wget -q https://raw.githubusercontent.com/La-Potencia-Cananbis/queztl-core/main/scripts/node-setup.sh && chmod +x node-setup.sh && sudo bash node-setup.sh"

echo ""
echo "✅ Both nodes ready!"
echo ""
echo "🧪 Test commands:"
echo "  ssh xava@$BEAST_IP 'cd $REMOTE_DIR && source venv/bin/activate && python backend/queztl_agents.py --demo'"
echo "  ssh xava@$SLOTH_IP 'cd $REMOTE_DIR && source venv/bin/activate && python backend/queztl_agents.py --demo'"
