#!/bin/bash

echo "🦅 QUEZTL-CORE BEAST MODE TEST"
echo "=============================="
echo ""
echo "This script will unleash the BEAST with:"
echo "  🎮 3D Graphics & Ray Tracing"
echo "  ⛏️  Crypto Mining Simulation"
echo "  🔥 EXTREME Combined Workload"
echo ""
read -p "Press Enter to start the beast tests..."

# 3D Workload - Medium
echo ""
echo "🎮 Running 3D Graphics Workload (Medium)..."
echo "Matrix operations + Ray tracing"
curl -s -X POST "http://localhost:8000/api/workload/3d?matrix_size=512&num_iterations=100&ray_count=10000" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"\\n📊 3D RESULTS\")
print(f\"Grade: {data['grade']}\")
print(f\"GFLOPS: {data['gflops']}\")
print(f\"Duration: {data['duration']:.2f}s\")
print(f\"Matrix Ops: {data['metrics']['matrix_operations']:,}\")
print(f\"Ray Hits: {data['metrics']['ray_intersections']:,}\")
print(f\"\\nComparison to GPUs:\")
for gpu, perf in data['comparison'].items():
    print(f\"  {gpu}: {perf}\")
"

echo ""
read -p "Press Enter for crypto mining test..."

# Mining Workload - Medium
echo ""
echo "⛏️  Running Crypto Mining Simulation (Medium)..."
echo "SHA-256 hashing + Proof-of-Work"
curl -s -X POST "http://localhost:8000/api/workload/mining?difficulty=4&num_blocks=5&parallel=true&num_workers=4" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"\\n📊 MINING RESULTS\")
print(f\"Grade: {data['grade']}\")
print(f\"Hash Rate: {data['hash_rate_display']}\")
print(f\"Duration: {data['duration']:.2f}s\")
print(f\"Blocks Mined: {data['blocks_mined']}\")
print(f\"Total Hashes: {data['total_hashes']:,}\")
print(f\"Workers: {data['workers']}\")
print(f\"\\nComparison to miners:\")
for miner, perf in data['comparison'].items():
    print(f\"  {miner}: {perf}\")
"

echo ""
read -p "Press Enter to UNLEASH THE BEAST (30-second extreme test)..."

# EXTREME Combined Workload
echo ""
echo "🔥🔥🔥 UNLEASHING THE BEAST! 🔥🔥🔥"
echo "Running 3D + Mining simultaneously for 30 seconds..."
echo "(This will push your system to MAXIMUM stress)"
echo ""

curl -s -X POST "http://localhost:8000/api/workload/extreme?duration_seconds=30" | python3 -c "
import sys, json
data = json.load(sys.stdin)

print(f\"\\n\" + \"=\"*60)
print(f\"🏆 BEAST MODE RESULTS\")
print(f\"=\"*60)
print(f\"\\n🎯 Overall Grade: {data['grade']}\")
print(f\"📊 Combined Score: {data['combined_score']:.2f}/100\")
print(f\"⚡ Beast Level: {data['beast_level']}\")
print(f\"⏱️  Duration: {data['duration']:.2f}s\")
print(f\"\\n{data['description']}\")

print(f\"\\n🎮 GPU Workload:\")
gpu = data['gpu_workload']
if 'error' not in gpu:
    print(f\"  GFLOPS: {gpu['gflops']}\")
    print(f\"  Grade: {gpu['grade']}\")
    print(f\"  Matrix Ops: {gpu['metrics']['matrix_operations']:,}\")
    
print(f\"\\n⛏️  Mining Workload:\")
mining = data['mining_workload']
if 'error' not in mining:
    print(f\"  Hash Rate: {mining['hash_rate_display']}\")
    print(f\"  Grade: {mining['grade']}\")
    print(f\"  Blocks Mined: {mining['blocks_mined']}\")
    
print(f\"\\n💻 System Metrics:\")
sys_met = data['system_metrics']
print(f\"  Peak CPU: {sys_met['peak_cpu_percent']:.1f}%\")
print(f\"  Memory Used: {sys_met['memory_used_mb']:.1f} MB\")
print(f\"  CPU Cores: {sys_met['cpu_cores']}\")

print(f\"\\n\" + \"=\"*60)

if data['grade'] == 'S':
    print(f\"\\n🌟🌟🌟 S-GRADE BEAST! 🌟🌟🌟\")
    print(f\"Your system is CRUSHING IT!\")
elif data['grade'] == 'A':
    print(f\"\\n⭐⭐ A-GRADE EXCELLENCE! ⭐⭐\")
    print(f\"Outstanding performance!\")
else:
    print(f\"\\n✅ Solid performance! Keep optimizing!\")

print(f\"\\n\" + \"=\"*60)
"

echo ""
echo "✅ Beast Mode Test Complete!"
echo ""
echo "Check the dashboard at http://localhost:3000 to see the results!"
