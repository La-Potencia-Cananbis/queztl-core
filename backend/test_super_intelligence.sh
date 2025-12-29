#!/bin/bash
# 🧠🔥 TEST SUPER INTELLIGENCE SYSTEM
# Analyze competitors, datasets, generate winning strategies

API_URL="https://queztl-core-backend.onrender.com"

echo "🦅 TESTING SUPER INTELLIGENCE SYSTEM"
echo "=========================================="
echo ""
echo "⏳ Waiting 60s for Render to deploy new code..."
sleep 60
echo ""

# Test 1: Check if Super Intelligence is loaded
echo "1️⃣ Testing Super Intelligence Status..."
curl -s "$API_URL/api/super/status" | python3 -m json.tool || echo "Not loaded yet"
echo ""
echo ""

# Test 2: Analyze competitors in 5K rendering domain
echo "2️⃣ Analyzing Competitors in 5K Rendering..."
curl -s -X POST "$API_URL/api/super/analyze-competitors?domain=5k_rendering" | python3 -m json.tool || echo "Error"
echo ""
echo ""

# Test 3: Analyze large dataset
echo "3️⃣ Analyzing Massive Dataset..."
curl -s -X POST "$API_URL/api/super/analyze-data?dataset=video_ai_market&source=industry" | python3 -m json.tool || echo "Error"
echo ""
echo ""

# Test 4: Generate winning strategy
echo "4️⃣ Generating Winning Strategy to Dominate Video AI..."
curl -s -X POST "$API_URL/api/super/winning-strategy?objective=dominate_video_ai" | python3 -m json.tool || echo "Error"
echo ""
echo ""

echo "=========================================="
echo "✅ Super Intelligence Test Complete!"
echo ""
echo "🔥 CAPABILITIES:"
echo "  • Competitor Analysis"
echo "  • Large Dataset Processing"
echo "  • Winning Strategy Generation"
echo "  • Auto-Implementation"
echo ""
echo "📊 Use these endpoints to:"
echo "  • Find competitor weaknesses"
echo "  • Analyze market data"
echo "  • Generate attack strategies"
echo "  • Auto-implement improvements"
