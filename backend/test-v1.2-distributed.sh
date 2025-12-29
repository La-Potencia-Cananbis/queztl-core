#!/bin/bash
# Test v1.2 Distributed Network & Auto-Scaling

echo "🚀 QUEZTL-CORE v1.2 - Distributed Network Test"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if backend is running
echo -e "${BLUE}1. Checking backend status...${NC}"
if curl -s http://localhost:8000/api/health > /dev/null; then
    echo -e "${GREEN}✅ Backend is running${NC}"
else
    echo -e "${YELLOW}⚠️  Backend not running. Starting...${NC}"
    cd backend && python -m uvicorn main:app --reload --port 8000 &
    sleep 5
fi

echo ""
echo -e "${BLUE}2. Checking distributed network status...${NC}"
NETWORK_STATUS=$(curl -s http://localhost:8000/api/v1.2/network/status)
echo "$NETWORK_STATUS" | python3 -m json.tool | head -20

echo ""
echo -e "${BLUE}3. Checking auto-scaler status...${NC}"
SCALER_STATUS=$(curl -s http://localhost:8000/api/v1.2/autoscaler/status)
echo "$SCALER_STATUS" | python3 -m json.tool

echo ""
echo -e "${BLUE}4. Submitting test workload (LLM Inference)...${NC}"
TASK_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1.2/workload/submit \
  -H "Content-Type: application/json" \
  -d '{
    "workload_type": "llm_inference",
    "payload": {"model_size": "7B"},
    "priority": 8
  }')
echo "$TASK_RESPONSE" | python3 -m json.tool

TASK_ID=$(echo "$TASK_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['task_id'])")
echo -e "${GREEN}✅ Task submitted: $TASK_ID${NC}"

echo ""
echo -e "${BLUE}5. Running real-world benchmarks...${NC}"
echo -e "${YELLOW}(This will take ~60 seconds)${NC}"

curl -s http://localhost:8000/api/v1.2/benchmarks/realworld | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('\n📊 BENCHMARK RESULTS:')
print('=' * 60)
for bench in data['benchmarks']:
    print(f\"\n🔹 {bench['name']}\")
    print(f\"   Score: {bench['score']:.2f} {bench['unit']}\")
    print(f\"   Time: {bench['execution_time']:.2f}s\")
    if bench.get('comparison'):
        print(\"   Comparison:\")
        for hw, score in list(bench['comparison'].items())[:3]:
            percent = (bench['score'] / score) * 100
            print(f\"      {hw}: {percent:.1f}%\")
print('=' * 60)
"

echo ""
echo -e "${BLUE}6. Testing manual scaling...${NC}"

echo -e "${YELLOW}Scaling UP by 2 nodes...${NC}"
curl -s -X POST http://localhost:8000/api/v1.2/scale/manual \
  -H "Content-Type: application/json" \
  -d '{"action": "up", "count": 2}' | python3 -m json.tool

sleep 3

echo -e "${YELLOW}Current node count:${NC}"
curl -s http://localhost:8000/api/v1.2/network/status | \
  python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"Nodes: {data['registry']['total_nodes']}\")"

echo ""
echo -e "${GREEN}✅ v1.2 Test Complete!${NC}"
echo ""
echo "📚 Next steps:"
echo "  - View network status: curl http://localhost:8000/api/v1.2/network/status"
echo "  - Submit workloads: curl -X POST http://localhost:8000/api/v1.2/workload/submit ..."
echo "  - Read docs: cat V1.2_DISTRIBUTED_SCALING.md"
echo ""
