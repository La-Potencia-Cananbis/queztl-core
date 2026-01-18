#!/bin/bash
# Deploy BeastQC Image Generator with Stable Diffusion XL

set -e

echo "🚩 BEASTQC IMAGE GENERATOR DEPLOYMENT"
echo "=================================================="
echo ""

BEAST_IP="192.168.1.105"
BEAST_USER="xava"
REMOTE_DIR="~/queztl-core"

echo "📡 Connecting to Beast (${BEAST_IP})..."
echo ""

# Check if Beast is online
if ! ping -c 1 ${BEAST_IP} &> /dev/null; then
    echo "❌ Beast is not reachable at ${BEAST_IP}"
    exit 1
fi

echo "✓ Beast is online"
echo ""

# Transfer files
echo "📤 Transferring files to Beast..."
scp backend/beast_image_generator.py ${BEAST_USER}@${BEAST_IP}:${REMOTE_DIR}/backend/
echo "✓ Files transferred"
echo ""

# Install dependencies and start server
echo "🔧 Installing dependencies on Beast..."
echo ""

ssh ${BEAST_USER}@${BEAST_IP} << 'ENDSSH'
cd ~/queztl-core
source venv/bin/activate

echo "Installing Python packages..."
pip install fastapi uvicorn[standard] pillow --break-system-packages

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "OPTIONAL: Install Stable Diffusion XL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "For AI image generation, install these packages:"
echo "  pip install torch torchvision --break-system-packages"
echo "  pip install diffusers transformers accelerate --break-system-packages"
echo ""
echo "⚠️  WARNING: This will download ~7GB of models"
echo "⚠️  First-time generation will be slow"
echo ""
echo "Without Stable Diffusion, the system will create text placeholders."
echo ""

read -p "Install Stable Diffusion now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing Stable Diffusion packages..."
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu --break-system-packages
    pip install diffusers transformers accelerate safetensors --break-system-packages
    echo "✓ Stable Diffusion installed (CPU mode)"
else
    echo "⏭  Skipping Stable Diffusion installation"
    echo "   You can install it later with:"
    echo "   pip install torch diffusers transformers accelerate --break-system-packages"
fi

echo ""
echo "✓ Dependencies installed"
echo ""

ENDSSH

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✓ DEPLOYMENT COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 START THE SERVER:"
echo ""
echo "  ssh ${BEAST_USER}@${BEAST_IP}"
echo "  cd queztl-core"
echo "  source venv/bin/activate"
echo "  python3 backend/beast_image_generator.py"
echo ""
echo "🌐 ACCESS THE UI:"
echo ""
echo "  open frontend/beast_image_ui.html"
echo ""
echo "  Or visit: file://$(pwd)/frontend/beast_image_ui.html"
echo ""
echo "📝 NOTES:"
echo ""
echo "  - Beast API will run on port 8001"
echo "  - First generation downloads models (~7GB)"
echo "  - CPU generation takes 2-5 minutes per image"
echo "  - Images saved to: output/beast_generated_images/"
echo ""
