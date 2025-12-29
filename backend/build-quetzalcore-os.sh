#!/bin/bash
# 🐧 QuetzalCore Custom OS Build Script

set -e

echo "🐧 QuetzalCore Custom Linux OS Builder"
echo "======================================"
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

MISSING=""

if ! command -v curl &> /dev/null; then
    MISSING="$MISSING curl"
fi

if ! command -v make &> /dev/null; then
    MISSING="$MISSING make"
fi

if ! command -v gcc &> /dev/null; then
    MISSING="$MISSING gcc"
fi

if ! command -v python3 &> /dev/null; then
    MISSING="$MISSING python3"
fi

if [ -n "$MISSING" ]; then
    echo "❌ Missing required tools:$MISSING"
    echo ""
    echo "Install on Ubuntu/Debian:"
    echo "  sudo apt-get install build-essential curl python3 libelf-dev bc flex bison libssl-dev"
    echo ""
    echo "Install on macOS:"
    echo "  brew install curl make gcc python3"
    echo ""
    exit 1
fi

echo "✅ All prerequisites satisfied"
echo ""

# Run the OS builder
echo "🔨 Starting QuetzalCore OS build..."
echo ""

cd "$(dirname "$0")"

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo "❌ backend directory not found"
    echo "Please run this script from the project root"
    exit 1
fi

# Run the Python builder
python3 backend/quetzalcore_os_builder.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ QuetzalCore OS build complete!"
    echo ""
    echo "📁 Build artifacts:"
    echo "  - Kernel: quetzalcore-os/linux-6.6.10/arch/x86/boot/bzImage"
    echo "  - Initramfs: quetzalcore-os/initramfs.cpio.gz"
    echo "  - ISO: quetzalcore-os/quetzalcore-os.iso"
    echo ""
    echo "🚀 To test in QEMU:"
    echo "  qemu-system-x86_64 -cdrom quetzalcore-os/quetzalcore-os.iso -m 2G -enable-kvm"
    echo ""
else
    echo ""
    echo "❌ Build failed"
    exit 1
fi
