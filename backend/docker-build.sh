#!/bin/bash
# Quick compile script

echo "🔨 Compiling QuetzalCore Hypervisor in Docker..."
echo ""

docker run --rm \
    -v $(pwd)/quetzalcore-hypervisor:/workspace/quetzalcore-hypervisor \
    quetzalcore-builder \
    bash -c '
        cd /workspace/quetzalcore-hypervisor/core && \
        echo "📦 Building release binary..." && \
        cargo build --release && \
        echo "" && \
        echo "✅ Build complete!" && \
        echo "📍 Binary: quetzalcore-hypervisor/core/target/release/quetzalcore-hv" && \
        ls -lh target/release/quetzalcore-hv
    '

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Hypervisor compiled successfully!"
    echo "📦 Binary location: quetzalcore-hypervisor/core/target/release/quetzalcore-hv"
    echo ""
    echo "⚠️  Note: Binary compiled for Linux, won't run directly on macOS"
    echo "   But can be deployed to Linux servers!"
else
    echo "❌ Build failed"
fi
