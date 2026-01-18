#!/bin/bash
# Quick setup script to run on Beast via SSH

cat << 'BANNER'
╔══════════════════════════════════════════════════════════════╗
║  ⚡ BEAST NODE SETUP - Ubuntu Server Headless               ║
╚══════════════════════════════════════════════════════════════╝
BANNER

echo ""
echo "🔗 Downloading node-setup.sh from GitHub..."
wget -q https://raw.githubusercontent.com/La-Potencia-Cananbis/queztl-core/main/scripts/node-setup.sh -O /tmp/node-setup.sh

echo "✓ Downloaded"
echo ""
echo "🚀 Starting setup (this will take ~5-10 minutes)..."
echo ""

chmod +x /tmp/node-setup.sh
sudo bash /tmp/node-setup.sh

echo ""
echo "✅ Beast is ready!"
echo ""
echo "📋 Next steps:"
echo "   • Test: cd ~/queztl-core && source venv/bin/activate && python backend/queztl_agents.py --demo"
echo "   • Install Sloth and repeat"
echo ""
