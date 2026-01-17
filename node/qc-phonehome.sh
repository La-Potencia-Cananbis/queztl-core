#!/bin/bash
# QC Node Phone-Home Enrollment Script
# Runs on first boot to enroll node with headnode

set -e

ENROLL_URL="${QC_ENROLL_URL:-https://enroll.qc.lan/enroll}"
CERT_DIR="/etc/qc/pki"
STATE="/var/lib/qc"
WORK_DIR="/opt/queztl-core"

mkdir -p "$CERT_DIR" "$STATE"

echo "🔐 QC Node Enrollment Starting..."
echo "   Enrollment API: $ENROLL_URL"

# Collect MAC addresses
echo "📡 Collecting hardware identity..."
MACS=$(ip link | awk '/link\/ether/ {print $2}' | sort -u)
MAC_JSON=$(printf '%s\n' $MACS | jq -R . | jq -s .)

# Get IP address
IP=$(ip route get 1.1.1.1 2>/dev/null | awk '/src/ {print $7}' || echo "")

echo "   MACs: $(echo "$MACS" | tr '\n' ',' | sed 's/,$//')"
echo "   IP: ${IP:-unknown}"

# Phone home to enrollment API
echo "📞 Contacting enrollment API..."
RESP=$(curl -s -X POST "$ENROLL_URL" \
  -H "Content-Type: application/json" \
  -d "{\"macs\":$MAC_JSON,\"ip\":\"$IP\"}" || {
    echo "❌ Failed to contact enrollment API"
    exit 1
  })

# Parse response
HOSTNAME=$(echo "$RESP" | jq -r .hostname)
NODE_ID=$(echo "$RESP" | jq -r .node_id)
ROLE=$(echo "$RESP" | jq -r .role)
TOKEN=$(echo "$RESP" | jq -r .step_token)
STEP_CA=$(echo "$RESP" | jq -r .step_ca_url)
PROV=$(echo "$RESP" | jq -r .step_provisioner)
GIT_REPO=$(echo "$RESP" | jq -r .git_repo)
GIT_REF=$(echo "$RESP" | jq -r .git_ref)
BOOTSTRAP=$(echo "$RESP" | jq -r .bootstrap_cmd)

echo "✓ Enrolled as:"
echo "   Node ID: $NODE_ID"
echo "   Role: $ROLE"
echo "   Hostname: $HOSTNAME"

# Bootstrap step-ca client
echo "🔐 Bootstrapping step-ca client..."
step ca bootstrap --ca-url "$STEP_CA" --install --force || {
  echo "❌ Failed to bootstrap step-ca"
  exit 1
}
echo "✓ CA trust established"

# Request mTLS certificate
echo "📜 Requesting node certificate..."
step ca certificate "$HOSTNAME" "$CERT_DIR/node.crt" "$CERT_DIR/node.key" \
  --token "$TOKEN" \
  --provisioner "$PROV" \
  --force || {
    echo "❌ Failed to obtain certificate"
    exit 1
  }
echo "✓ Certificate obtained: $CERT_DIR/node.crt"

# Set hostname
echo "🏷️  Setting hostname..."
hostnamectl set-hostname "$HOSTNAME"
echo "✓ Hostname: $HOSTNAME"

# Clone or update Git repository
if [ ! -d "$WORK_DIR" ]; then
  echo "📥 Cloning queztl-core repository..."
  git clone "$GIT_REPO" "$WORK_DIR" || {
    echo "❌ Failed to clone repository"
    exit 1
  }
else
  echo "📥 Updating queztl-core repository..."
  cd "$WORK_DIR"
  git fetch origin
fi

cd "$WORK_DIR"
git checkout "$GIT_REF"
git pull origin "$GIT_REF" || true

echo "✓ Repository ready: $WORK_DIR"

# Export certificate paths for bootstrap
export QC_CERT_CRT="$CERT_DIR/node.crt"
export QC_CERT_KEY="$CERT_DIR/node.key"
export QC_NODE_ID="$NODE_ID"
export QC_ROLE="$ROLE"

# Run bootstrap
echo "🚀 Running Queztl bootstrap..."
bash -lc "$BOOTSTRAP" || {
  echo "⚠️  Bootstrap command failed, but enrollment complete"
}

# Mark enrollment complete
touch "$STATE/firstboot.done"
echo ""
echo "✅ Enrollment complete!"
echo "   Certificate: $CERT_DIR/node.crt"
echo "   Key: $CERT_DIR/node.key"
echo "   Workspace: $WORK_DIR"
echo ""
