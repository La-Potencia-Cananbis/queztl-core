#!/bin/bash

echo "🦅 QUEZTL WEB GPU DRIVER TEST SUITE"
echo "=========================================="
echo

echo "1️⃣  Testing GPU Capabilities..."
curl -s http://localhost:8000/api/gpu/capabilities | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'✅ Vendor: {data[\"vendor\"]}')
print(f'✅ Renderer: {data[\"renderer\"]}')
print(f'✅ Parallel Threads: {data[\"parallel_threads\"]:,}')
print(f'✅ Compute Shaders: {\"Yes\" if data[\"compute_shader_support\"] else \"No\"}')
print(f'✅ Extensions: {len(data[\"extensions\"])} available')
"
echo

echo "2️⃣  Running WebGL Benchmark..."
curl -s -X POST http://localhost:8000/api/gpu/benchmark/webgl | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'🎮 Duration: {data[\"duration_ms\"]:.2f} ms')
print(f'🎮 Commands: {data[\"commands_executed\"]}')
print(f'🎮 Triangles: {data[\"result\"][\"stats\"][\"triangles_rendered\"]}')
print(f'🎮 Grade: {data[\"grade\"]}')
"
echo

echo "3️⃣  Running Compute Shader Benchmark..."
curl -s -X POST http://localhost:8000/api/gpu/benchmark/compute | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'⚡ Total Threads: {data[\"total_threads\"]:,}')
print(f'⚡ Duration: {data[\"duration_ms\"]:.3f} ms')
print(f'⚡ Throughput: {data[\"threads_per_second\"] / 1e9:.2f} B threads/sec')
print(f'⚡ Grade: {data[\"grade\"]}')
print(f'⚡ vs RTX 3080: {data[\"comparison\"][\"nvidia_rtx_3080\"][\"ratio\"] * 100:.2f}%')
"
echo

echo "4️⃣  Testing Rotating Cube Demo..."
curl -s -X POST http://localhost:8000/api/gpu/demo/rotating-cube | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'🎲 {data[\"message\"]}')
print(f'🎲 Triangles Rendered: {data[\"triangles_rendered\"]}')
print(f'🎲 Draw Calls: {data[\"draw_calls\"]}')
print(f'🎲 Integration: {data[\"web_integration\"]}')
"
echo

echo "5️⃣  Getting GPU Statistics..."
curl -s http://localhost:8000/api/gpu/stats | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'📊 Buffers: {data[\"driver_stats\"][\"buffers\"]}')
print(f'📊 Shaders: {data[\"driver_stats\"][\"shaders\"]}')
print(f'📊 Triangles: {data[\"driver_stats\"][\"triangles_rendered\"]:,}')
print(f'📊 Grade: {data[\"performance\"][\"grade\"]} - {data[\"performance\"][\"description\"]}')
"
echo

echo "=========================================="
echo "✅ ALL TESTS COMPLETE!"
echo "🖥️  Demo page: http://localhost:3000/gpu-demo.html"
