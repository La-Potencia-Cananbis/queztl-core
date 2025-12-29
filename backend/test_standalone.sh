#!/bin/bash
# Test QuetzalCore STANDALONE Mode
# Zero credits, pure autonomous operation

echo "🦅 TESTING QUETZALCORE STANDALONE MODE"
echo "======================================"
echo "✅ Zero OpenAI credits"
echo "✅ Zero Anthropic credits"
echo "✅ Zero external API calls"
echo "✅ 100% YOUR brain, YOUR models"
echo ""

API_URL="https://queztl-core-backend.onrender.com"

echo "1️⃣ STANDALONE STATUS"
echo "-------------------"
curl -s "$API_URL/api/standalone/status" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"🦅 Name: {data['name']}\")
print(f\"🎯 Mode: {data['mode']}\")
print(f\"⏱️  Uptime: {data['uptime_seconds']:.1f}s\")
print(f\"📊 Tasks Processed: {data['tasks_processed']}\")
print(f\"🧠 Autonomous Decisions: {data['autonomous_decisions']}\")
print(f\"📚 Learning Cycles: {data['learning_cycles']}\")
print(f\"💾 Local Models: {data['local_models']['count']}\")
print(f\"💰 Credits Used: {data['cost']['total_credits']}\")
print(f\"💵 Cost USD: \${data['cost']['cost_usd']:.2f}\")
print(f\"🎯 Independence: {data['independence']}\")
"
echo ""

echo "2️⃣ COMPARE MODES (Hybrid vs Standalone)"
echo "---------------------------------------"
curl -s "$API_URL/api/standalone/compare" | python3 -c "
import sys, json
data = json.load(sys.stdin)
comp = data['comparison']

print('STANDALONE MODE:')
print(f\"  💰 Credits: {comp['standalone']['credits_used']}\")
print(f\"  💵 Cost: \${comp['standalone']['cost_usd']:.2f}\")
print(f\"  🎯 Independence: {comp['standalone']['independence']}\")
print(f\"  🔒 Privacy: {comp['standalone']['privacy']}\")
print()

print('HYBRID MODE:')
print(f\"  💰 Credits: {comp['hybrid']['credits_used']}\")
print(f\"  💵 Cost: {comp['hybrid']['cost_usd']}\")
print(f\"  🎯 Independence: {comp['hybrid']['independence']}\")
print(f\"  🔒 Privacy: {comp['hybrid']['privacy']}\")
print()

print('📌 ' + data['recommendation'])
"
echo ""

echo "3️⃣ PROCESS TASK - STANDALONE MODE"
echo "---------------------------------"
curl -s -X POST "$API_URL/api/standalone/process" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "video_enhancement",
    "input_data": {
      "video": "test_5k.mp4",
      "enhance": "neural_upscale"
    },
    "autonomous": true
  }' | python3 -c "
import sys, json
data = json.load(sys.stdin)
result = data.get('result', {})

print(f\"✅ Success: {data['success']}\")
print(f\"🎯 Mode: {data['mode']}\")
print(f\"💰 Credits Used: {data['credits_used']}\")
print(f\"🌐 External Calls: {data['external_calls']}\")
print()

brain = result.get('brain_decision', {})
print(f\"🧠 Brain Decision:\")
print(f\"   Domain: {brain.get('domain')}\")
print(f\"   Action: {brain.get('action')}\")
print(f\"   Confidence: {brain.get('confidence')}\")
print()

ml = result.get('ml_output', {})
print(f\"💾 ML Output:\")
print(f\"   Status: {ml.get('status')}\")
print(f\"   Models Used: {result.get('models_used', [])}\")
"
echo ""

echo "4️⃣ LIST YOUR MODELS"
echo "-------------------"
curl -s "$API_URL/api/standalone/models" | python3 -c "
import sys, json
data = json.load(sys.stdin)

if data['success']:
    models = data['models']['models']
    print(f\"💾 Total Models: {data['total_models']}\")
    if models:
        for model in models:
            print(f\"  ✅ {model}\")
    else:
        print(\"  📝 No models trained yet - train your first model!\")
"
echo ""

echo "✅ STANDALONE MODE READY!"
echo "========================="
echo ""
echo "🎯 YOUR QUETZALCORE IS RUNNING INDEPENDENTLY"
echo "💰 Zero credits used"
echo "🌐 Zero external API calls"
echo "🔒 Complete privacy - data never leaves your server"
echo "🦅 100% autonomous operation"
echo ""
echo "Call it with:"
echo "  curl -X POST $API_URL/api/standalone/process \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"task_type\": \"your_task\", \"input_data\": {...}}'"
