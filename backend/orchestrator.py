#!/usr/bin/env python3
"""
Queztl Orchestrator - Neural Network Coordinator
Manages task distribution across cluster with neurotransmitter-style messaging

Roles:
- Builder: Infrastructure setup, environment prep (runs anywhere)
- Creator: Research, design, architecture (CPU-light, can run on Sloth)
- Coder: Implementation, testing (CPU-heavy, prefers Beast)
- Morph: Transformation between states (lightweight coordinator)

Sloth = Slow memory / persistent storage / background tasks
Beast = Fast compute / real-time processing / generation
"""

import json
import subprocess
import socket
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import time

# DHCP-safe cluster host resolution
try:
    from backend.queztl_discovery import resolve_cluster_hosts, ssh_user
except ImportError:  # pragma: no cover
    from queztl_discovery import resolve_cluster_hosts, ssh_user


# Cluster configuration
# IMPORTANT: Beast/Sloth may be DHCP; avoid hardcoding IPs.
# Use env vars QUEZTL_BEAST_HOST/QUEZTL_SLOTH_HOST or best-effort discovery.

def build_nodes():
    hosts = resolve_cluster_hosts()
    return {
        "sloth": {
            "host": hosts.sloth,
            "role": "slow_memory",
            "storage_gb": 500,
            "preferred_tasks": ["builder", "creator", "orchestrator", "storage"],
            "ssh_user": ssh_user(),
        },
        "beast": {
            "host": hosts.beast,
            "role": "fast_compute",
            "storage_gb": 100,
            "preferred_tasks": ["coder", "generator", "trainer"],
            "ssh_user": ssh_user(),
        },
    }

# Resolved at runtime
NODES = build_nodes()

class Neurotransmitter:
    """Message passing between cluster nodes (like neural signals)"""
    
    def __init__(self, sender: str, task_type: str):
        self.sender = sender
        self.task_type = task_type
        self.timestamp = datetime.now().isoformat()
        self.message_id = f"{sender}_{task_type}_{int(time.time())}"
    
    def send(self, target_node: str, payload: Dict) -> bool:
        """Send signal to target node"""
        message = {
            "id": self.message_id,
            "sender": self.sender,
            "task_type": self.task_type,
            "timestamp": self.timestamp,
            "payload": payload
        }
        
        target = NODES.get(target_node)
        if not target:
            print(f"❌ Unknown target: {target_node}")
            return False
        
        # Write message to shared location
        msg_file = Path(f"/tmp/queztl_msg_{self.message_id}.json")
        msg_file.write_text(json.dumps(message, indent=2))
        
        # Send via SSH
        try:
            cmd = f"scp {msg_file} {target['ssh_user']}@{target['host']}:~/queztl-core/messages/"
            subprocess.run(cmd.split(), check=True, capture_output=True)
            print(f"📡 Signal sent: {self.sender} → {target_node} [{self.task_type}]")
            return True
        except Exception as e:
            print(f"❌ Signal failed: {e}")
            return False

