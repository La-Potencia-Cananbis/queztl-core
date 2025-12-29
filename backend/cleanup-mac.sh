#!/bin/bash
# 🧹 CLEANUP YOUR MAC
# Removes all temporary files, build artifacts, and unnecessary installs
# Keeps only: source code, configs, and documentation

set -e

echo "🧹 QUETZALCORE - Mac Cleanup Script"
echo "==============================="
echo ""
echo "This will remove:"
echo "  ✓ Rust toolchain (~2GB)"
echo "  ✓ Ubuntu ISO downloads"
echo "  ✓ Docker build artifacts"
echo "  ✓ Temporary build files"
echo "  ✓ Node modules (~500MB)"
echo "  ✓ Python cache files"
echo "  ✓ Cargo build artifacts"
echo ""
echo "This will KEEP:"
echo "  ✓ Source code"
echo "  ✓ Configuration files"
echo "  ✓ Documentation"
echo "  ✓ Deployed apps (on cloud)"
echo ""
read -p "Proceed with cleanup? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 0
fi

BYTES_FREED=0

# Function to track freed space
freed() {
    size=$1
    BYTES_FREED=$((BYTES_FREED + size))
}

echo ""
echo "Starting cleanup..."
echo ""

# Remove Rust toolchain (if installed by our scripts)
if [ -d "$HOME/.cargo" ]; then
    echo "🦀 Removing Rust toolchain..."
    RUST_SIZE=$(du -sk "$HOME/.cargo" 2>/dev/null | cut -f1 || echo "0")
    rm -rf "$HOME/.cargo"
    rm -rf "$HOME/.rustup"
    freed $RUST_SIZE
    echo "   ✅ Freed ~$((RUST_SIZE / 1024))MB"
fi

# Remove Ubuntu ISOs
echo "💿 Removing Ubuntu ISOs..."
ISO_SIZE=0
if [ -f "$HOME/Downloads/ubuntu-22.04.3-live-server-arm64.iso" ]; then
    ISO_SIZE=$(du -sk "$HOME/Downloads/ubuntu-22.04.3-live-server-arm64.iso" 2>/dev/null | cut -f1 || echo "0")
    rm -f "$HOME/Downloads/ubuntu-22.04.3-live-server-arm64.iso"
    freed $ISO_SIZE
    echo "   ✅ Freed ~$((ISO_SIZE / 1024))MB"
else
    echo "   ℹ️  No ISOs found"
fi

# Remove Docker images
if command -v docker &> /dev/null && docker info > /dev/null 2>&1; then
    echo "🐳 Removing Docker build images..."
    docker rmi quetzalcore-builder 2>/dev/null && echo "   ✅ Removed quetzalcore-builder image" || echo "   ℹ️  No build images found"
    
    # Prune unused Docker data
    DOCKER_BEFORE=$(docker system df -v 2>/dev/null | grep "Total" | awk '{print $4}' || echo "0B")
    docker system prune -af --volumes > /dev/null 2>&1
    echo "   ✅ Pruned Docker cache"
fi

# Clean node_modules
echo "📦 Cleaning node_modules..."
NODE_SIZE=0
if [ -d "node_modules" ]; then
    NODE_SIZE=$(du -sk node_modules 2>/dev/null | cut -f1 || echo "0")
    rm -rf node_modules
    freed $NODE_SIZE
    echo "   ✅ Freed ~$((NODE_SIZE / 1024))MB"
else
    echo "   ℹ️  No node_modules found"
fi

# Clean Python cache
echo "🐍 Cleaning Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
echo "   ✅ Python cache cleaned"

# Clean Rust build artifacts
echo "🦀 Cleaning Rust build artifacts..."
if [ -d "quetzalcore-hypervisor/core/target" ]; then
    CARGO_SIZE=$(du -sk quetzalcore-hypervisor/core/target 2>/dev/null | cut -f1 || echo "0")
    rm -rf quetzalcore-hypervisor/core/target
    freed $CARGO_SIZE
    echo "   ✅ Freed ~$((CARGO_SIZE / 1024))MB"
else
    echo "   ℹ️  No Cargo artifacts found"
fi

# Remove log files
echo "📝 Cleaning log files..."
rm -f *.log
rm -f nohup.out
echo "   ✅ Logs cleaned"

# Remove temporary files
echo "🗑️  Removing temporary files..."
rm -f .DS_Store
rm -f *.tmp
rm -f .vm-setup-resume
find . -name ".DS_Store" -delete 2>/dev/null || true
echo "   ✅ Temp files removed"

# Clean Homebrew cache (optional)
if command -v brew &> /dev/null; then
    echo "🍺 Cleaning Homebrew cache..."
    BREW_BEFORE=$(du -sk "$(brew --cache)" 2>/dev/null | cut -f1 || echo "0")
    brew cleanup > /dev/null 2>&1 || true
    BREW_AFTER=$(du -sk "$(brew --cache)" 2>/dev/null | cut -f1 || echo "0")
    BREW_FREED=$((BREW_BEFORE - BREW_AFTER))
    freed $BREW_FREED
    echo "   ✅ Freed ~$((BREW_FREED / 1024))MB"
fi

# Remove downloaded setup scripts we don't need anymore
echo "🗂️  Cleaning setup scripts..."
rm -f setup-docker-builder.sh
rm -f setup-local-vm.sh
rm -f quick-start-vm.sh
rm -f one-click-vm.sh
rm -f setup-vm-environment.sh
echo "   ✅ Setup scripts removed"

echo ""
echo "==============================="
echo "✅ CLEANUP COMPLETE"
echo "==============================="
echo ""
echo "📊 Estimated space freed: ~$((BYTES_FREED / 1024 / 1024))GB"
echo ""
echo "✨ Your Mac is clean!"
echo ""
echo "📁 Kept:"
echo "   • /Users/xavasena/hive (source code)"
echo "   • .venv (Python environment)"
echo "   • Configuration files"
echo "   • Documentation"
echo ""
echo "☁️  Your apps are still running on:"
echo "   • https://senasaitech.com (frontend)"
echo "   • https://hive-backend.onrender.com (backend)"
echo "   • https://10.112.221.224:9999 (mobile dashboard)"
echo ""
echo "💡 To rebuild anything, use cloud workers:"
echo "   ./setup-cloud-workers.sh"
echo ""
