#!/bin/bash
# 🧠🔒 Test Hybrid Intelligence + Security Systems
# Running in PARALLEL

echo "🦅 TESTING QUETZALCORE SYSTEMS IN PARALLEL"
echo "=========================================="
echo ""

API_URL="https://queztl-core-backend.onrender.com"

# Test 1: Backend Health (no auth needed)
echo "1️⃣ Testing Backend Health..."
curl -s $API_URL/ | head -50 &
PID1=$!

# Test 2: Check if hybrid intelligence is loaded
echo "2️⃣ Testing Hybrid Intelligence availability..."
curl -s "$API_URL/api/hybrid/status" 2>&1 | head -50 &
PID2=$!

# Test 3: Test security (should fail without API key)
echo "3️⃣ Testing Security (should require API key)..."
curl -s "$API_URL/api/hybrid/process" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"task_type":"test"}' 2>&1 | head -50 &
PID3=$!

# Test 4: Test rate limiting
echo "4️⃣ Testing Rate Limiting..."
for i in {1..5}; do
  curl -s "$API_URL/" > /dev/null 2>&1 &
done
echo "   Sent 5 rapid requests to test rate limiting" &
PID4=$!

# Test 5: Existing 5K renderer
echo "5️⃣ Testing 5K Renderer (existing)..."
curl -s -X POST "$API_URL/api/render/5k" \
  -H "Content-Type: application/json" \
  -d '{"scene_type":"benchmark","width":1920,"height":1080}' 2>&1 | head -50 &
PID5=$!

# Wait for all parallel tests
echo ""
echo "⏳ Running all tests in parallel..."
wait $PID1 $PID2 $PID3 $PID4 $PID5

echo ""
echo "=========================================="
echo "✅ All parallel tests completed!"
echo ""
echo "📊 Expected Results:"
echo "  • Backend health: Should return service info"
echo "  • Hybrid Intelligence: May not be loaded yet (needs backend restart)"
echo "  • Security: Should reject requests without API key"
echo "  • Rate Limiting: Tracking requests per IP"
echo "  • 5K Renderer: Should return benchmark results"
echo ""
echo "🔑 To use secured endpoints, you need an API key!"
echo "   Generate one at: $API_URL/api/security/generate-key"
