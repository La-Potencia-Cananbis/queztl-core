#!/usr/bin/env python3
"""
🚀 QUETZALCORE COMPLETE LAUNCH SYSTEM

Launches the full stack:
- 🧠 Positronic Brain
- 🎛️  Master Hypervisor
- 🐧 Linux JIT Instance
- 📊 Real-time Monitoring Dashboard
- 🔧 Tools & Architecture Interface

This gives you a complete window into the QuetzalCore ecosystem.
"""

import asyncio
import sys
import time
import os
from typing import Dict, List
import subprocess

sys.path.insert(0, '/Users/xavasena/hive')

# Import QuetzalCore components
from backend.quetzalcore_brain import QuetzalCoreBrain, BrainControlledHypervisor
from backend.hypervisor.core import QuetzalCoreHypervisor, VMState


class QuetzalCoreMonitoringDashboard:
    """
    Real-time monitoring dashboard for QuetzalCore
    """
    
    def __init__(self):
        self.refresh_interval = 2  # seconds
        self.running = True
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def format_bytes(self, bytes_val: int) -> str:
        """Format bytes to human-readable"""
        val = float(bytes_val)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if val < 1024:
                return f"{val:.1f}{unit}"
            val /= 1024
        return f"{val:.1f}TB"
    
    def format_uptime(self, seconds: float) -> str:
        """Format uptime"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            return f"{seconds/60:.0f}m"
        elif seconds < 86400:
            return f"{seconds/3600:.1f}h"
        else:
            return f"{seconds/86400:.1f}d"
    
    def draw_box(self, title: str, content: List[str], width: int = 70):
        """Draw a box with content"""
        print("┌" + "─" * (width - 2) + "┐")
        # Title
        padding = (width - len(title) - 4) // 2
        print(f"│ {' ' * padding}{title}{' ' * (width - len(title) - padding - 4)} │")
        print("├" + "─" * (width - 2) + "┤")
        
        # Content
        for line in content:
            # Truncate or pad
            if len(line) > width - 4:
                line = line[:width - 7] + "..."
            print(f"│ {line:<{width-4}} │")
        
        print("└" + "─" * (width - 2) + "┘")
    
    def draw_progress_bar(self, percentage: float, width: int = 30) -> str:
        """Draw a progress bar"""
        filled = int(width * percentage / 100)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {percentage:.1f}%"
    
    async def render(
        self,
        brain: QuetzalCoreBrain,
        hypervisor: QuetzalCoreHypervisor,
        linux_vm_id: str = ""
    ):
        """Render the dashboard"""
        
        while self.running:
            self.clear_screen()
            
            # Header
            print("=" * 70)
            print(" " * 15 + "🧠 QUETZALCORE COMMAND CENTER 🦅")
            print("=" * 70)
            print()
            
            # Brain Status
            brain_status = brain.get_brain_status()
            brain_content = [
                f"🆔 Brain ID: {brain_status['brain_id']}",
                f"⏱️  Uptime: {self.format_uptime(brain_status['uptime_seconds'])}",
                f"🤖 Mode: {'AUTONOMOUS' if brain_status['autonomous_mode'] else 'MANUAL'}",
                f"🎓 Learning Rate: {brain_status['learning_rate']}",
                "",
                "📊 METRICS:",
                f"  ✅ Tasks Completed: {brain_status['metrics']['tasks_completed']}",
                f"  🎯 Decisions Made: {brain_status['metrics']['decisions_made']}",
                f"  ⚡ Optimizations: {brain_status['metrics']['optimizations_applied']}",
                f"  🧬 Learning Cycles: {brain_status['metrics']['learning_cycles']}",
                "",
                f"💾 Experiences: {brain_status['experiences_stored']} stored",
                f"📚 Knowledge Domains: {brain_status['knowledge_domains']}",
            ]
            self.draw_box("🧠 POSITRONIC BRAIN STATUS", brain_content)
            print()
            
            # Hypervisor Status
            hv_stats = hypervisor.get_stats()
            cpu_usage = (hv_stats['resources']['vcpus_allocated'] / 
                        max(hv_stats['resources']['vcpus_total'], 1)) * 100
            mem_usage = (hv_stats['resources']['memory_allocated_mb'] / 
                        max(hv_stats['resources']['memory_total_mb'], 1)) * 100
            
            hv_content = [
                f"🖥️  VMs: {hv_stats['vms']['total']} total | "
                f"▶️  {hv_stats['vms']['running']} running | "
                f"⏸️  {hv_stats['vms']['stopped']} stopped",
                "",
                "💻 CPU ALLOCATION:",
                f"  {self.draw_progress_bar(cpu_usage)}",
                f"  {hv_stats['resources']['vcpus_allocated']}/{hv_stats['resources']['vcpus_total']} vCPUs allocated",
                "",
                "💾 MEMORY ALLOCATION:",
                f"  {self.draw_progress_bar(mem_usage)}",
                f"  {hv_stats['resources']['memory_allocated_mb']}/{hv_stats['resources']['memory_total_mb']} MB allocated",
                "",
                f"🌐 Nodes: {hv_stats['nodes']['total']} | "
                f"{'Distributed' if hv_stats['nodes']['distributed_mode'] else 'Local'} Mode",
            ]
            self.draw_box("🎛️  MASTER HYPERVISOR STATUS", hv_content)
            print()
            
            # Linux JIT Instance
            if linux_vm_id and linux_vm_id in hypervisor.vms:
                vm = hypervisor.vms[linux_vm_id]
                vm_uptime = time.time() - vm.started_at if vm.state == VMState.RUNNING else 0
                
                linux_content = [
                    f"🆔 VM ID: {vm.vm_id}",
                    f"📛 Name: {vm.name}",
                    f"⚡ State: {vm.state.value.upper()}",
                    f"⏱️  Uptime: {self.format_uptime(vm_uptime)}",
                    "",
                    "🔧 RESOURCES:",
                    f"  CPU: {vm.vcpu_count} vCPUs",
                    f"  Memory: {vm.memory_mb} MB",
                    f"  GPU: {vm.vgpu_count} vGPUs",
                    "",
                    "🐧 CONSOLE OUTPUT (last 5 lines):",
                ]
                
                # Add console output
                for line in vm.console_output[-5:]:
                    if line:
                        linux_content.append(f"  {line}")
                
                self.draw_box("🐧 LINUX JIT INSTANCE", linux_content)
            else:
                linux_content = [
                    "⚠️  No Linux JIT instance running",
                    "",
                    "Press 'L' to launch a new Linux instance"
                ]
                self.draw_box("🐧 LINUX JIT INSTANCE", linux_content)
            
            print()
            
            # Running VMs
            vms = hypervisor.list_vms()
            if vms:
                vm_list_content = []
                for vm_info in vms[:5]:  # Show max 5
                    state_icon = "▶️ " if vm_info['state'] == 'running' else "⏸️ "
                    vm_list_content.append(
                        f"{state_icon} {vm_info['name']:<20} | "
                        f"CPU:{vm_info['vcpus']} | "
                        f"RAM:{vm_info['memory_mb']}MB | "
                        f"⏱️ {self.format_uptime(vm_info['uptime'])}"
                    )
                
                if len(vms) > 5:
                    vm_list_content.append(f"... and {len(vms) - 5} more")
                
                self.draw_box("📋 ACTIVE VIRTUAL MACHINES", vm_list_content)
            
            print()
            
            # Footer
            print("=" * 70)
            print("Commands: [L]aunch Linux | [S]top VM | [R]efresh | [Q]uit")
            print("=" * 70)
            
            await asyncio.sleep(self.refresh_interval)


class QuetzalCoreCompleteSystem:
    """
    Complete QuetzalCore system with all components
    """
    
    def __init__(self):
        print("\n" + "=" * 70)
        print(" " * 10 + "🚀 INITIALIZING QUETZALCORE COMPLETE SYSTEM")
        print("=" * 70 + "\n")
        
        # Initialize brain-controlled hypervisor
        print("🧠 Initializing Positronic Brain...")
        self.system = BrainControlledHypervisor()
        
        # Register local resources
        print("📡 Registering QuetzalCore nodes...")
        self.system.hypervisor.register_node(
            "local-node",
            vcpus=16,
            memory_mb=32768  # 32GB
        )
        
        # Monitoring dashboard
        self.dashboard = QuetzalCoreMonitoringDashboard()
        
        # Track Linux JIT instance
        self.linux_vm_id = None
        
        print("\n✅ System initialization complete!\n")
    
    async def launch_linux_jit_instance(self) -> str:
        """
        Launch a Linux JIT (Just-In-Time) instance
        """
        
        print("\n🐧 Launching Linux JIT instance...")
        
        # Let the brain analyze and decide
        result = await self.system.request_compute(
            "Launch interactive Linux instance for monitoring and tool access",
            {
                'type': 'linux_jit',
                'purpose': 'monitoring',
                'interactive': True
            }
        )
        
        vm_id = result['vm_id']
        self.linux_vm_id = vm_id
        
        # Get the VM
        vm = self.system.hypervisor.vms[vm_id]
        
        # Add welcome messages to console
        vm.console_output.extend([
            "",
            "Welcome to QuetzalCore Linux JIT Instance",
            "════════════════════════════════════════",
            f"Kernel: Linux 6.1.0-quetzalcore",
            f"Memory: {vm.memory_mb}MB",
            f"CPUs: {vm.vcpu_count}",
            "",
            "Available QuetzalCore Tools:",
            "  • quetzalcore-brain    - Brain interface",
            "  • quetzalcore-monitor  - System monitoring",
            "  • quetzalcore-deploy   - Deployment tools",
            "  • quetzalcore-mining   - Mining analysis",
            "  • quetzalcore-3d       - 3D generation",
            "",
            "Type 'help' for command list",
            "root@quetzalcore:~# _"
        ])
        
        print(f"✅ Linux JIT instance ready: {vm_id}")
        
        return vm_id
    
    async def run(self):
        """
        Run the complete system
        """
        
        print("\n" + "=" * 70)
        print(" " * 15 + "🦅 QUETZALCORE SYSTEM ONLINE")
        print("=" * 70 + "\n")
        
        # Launch Linux JIT instance
        await self.launch_linux_jit_instance()
        
        # Start brain thinking loop in background
        asyncio.create_task(self.system.brain.autonomous_thinking_loop())
        
        # Let brain learn from the Linux launch
        await self.system.complete_task(
            'linux-jit-launch',
            {'status': 'running', 'vm_id': self.linux_vm_id},
            success=True
        )
        
        # Launch a few demo tasks so brain has knowledge
        await self._run_demo_tasks()
        
        # Start monitoring dashboard
        print("\n🎯 Starting real-time monitoring dashboard...")
        print("   (Press Ctrl+C to stop)\n")
        
        await asyncio.sleep(2)
        
        try:
            await self.dashboard.render(
                self.system.brain,
                self.system.hypervisor,
                self.linux_vm_id
            )
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down gracefully...")
            await self.shutdown()
    
    async def _run_demo_tasks(self):
        """Run some demo tasks to populate brain knowledge"""
        
        print("\n🎓 Running demo tasks to teach the brain...\n")
        
        # Task 1: Mining
        print("  📋 Task 1: Mining MAG processing")
        task1 = await self.system.request_compute(
            "Process mining MAG survey",
            {'survey_id': 'DEMO-001', 'points': 5000}
        )
        await asyncio.sleep(1)
        await self.system.complete_task('task-1', {'anomalies': 3}, success=True)
        
        # Task 2: 3D Generation
        print("  📋 Task 2: 3D model generation")
        task2 = await self.system.request_compute(
            "Generate 3D model",
            {'points': 10000, 'quality': 'medium'}
        )
        await asyncio.sleep(1)
        await self.system.complete_task('task-2', {'model_id': 'demo-3d'}, success=True)
        
        # Task 3: ML Training
        print("  📋 Task 3: ML training")
        task3 = await self.system.request_compute(
            "Train anomaly detection model",
            {'epochs': 50}
        )
        await asyncio.sleep(1)
        await self.system.complete_task('task-3', {'accuracy': 0.93}, success=True)
        
        print("\n✅ Brain trained on demo tasks\n")
    
    async def shutdown(self):
        """Graceful shutdown"""
        
        # Stop all VMs
        for vm_id in list(self.system.hypervisor.vms.keys()):
            try:
                await self.system.hypervisor.stop_vm(vm_id)
            except:
                pass
        
        # Stop brain
        self.system.brain.autonomous_mode = False
        
        print("✅ QuetzalCore system shut down")
        print("\n🦅 Hasta luego!\n")


async def main():
    """
    Main entry point
    """
    
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                                                                   ║")
    print("║              🧠 QUETZALCORE COMPLETE LAUNCH SYSTEM 🦅                  ║")
    print("║                                                                   ║")
    print("║  Positronic Brain + Master Hypervisor + Linux JIT Instance       ║")
    print("║                                                                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print()
    
    # Create and run complete system
    system = QuetzalCoreCompleteSystem()
    
    try:
        await system.run()
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user")
        await system.shutdown()
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        await system.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
