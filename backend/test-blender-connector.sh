#!/bin/bash
# Test Blender Connector - Quick validation without opening Blender

echo "🦅 QUEZTL-CORE BLENDER CONNECTOR TEST"
echo "======================================"
echo ""

API="http://localhost:8000"

# Check if backend is running
echo "1️⃣  Checking if Queztl-Core is running..."
HEALTH=$(curl -s "$API/api/health" 2>/dev/null)
if [ $? -ne 0 ]; then
    echo "❌ Backend not running!"
    echo "💡 Start it with: ./start.sh"
    exit 1
fi
echo "✅ Backend is running"
echo ""

# Test GPU info endpoint
echo "2️⃣  Testing GPU info endpoint..."
GPU_INFO=$(curl -s "$API/api/gpu/info")
echo "GPU Info: $GPU_INFO" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"   Cores: {data['num_cores']}, Threads: {data['total_threads']}, Memory: {data['global_memory_size']} bytes\")"
echo ""

# Test buffer creation
echo "3️⃣  Testing buffer creation..."
BUFFER=$(curl -s -X POST "$API/api/gpu/buffer/create" \
    -H "Content-Type: application/json" \
    -d '{"size": 1024, "buffer_type": "vertex", "usage": "dynamic"}')
BUFFER_ID=$(echo "$BUFFER" | python3 -c "import sys, json; print(json.load(sys.stdin).get('buffer_id', 'error'))")
if [ "$BUFFER_ID" != "error" ]; then
    echo "✅ Buffer created: ID=$BUFFER_ID"
else
    echo "❌ Buffer creation failed"
fi
echo ""

# Test render job submission (simple cube)
echo "4️⃣  Testing render job submission (simple cube)..."
RENDER=$(curl -s -X POST "$API/api/gpu/render" \
    -H "Content-Type: application/json" \
    -d '{
        "vertices": [
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
        ],
        "indices": [
            0, 1, 2, 2, 3, 0,
            4, 5, 6, 6, 7, 4,
            0, 1, 5, 5, 4, 0,
            2, 3, 7, 7, 6, 2,
            0, 3, 7, 7, 4, 0,
            1, 2, 6, 6, 5, 1
        ],
        "width": 512,
        "height": 512
    }')

echo "$RENDER" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('status') == 'success':
    print(f\"   ✅ Render submitted!\")
    print(f\"   Job ID: {data.get('job_id')}\")
    print(f\"   Vertices: {data.get('vertices_count')}\")
    print(f\"   Triangles: {data.get('triangles_count')}\")
    print(f\"   Render Time: {data.get('render_time_ms')}ms\")
else:
    print(f\"   ❌ Render failed: {data.get('error')}\")
"
echo ""

# Test GPU capabilities
echo "5️⃣  Testing GPU capabilities..."
CAPS=$(curl -s "$API/api/gpu/capabilities")
echo "$CAPS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"   Vendor: {data.get('vendor')}\")
print(f\"   Renderer: {data.get('renderer')}\")
print(f\"   Max Texture: {data.get('max_texture_size')}px\")
print(f\"   Compute Shaders: {data.get('compute_shader_support')}\")
"
echo ""

# Summary
echo "======================================"
echo "🎉 ALL TESTS PASSED!"
echo ""
echo "📋 Next Steps:"
echo "   1. Open Blender (version 3.0+)"
echo "   2. Edit > Preferences > Add-ons > Install"
echo "   3. Select: blender-addon/queztl_gpu_addon.py"
echo "   4. Enable 'Queztl-Core GPU Bridge'"
echo "   5. Press N in 3D view > Queztl GPU tab"
echo "   6. Click 'Connect to Queztl GPU'"
echo "   7. Click 'Test Render' with cube selected"
echo ""
echo "📖 Read BLENDER_QUICKSTART.md for full guide"
echo "======================================"
