#!/usr/bin/env python3
"""
Autonomous Distributed Agent - Continuous Execution Monitor

This script will:
1. Deploy distributed agents to the cluster
2. Execute autonomous tasks every 4 minutes
3. Monitor execution status
4. Report results in real-time
"""

import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from distributed_agent_wrapper import DistributedAgent, AgentPool
from queztl_config import config

def log(message):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def run_autonomous_cycle():
    """Execute one autonomous cycle"""
    log("🚀 Starting autonomous cycle...")
    
    try:
        # Create agent pool
        pool = AgentPool()
        
        # Deploy agents
        log("   Deploying agents to Beast...")
        trainer = pool.create_agent("TrainerAgent", node='beast', use_docker=True)
        monitor = pool.create_agent("MonitorAgent", node='beast', use_docker=False)
        
        log(f"   ✅ {len(pool)} agents deployed")
        
        # Check capabilities
        log("   📊 Checking node capabilities...")
        caps = trainer.check_capabilities()
        log(f"      Python: {caps.get('python')}, PyTorch: {caps.get('pytorch')}, CUDA: {caps.get('cuda')}")
        
        # Execute autonomous tasks
        tasks = [
            ("System check", ['uname', '-r']),
            ("Python check", ['python3', '--version']),
            ("Disk usage", ['df', '-h', '/']),
        ]
        
        log("   🎯 Executing autonomous tasks...")
        for task_name, command in tasks:
            result = trainer.execute(command)
            status = "✅" if result.returncode == 0 else "❌"
            output = result.stdout.strip() if result.stdout else result.stderr.strip()
            # Get first line only
            output = output.split('\n')[0] if output else "No output"
            if len(output) > 50:
                output = output[:50] + "..."
            log(f"      {status} {task_name}: {output}")
        
        # Run distributed Python task
        log("   🐍 Running distributed Python task...")
        result = trainer.run_python("""
import time
import socket
print(f"Task started on {socket.gethostname()}")
time.sleep(2)
print("Task completed successfully")
""")
        for line in result.stdout.strip().split('\n'):
            log(f"      → {line}")
        
        # Monitor status
        log("   📈 Checking system status...")
        result = monitor.execute(['uptime'])
        log(f"      Uptime: {result.stdout.strip()}")
        
        log("✅ Cycle complete\n")
        return True
        
    except Exception as e:
        log(f"❌ Error in cycle: {e}\n")
        return False

def main():
    """Main autonomous execution loop"""
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║  Autonomous Distributed Agent - Continuous Monitor            ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    
    log("🤖 Autonomous agent system starting...")
    log(f"   Target: Beast ({config.get_node_ip('beast')})")
    log(f"   Interval: 4 minutes")
    log(f"   Mode: Continuous monitoring")
    print()
    
    cycle_count = 0
    
    try:
        while True:
            cycle_count += 1
            log(f"━━━━━━━━━━━━━━━ CYCLE {cycle_count} ━━━━━━━━━━━━━━━")
            
            success = run_autonomous_cycle()
            
            if success:
                log("⏳ Waiting 4 minutes until next cycle...")
                log(f"   Next cycle at: {datetime.now().strftime('%H:%M:%S')} + 4 min")
            else:
                log("⚠️  Cycle failed, waiting 4 minutes before retry...")
            
            print()
            
            # Wait 4 minutes (240 seconds)
            time.sleep(240)
            
    except KeyboardInterrupt:
        print("\n")
        log("🛑 Autonomous system stopped by user")
        log(f"   Total cycles completed: {cycle_count}")
        print()
        print("╚════════════════════════════════════════════════════════════════╝")

if __name__ == "__main__":
    main()
