#!/bin/bash
# Install QZPM on remote machines (Beast, Sloth, cluster nodes)

set -e

REMOTE_HOST="$1"
REMOTE_USER="${2:-xava}"

if [ -z "$REMOTE_HOST" ]; then
    echo "Usage: $0 <host> [user]"
    echo ""
    echo "Examples:"
    echo "  $0 192.168.1.105        # Install on Beast"
    echo "  $0 192.168.1.106 xava   # Install on Sloth"
    exit 1
fi

echo "🚩 Installing QZPM on ${REMOTE_HOST}"
echo "=" * 50
echo ""

# Check connectivity
if ! ping -c 1 ${REMOTE_HOST} &> /dev/null; then
    echo "❌ ${REMOTE_HOST} is not reachable"
    exit 1
fi

echo "✓ ${REMOTE_HOST} is online"
echo ""

# Copy QZPM
echo "📤 Transferring QZPM..."
scp qzpm ${REMOTE_USER}@${REMOTE_HOST}:/tmp/qzpm
echo "✓ QZPM transferred"
echo ""

# Install on remote
echo "📦 Installing on remote..."
ssh ${REMOTE_USER}@${REMOTE_HOST} << 'ENDSSH'
mkdir -p ~/bin
mv /tmp/qzpm ~/bin/qzpm
chmod +x ~/bin/qzpm

# Add to PATH if not already there
if ! grep -q 'export PATH="$HOME/bin:$PATH"' ~/.bashrc; then
    echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
fi

~/bin/qzpm update
echo ""
echo "✓ QZPM installed at ~/bin/qzpm"
echo ""
echo "Usage on remote:"
echo "  qzpm list"
echo "  qzpm install <package>"
ENDSSH

echo ""
echo "✓ Installation complete!"
echo ""
echo "Test it:"
echo "  ssh ${REMOTE_USER}@${REMOTE_HOST} 'qzpm list'"
echo ""
