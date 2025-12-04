#!/bin/bash

# Queztl-Core Power Demo Script
# Showcases the system's capabilities

echo "🦅 ================================="
echo "   QUEZTL-CORE POWER DEMONSTRATION"
echo "   ================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if API is running
echo "🔍 Checking if Queztl-Core is running..."
if curl -s http://localhost:8000/api/health > /dev/null; then
    echo -e "${GREEN}✓${NC} Backend is running!"
else
    echo -e "${RED}✗${NC} Backend is not running. Start with: ./start.sh"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 STEP 1: Measure Current Power"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

POWER_RESULT=$(curl -s http://localhost:8000/api/power/measure)
POWER_SCORE=$(echo $POWER_RESULT | python3 -c "import sys, json; print(json.load(sys.stdin)['power_score'])")
CPU_USAGE=$(echo $POWER_RESULT | python3 -c "import sys, json; print(json.load(sys.stdin)['cpu']['usage_percent'])")
MEMORY_USAGE=$(echo $POWER_RESULT | python3 -c "import sys, json; print(json.load(sys.stdin)['memory']['percent'])")

echo -e "${BLUE}Power Score:${NC} $POWER_SCORE / 100"
echo -e "${BLUE}CPU Usage:${NC} $CPU_USAGE%"
echo -e "${BLUE}Memory Usage:${NC} $MEMORY_USAGE%"

sleep 2

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💪 STEP 2: Light Stress Test (5 seconds)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Running light stress test..."

STRESS_RESULT=$(curl -s -X POST "http://localhost:8000/api/power/stress-test?duration=5&intensity=light")
OPS_PER_SEC=$(echo $STRESS_RESULT | python3 -c "import sys, json; print(round(json.load(sys.stdin)['operations_per_second'], 2))")
ERROR_RATE=$(echo $STRESS_RESULT | python3 -c "import sys, json; print(round(json.load(sys.stdin)['error_rate'] * 100, 2))")
GRADE=$(echo $STRESS_RESULT | python3 -c "import sys, json; print(json.load(sys.stdin)['grade'])")

echo ""
echo -e "${GREEN}✓${NC} Test Complete!"
echo -e "${YELLOW}Operations/sec:${NC} $OPS_PER_SEC"
echo -e "${YELLOW}Error Rate:${NC} $ERROR_RATE%"
echo -e "${YELLOW}Grade:${NC} $GRADE"

sleep 2

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧠 STEP 3: Creative Training Scenario"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Generating random creative scenario..."

SCENARIO=$(curl -s -X POST http://localhost:8000/api/training/creative)
SCENARIO_NAME=$(echo $SCENARIO | python3 -c "import sys, json; print(json.load(sys.stdin)['name'])")
SCENARIO_DESC=$(echo $SCENARIO | python3 -c "import sys, json; print(json.load(sys.stdin)['description'])")

echo ""
echo -e "${BLUE}Scenario:${NC} $SCENARIO_NAME"
echo -e "${BLUE}Description:${NC} $SCENARIO_DESC"
echo ""
echo "Objectives:"
echo $SCENARIO | python3 -c "import sys, json; [print(f'  • {obj}') for obj in json.load(sys.stdin)['objectives']]"

sleep 2

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏆 STEP 4: View Creative Modes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

curl -s http://localhost:8000/api/training/creative/modes | python3 -c "
import sys, json
data = json.load(sys.stdin)
for mode in data['modes']:
    desc = data['descriptions'].get(mode, 'No description')
    print(f'  🎯 {mode.replace(\"_\", \" \").title()}: {desc}')
"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ DEMONSTRATION COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "  1. Visit the dashboard: http://localhost:3000"
echo "  2. Run full benchmark: curl -X POST http://localhost:8000/api/power/benchmark"
echo "  3. Try more stress tests: curl -X POST \"http://localhost:8000/api/power/stress-test?duration=15&intensity=medium\""
echo "  4. Check the guide: cat POWER_TRAINING_GUIDE.md"
echo ""
echo "🦅 Queztl-Core is ready to flex its power!"
