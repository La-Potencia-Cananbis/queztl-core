#!/bin/bash
# Test QueztlOS build in Docker container

set -e

echo "🐋 Building QueztlOS in Docker..."
echo ""

# Build the builder image
echo "Building Docker image..."
docker build -f infra/queztl-os/Dockerfile.builder -t queztl-builder .

echo ""
echo "✅ Builder image ready!"
echo ""
echo "🚀 Run the builder:"
echo ""
echo "# Interactive shell:"
echo "docker run -it --rm --privileged -v \$(pwd):/workspace queztl-builder"
echo ""
echo "# Build the ISO:"
echo "docker run -it --rm --privileged -v \$(pwd):/workspace queztl-builder sudo /workspace/infra/queztl-os/build-distro.sh"
echo ""
echo "# Test bootstrap installer:"
echo "docker run -it --rm -v \$(pwd):/workspace queztl-builder /workspace/infra/queztl-os/queztl-bootstrap --help"
echo ""

read -p "Start interactive builder? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker run -it --rm --privileged \
        -v $(pwd):/workspace \
        -v /tmp/queztl-build:/tmp/queztl-os-build \
        queztl-builder
fi
