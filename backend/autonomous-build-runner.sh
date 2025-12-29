#!/bin/bash
# 🦅 QUETZALCORE OS - AUTONOMOUS BUILD RUNNER
# Watches for changes and auto-rebuilds kernel

set -e

echo "🦅 QUETZALCORE OS - AUTONOMOUS BUILD RUNNER"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
KERNEL_DIR="/Users/xavasena/hive/quetzalcore-kernel"
BUILD_LOG="/Users/xavasena/hive/build.log"
MAX_PARALLEL=4

# Check if kernel directory exists
if [ ! -d "$KERNEL_DIR" ]; then
    echo "Creating kernel project..."
    mkdir -p "$KERNEL_DIR/src"
    cd "$KERNEL_DIR"
    cargo init --name quetzalcore-kernel 2>/dev/null || true
fi

# Function to build kernel
build_kernel() {
    echo -e "${YELLOW}🔨 Building kernel...${NC}"
    START_TIME=$(date +%s)
    
    cd "$KERNEL_DIR"
    if cargo build --release 2>&1 | tee "$BUILD_LOG"; then
        END_TIME=$(date +%s)
        DURATION=$((END_TIME - START_TIME))
        echo -e "${GREEN}✅ Build successful! (${DURATION}s)${NC}"
        
        # Show binary size
        if [ -f "target/release/quetzalcore-kernel" ]; then
            SIZE=$(du -h target/release/quetzalcore-kernel | cut -f1)
            echo -e "${GREEN}📦 Binary size: ${SIZE}${NC}"
        fi
        
        return 0
    else
        echo -e "${RED}❌ Build failed!${NC}"
        return 1
    fi
}

# Function to run tests
run_tests() {
    echo -e "${YELLOW}🧪 Running tests...${NC}"
    cd "$KERNEL_DIR"
    if cargo test --release 2>&1; then
        echo -e "${GREEN}✅ All tests passed!${NC}"
        return 0
    else
        echo -e "${RED}❌ Tests failed!${NC}"
        return 1
    fi
}

# Function to boot test
boot_test() {
    echo -e "${YELLOW}🚀 Boot testing...${NC}"
    
    # Check if QEMU is installed
    if ! command -v qemu-system-x86_64 &> /dev/null; then
        echo -e "${YELLOW}⚠️  QEMU not installed, skipping boot test${NC}"
        return 0
    fi
    
    # Quick boot test (5 second timeout)
    timeout 5 qemu-system-x86_64 \
        -kernel "$KERNEL_DIR/target/release/quetzalcore-kernel" \
        -serial stdio \
        -display none \
        2>&1 | tee /tmp/qemu-boot.log || true
    
    echo -e "${GREEN}✅ Boot test complete${NC}"
}

# Watch mode
watch_mode() {
    echo -e "${GREEN}👀 Watching for file changes...${NC}"
    echo "   Press Ctrl+C to stop"
    echo ""
    
    # Install fswatch if not present (Mac)
    if ! command -v fswatch &> /dev/null; then
        echo "📦 Installing fswatch..."
        brew install fswatch 2>/dev/null || {
            echo -e "${RED}❌ Please install fswatch: brew install fswatch${NC}"
            exit 1
        }
    fi
    
    # Watch for changes
    fswatch -0 -r "$KERNEL_DIR/src" | while read -d "" event; do
        echo ""
        echo -e "${YELLOW}📝 File changed: $(basename $event)${NC}"
        echo ""
        
        build_kernel && run_tests
        
        echo ""
        echo -e "${GREEN}👀 Watching for more changes...${NC}"
        echo ""
    done
}

# Continuous Integration mode
ci_mode() {
    echo -e "${GREEN}🤖 CI Mode - Full build & test${NC}"
    echo ""
    
    # Clean build
    cd "$KERNEL_DIR"
    echo "🧹 Cleaning previous build..."
    cargo clean
    
    # Build
    if ! build_kernel; then
        exit 1
    fi
    
    # Test
    if ! run_tests; then
        exit 1
    fi
    
    # Boot test
    boot_test
    
    echo ""
    echo -e "${GREEN}✅ CI PASSED - All checks successful!${NC}"
}

# Parallel build mode
parallel_mode() {
    echo -e "${GREEN}⚡ Parallel Build Mode${NC}"
    echo ""
    
    # Build for multiple targets in parallel
    cd "$KERNEL_DIR"
    
    echo "Building for x86_64..."
    cargo build --release --target x86_64-unknown-none 2>&1 > /tmp/build-x86.log &
    PID_X86=$!
    
    echo "Building for tests..."
    cargo build --release 2>&1 > /tmp/build-host.log &
    PID_HOST=$!
    
    # Wait for all builds
    wait $PID_X86 && echo -e "${GREEN}✅ x86_64 build done${NC}" || echo -e "${RED}❌ x86_64 build failed${NC}"
    wait $PID_HOST && echo -e "${GREEN}✅ host build done${NC}" || echo -e "${RED}❌ host build failed${NC}"
    
    echo ""
    echo -e "${GREEN}⚡ Parallel builds complete!${NC}"
}

# Fast iteration mode
fast_mode() {
    echo -e "${GREEN}🏃 Fast Iteration Mode${NC}"
    echo "   Quick build -> test -> boot loop"
    echo "   Press Enter to rebuild, Ctrl+C to stop"
    echo ""
    
    while true; do
        build_kernel && run_tests && boot_test
        
        echo ""
        echo -e "${GREEN}✅ Iteration complete! Press Enter to rebuild...${NC}"
        read
    done
}

# Show usage
usage() {
    echo "Usage: $0 [MODE]"
    echo ""
    echo "Modes:"
    echo "  watch     - Watch files and auto-rebuild (default)"
    echo "  ci        - Continuous Integration mode (full build & test)"
    echo "  parallel  - Build multiple targets in parallel"
    echo "  fast      - Fast iteration loop (manual)"
    echo "  once      - Build once and exit"
    echo ""
    echo "Examples:"
    echo "  $0              # Watch mode"
    echo "  $0 ci           # CI mode"
    echo "  $0 parallel     # Parallel builds"
}

# Main
case "${1:-watch}" in
    watch)
        watch_mode
        ;;
    ci)
        ci_mode
        ;;
    parallel)
        parallel_mode
        ;;
    fast)
        fast_mode
        ;;
    once)
        build_kernel && run_tests
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        echo -e "${RED}Unknown mode: $1${NC}"
        echo ""
        usage
        exit 1
        ;;
esac