class Orchestrator:
    """Coordinates tasks across cluster using neurotransmitter pattern"""
    
    def __init__(self):
        self.hostname = socket.gethostname()
        self.current_node = self.detect_node()
        self.preferred_host = "sloth"  # Orchestrator prefers Sloth
        self.task_queue = []
        
        # Create message directory
        Path("~/queztl-core/messages").expanduser().mkdir(parents=True, exist_ok=True)
    
    def detect_node(self) -> Optional[str]:
        """Detect which node we're running on.

        Prefer hostname-based detection (works with DHCP).
        """
        hn = socket.gethostname().lower()
        if 'beast' in hn:
            return 'beast'
        if 'sloth' in hn:
            return 'sloth'
        # Unknown/command-center
        return 'unknown'
    
    def check_node_health(self, node_name: str) -> Dict:
        """Check if node is responsive"""
        node = NODES.get(node_name)
        if not node:
            return {"status": "unknown"}

        if not node.get('host'):
            return {
                "status": "unconfigured",
                "node": node_name,
                "hint": "Set QUEZTL_BEAST_HOST/QUEZTL_SLOTH_HOST (or enable nmap discovery)."
            }
        
        # Ping test
        ping_result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", node['host']],
            capture_output=True
        )
        
        if ping_result.returncode != 0:
            return {"status": "offline", "node": node_name}
        
        # SSH test
        try:
            ssh_result = subprocess.run(
                ["ssh", "-o", "ConnectTimeout=3", f"{node['ssh_user']}@{node['host']}", 
                 "echo 'ok' && df -h / | awk 'NR==2 {print $5}'"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if ssh_result.returncode == 0:
                lines = ssh_result.stdout.strip().split('\n')
                disk_usage = lines[-1] if len(lines) > 1 else "unknown"
                return {
                    "status": "online",
                    "node": node_name,
                    "disk_usage": disk_usage,
                    "host": node['host']
                }
        except Exception as e:
            return {"status": "error", "node": node_name, "error": str(e)}
        
        return {"status": "offline", "node": node_name}
    
    def should_migrate(self) -> bool:
        """Check if orchestrator should migrate to Sloth"""
        if self.current_node == self.preferred_host:
            return False
        
        # Check if Sloth is available
        sloth_health = self.check_node_health("sloth")
        return sloth_health["status"] == "online"
    
    def migrate_to_sloth(self):
        """Migrate orchestrator process to Sloth"""
        print(f"🔄 Migrating orchestrator: {self.current_node} → sloth")
        
        sloth = NODES["sloth"]
        
        # Copy orchestrator to Sloth
        try:
            subprocess.run([
                "scp", __file__, 
                f"{sloth['ssh_user']}@{sloth['host']}:~/queztl-core/backend/"
            ], check=True)
            
            # Start on Sloth
            subprocess.run([
                "ssh", f"{sloth['ssh_user']}@{sloth['host']}",
                "cd ~/queztl-core && nohup python3 backend/orchestrator.py > logs/orchestrator.log 2>&1 &"
            ], check=True)
            
            print("✅ Orchestrator migrated to Sloth")
            print("🛑 Shutting down local instance...")
            exit(0)
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
    
    def assign_task(self, task_type: str, task_data: Dict) -> str:
        """Assign task to best available node"""
        
        # Determine best node for task type
        target_node = None
        
        if task_type in ["builder", "creator", "storage", "orchestrator"]:
            # Prefer Sloth for these
            if self.check_node_health("sloth")["status"] == "online":
                target_node = "sloth"
            else:
                target_node = "beast"
        
        elif task_type in ["coder", "generator", "trainer"]:
            # Prefer Beast for compute
            if self.check_node_health("beast")["status"] == "online":
                target_node = "beast"
            else:
                target_node = "sloth"
        
        if not target_node:
            print("❌ No nodes available")
            return "failed"
        
        # Send neurotransmitter signal
        signal = Neurotransmitter(self.current_node or "unknown", task_type)
        success = signal.send(target_node, task_data)
        
        if success:
            print(f"✅ Task assigned: {task_type} → {target_node}")
            return target_node
        else:
            return "failed"
    
    def builder_task(self, target: str, setup_type: str):
        """Builder: Setup infrastructure on target node"""
        task_data = {
            "action": "setup_environment",
            "setup_type": setup_type,
            "timestamp": datetime.now().isoformat()
        }
        
        return self.assign_task("builder", task_data)
    
    def creator_task(self, research_topic: str):
        """Creator: Research and design"""
        task_data = {
            "action": "research_and_design",
            "topic": research_topic,
            "can_morph_to": "coder",  # Can hand off to coder
            "timestamp": datetime.now().isoformat()
        }
        
        return self.assign_task("creator", task_data)
    
    def status_report(self):
        """Generate cluster status report"""
        print("\n" + "="*70)
        print("🧠 QUEZTL ORCHESTRATOR - CLUSTER STATUS")
        print("="*70)
        print(f"Current Host: {self.current_node or 'unknown'}")
        print(f"Preferred Host: {self.preferred_host}")
        print()
        
        for node_name in NODES.keys():
            health = self.check_node_health(node_name)
            node_info = NODES[node_name]
            
            status_emoji = "✅" if health["status"] == "online" else "❌"
            print(f"{status_emoji} {node_name.upper()} ({node_info.get('host')})")
            print(f"   Role: {node_info['role']}")
            print(f"   Status: {health['status']}")
            if health.get('disk_usage'):
                print(f"   Disk: {health['disk_usage']}")
            print(f"   Preferred Tasks: {', '.join(node_info['preferred_tasks'])}")
            print()
        
        print("="*70)
    
    def run(self):
        """Main orchestrator loop"""
        print(f"🚀 Orchestrator starting on {self.current_node}...")
        
        # Check if should migrate to Sloth
        if self.should_migrate():
            self.migrate_to_sloth()
        
        # Main status loop
        self.status_report()
        
        print("\n💡 Orchestrator ready for task assignment")
        print("   Use: orchestrator.assign_task(task_type, task_data)")

def main():
    orchestrator = Orchestrator()
    orchestrator.run()
    
    # Example: Setup builder on Sloth
    print("\n📋 Example: Deploying builder to Sloth...")
    result = orchestrator.builder_task("sloth", "trash_cleaner")
    
    # Example: Research task
    print("\n📋 Example: Assigning creator research task...")
    result = orchestrator.creator_task("AI training on communist theory")

if __name__ == "__main__":
    main()
