#!/bin/bash
# SSH Setup for Beast & Sloth Remote Control
# Run this on your LAPTOP after Beast/Sloth are installed

set -e

echo "🔐 Setting up SSH for Beast & Sloth remote control"
echo ""

# Generate SSH key if needed
if [ ! -f ~/.ssh/id_rsa ]; then
    echo "📝 Generating SSH key..."
    ssh-keygen -t rsa -b 4096 -C "queztl-control@laptop" -f ~/.ssh/id_rsa -N ""
    echo "✓ SSH key generated"
else
    echo "✓ SSH key already exists"
fi

echo ""
echo "Enter Beast's IP address:"
read -p "Beast IP: " BEAST_IP

echo "Enter Sloth's IP address:"
read -p "Sloth IP: " SLOTH_IP

echo "Enter username (default: queztl):"
read -p "Username: " USERNAME
USERNAME=${USERNAME:-queztl}

echo ""
echo "📤 Copying SSH keys to remote machines..."

# Copy to Beast
echo ""
echo "Copying to Beast ($BEAST_IP)..."
ssh-copy-id -i ~/.ssh/id_rsa.pub $USERNAME@$BEAST_IP || {
    echo "⚠️  Manual key copy for Beast:"
    echo "   ssh $USERNAME@$BEAST_IP 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys' < ~/.ssh/id_rsa.pub"
}

# Copy to Sloth
echo ""
echo "Copying to Sloth ($SLOTH_IP)..."
ssh-copy-id -i ~/.ssh/id_rsa.pub $USERNAME@$SLOTH_IP || {
    echo "⚠️  Manual key copy for Sloth:"
    echo "   ssh $USERNAME@$SLOTH_IP 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys' < ~/.ssh/id_rsa.pub"
}

echo ""
echo "📝 Creating SSH config..."

# Backup existing config
if [ -f ~/.ssh/config ]; then
    cp ~/.ssh/config ~/.ssh/config.backup
fi

# Add hosts to SSH config
cat >> ~/.ssh/config << EOF

# Queztl Agent Cluster
Host beast
    HostName $BEAST_IP
    User $USERNAME
    IdentityFile ~/.ssh/id_rsa
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host sloth
    HostName $SLOTH_IP
    User $USERNAME
    IdentityFile ~/.ssh/id_rsa
    ServerAliveInterval 60
    ServerAliveCountMax 3
EOF

echo "✓ SSH config updated"

# Test connections
echo ""
echo "🔍 Testing connections..."

echo ""
echo "Testing Beast..."
ssh -o ConnectTimeout=5 beast "echo '✓ Beast connection successful'" || echo "✗ Beast connection failed"

echo ""
echo "Testing Sloth..."
ssh -o ConnectTimeout=5 sloth "echo '✓ Sloth connection successful'" || echo "✗ Sloth connection failed"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SSH Setup Complete!"
echo ""
echo "You can now connect without passwords:"
echo "   ssh beast"
echo "   ssh sloth"
echo ""
echo "Run commands remotely:"
echo "   ssh beast 'hostname && uptime'"
echo "   ssh sloth 'python3 --version'"
echo ""
echo "Deploy agents:"
echo "   ssh beast 'cd queztl-core && python backend/queztl_agents.py --spawn trainer'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
