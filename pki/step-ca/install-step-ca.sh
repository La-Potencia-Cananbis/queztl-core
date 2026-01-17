#!/usr/bin/env bash
# Install and configure Smallstep step-ca on Debian
# Run on the headnode that will act as internal CA

set -euo pipefail

echo "🔐 Installing Smallstep step-ca on Debian..."

# Install dependencies
if ! command -v curl >/dev/null; then
  apt-get update
  apt-get install -y curl ca-certificates gnupg
fi

# Add Smallstep repository
curl -fsSL https://packages.smallstep.com/keys/smallstep-archive-keyring.gpg \
  | gpg --dearmor -o /usr/share/keyrings/smallstep-archive-keyring.gpg

cat >/etc/apt/sources.list.d/smallstep.list <<EOF
deb [signed-by=/usr/share/keyrings/smallstep-archive-keyring.gpg] https://packages.smallstep.com/debian/ stable main
EOF

# Install step-ca and step-cli
apt-get update
apt-get install -y step-ca step-cli

# Create step user and directories
useradd --system --home /var/lib/step --shell /usr/sbin/nologin step || true
install -d -o step -g step -m 0750 /etc/step-ca /var/lib/step /var/log/step-ca

echo "✓ step-ca installed"
echo ""
echo "📝 Next steps:"
echo "   1. Initialize CA: sudo -u step step ca init"
echo "   2. Configure ca.json in /etc/step-ca/config/"
echo "   3. Install systemd service: scripts/pki/install-step-ca-service.sh"
echo "   4. Move ROOT CA key offline after init"
echo ""
