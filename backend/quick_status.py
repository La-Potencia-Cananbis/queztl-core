#!/usr/bin/env python3
"""Quick cluster status check - runs in <10 seconds"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from queztl_exec import ExecConfig, CommandExecutor, ExecMode
from queztl_config import config

print("🔍 Queztl Cluster Status Check")
print("=" * 60)

# Check Beast
try:
    exec_cfg = ExecConfig(
        mode=ExecMode.SSH,
        ssh_user=config.SSH_USER,
        ssh_host='192.168.1.105'
    )
    executor = CommandExecutor(exec_cfg)
    
    result = executor.run(['hostname'], timeout=5)
    if result.returncode == 0:
        print(f"✅ Beast (192.168.1.105): {result.stdout.strip()}")
        
        # Quick Python check
        py_result = executor.run(['python3', '--version'], timeout=5)
        if py_result.returncode == 0:
            print(f"   Python: {py_result.stdout.strip()}")
    else:
        print(f"❌ Beast: Failed (exit {result.returncode})")
except Exception as e:
    print(f"❌ Beast: Error - {e}")

# Check Docker on Beast
try:
    docker_cfg = ExecConfig(
        mode=ExecMode.SSH_DOCKER,
        ssh_user=config.SSH_USER,
        ssh_host='192.168.1.105',
        docker_container='ray-worker'
    )
    docker_exec = CommandExecutor(docker_cfg)
    
    result = docker_exec.run(['whoami'], timeout=5)
    if result.returncode == 0:
        print(f"✅ Beast Docker (ray-worker): user={result.stdout.strip()}")
    else:
        print(f"❌ Beast Docker: Failed")
except Exception as e:
    print(f"❌ Beast Docker: Error - {e}")

print("=" * 60)
print("✅ Status check complete")
