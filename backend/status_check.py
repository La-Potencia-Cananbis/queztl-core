#!/usr/bin/env python3
"""
Quick Status Check for Autonomous Distributed System

Run this anytime to check what's happening with the autonomous agents.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from distributed_agent_wrapper import DistributedAgent
from queztl_config import config

print("╔════════════════════════════════════════════════════════════════╗")
print("║  Distributed Agent Status Check                                ║")
print("╚════════════════════════════════════════════════════════════════╝")
print()

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"🕐 Status as of: {timestamp}")
print()

# Check Beast connectivity
print("🔍 Checking Beast (192.168.1.105)...")
try:
    agent = DistributedAgent("StatusCheck", node='beast', use_docker=False)
    
    # Get hostname
    result = agent.execute(['hostname'])
    if result.returncode == 0:
        print(f"   ✅ Connected to: {result.stdout.strip()}")
    else:
        print(f"   ❌ Connection failed")
        sys.exit(1)
    
    # Check uptime
    result = agent.execute(['uptime', '-p'])
    if result.returncode == 0:
        print(f"   ⏱️  Uptime: {result.stdout.strip()}")
    
    # Check load
    result = agent.execute(['cat', '/proc/loadavg'])
    if result.returncode == 0:
        load = result.stdout.strip().split()[:3]
        print(f"   📊 Load average: {' '.join(load)}")
    
    # Check Docker containers
    print()
    print("🐳 Docker containers:")
    result = agent.execute(['docker', 'ps', '--format', '{{.Names}}\t{{.Status}}'])
    if result.returncode == 0:
        for line in result.stdout.strip().split('\n'):
            if line:
                name, status = line.split('\t', 1)
                print(f"   • {name}: {status}")
    
    # Check Python environment in ray-worker
    print()
    print("🐍 Python environment (ray-worker):")
    agent_docker = DistributedAgent("DockerCheck", node='beast', use_docker=True)
    caps = agent_docker.check_capabilities()
    print(f"   • Python: {caps.get('python', 'N/A')}")
    print(f"   • PyTorch: {caps.get('pytorch', 'Not installed')}")
    print(f"   • CUDA: {caps.get('cuda', False)}")
    print(f"   • CPUs: {caps.get('cpu_count', 'N/A')}")
    
    print()
    print("✅ All systems operational")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print()
print("╚════════════════════════════════════════════════════════════════╝")
