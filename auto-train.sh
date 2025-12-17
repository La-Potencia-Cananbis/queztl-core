#!/bin/bash
# Auto-install all high-priority training modules

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                   QUEZTL AUTO-TRAINING SYSTEM                              ║"
echo "║                   Installing High-Priority Modules                         ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# High-priority modules
MODULES=(
    "image-to-3d"
    "enhanced-3d"
    "gis-lidar"
    "geophysics-magnetic"
)

# Track results
SUCCESS=0
FAILED=0
FAILED_MODULES=()

# Check dependencies first
echo "🔍 Checking dependencies..."
./qtm check-deps

echo ""
echo "Press Enter to start training, or Ctrl+C to cancel..."
read

START_TIME=$(date +%s)

# Train each module
for module in "${MODULES[@]}"; do
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🚀 Training: $module"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if ./qtm install "$module"; then
        echo "✅ $module - SUCCESS"
        ((SUCCESS++))
    else
        echo "❌ $module - FAILED"
        ((FAILED++))
        FAILED_MODULES+=("$module")
    fi
done

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
MINUTES=$((DURATION / 60))
SECONDS=$((DURATION % 60))

# Summary
echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                         TRAINING SUMMARY                                   ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "✅ Successful: $SUCCESS"
echo "❌ Failed: $FAILED"
echo "⏱️  Total time: ${MINUTES}m ${SECONDS}s"
echo ""

if [ $FAILED -gt 0 ]; then
    echo "Failed modules:"
    for module in "${FAILED_MODULES[@]}"; do
        echo "  - $module"
    done
    echo ""
fi

# Show final status
./qtm status

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                   Training Complete! 🎉                                    ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
