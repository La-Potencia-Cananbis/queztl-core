#!/usr/bin/env python3
"""
Quick setup helper for Queztl cluster execution
Discovers nodes and configures executor
"""

import subprocess
import sys
from pathlib import Path

def find_node_ip(node_name: str) -> str:
    """Use nmap to find a node's current DHCP IP"""
    try:
        # Try SSH config first
        result = subprocess.run(
            ['ssh', '-G', node_name],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('hostname '):
                    return line.split()[1]
    except:
        pass
    
    # Fallback to nmap scan
    print(f"🔍 Scanning network for {node_name}...")
    try:
        result = subprocess.run(
            ['nmap', '-sn', '192.168.1.0/24'],
            capture_output=True,
            text=True,
            timeout=30
        )
        # This is crude but works - look for the hostname in nmap output
        for line in result.stdout.split('\n'):
            if node_name.lower() in line.lower():
                # Find IP in previous lines
                lines = result.stdout.split('\n')
                idx = lines.index(line)
                for i in range(max(0, idx-3), idx):
                    if 'Nmap scan report for' in lines[i]:
                        ip = lines[i].split()[-1].strip('()')
                        return ip
    except Exception as e:
        print(f"⚠️  Scan failed: {e}")
    
    return None

def test_connection(host: str, user: str = 'xava') -> bool:
    """Quick SSH connectivity test"""
    try:
        result = subprocess.run(
            ['ssh', '-o', 'ConnectTimeout=3', f'{user}@{host}', 'echo OK'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0 and 'OK' in result.stdout
    except:
        return False

def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  Queztl Cluster Setup Helper                                ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    from queztl_config import config
    
    # Find Sloth (coordinator)
    print("🔍 Finding Sloth (coordinator)...")
    sloth_ip = find_node_ip('sloth')
    
    if sloth_ip:
        print(f"   Found: {sloth_ip}")
        if test_connection(sloth_ip, config.SSH_USER):
            print(f"   ✅ SSH connection works!")
            print()
            print(f"📝 To use this IP:")
            print(f"   export QUEZTL_SSH_HOST={sloth_ip}")
            print()
        else:
            print(f"   ⚠️  Found IP but SSH failed - check credentials")
    else:
        print(f"   ❌ Could not find Sloth")
        print(f"   💡 Manually set: export QUEZTL_SSH_HOST=<sloth-ip>")
    
    # Find Beast (GPU node)
    print()
    print("🔍 Finding Beast (GPU node)...")
    beast_ip = find_node_ip('beast')
    
    if beast_ip:
        print(f"   Found: {beast_ip}")
        if test_connection(beast_ip, config.SSH_USER):
            print(f"   ✅ SSH connection works!")
            print()
            print(f"📝 To use this IP:")
            print(f"   export QUEZTL_BEAST_IP={beast_ip}")
            print()
        else:
            print(f"   ⚠️  Found IP but SSH failed")
    else:
        print(f"   ❌ Could not find Beast")
        print(f"   💡 Manually set: export QUEZTL_BEAST_IP=<beast-ip>")
    
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📋 Current config:")
    print()
    print(config.summary())

if __name__ == "__main__":
    main()
