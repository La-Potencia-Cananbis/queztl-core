#!/usr/bin/env python3
"""
🦅 QuetzalCore Infrastructure Monitor
Real-time OS utilization across distributed infrastructure
Like Activity Monitor but for your entire cluster!
"""

import asyncio
import time
import psutil
import json
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass, asdict
import curses


@dataclass
class SystemMetrics:
    """Real-time system metrics"""
    timestamp: str
    cpu_percent: float
    cpu_count: int
    memory_percent: float
    memory_gb: float
    memory_available_gb: float
    disk_percent: float
    disk_gb: float
    disk_available_gb: float
    processes_count: int
    threads_count: int
    boot_time: str
    uptime_hours: float


@dataclass
class ProcessMetrics:
    """Per-process metrics"""
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    memory_mb: float
    status: str
    num_threads: int


class InfrastructureMonitor:
    """Monitor OS utilization across infrastructure"""
    
    def __init__(self):
        self.metrics_history = []
        self.top_processes = []
        self.start_time = time.time()
        
    def get_system_metrics(self) -> SystemMetrics:
        """Collect system-wide metrics"""
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        boot_time = psutil.boot_time()
        uptime = (time.time() - boot_time) / 3600
        
        return SystemMetrics(
            timestamp=datetime.now().isoformat(),
            cpu_percent=cpu,
            cpu_count=psutil.cpu_count(),
            memory_percent=memory.percent,
            memory_gb=memory.total / (1024**3),
            memory_available_gb=memory.available / (1024**3),
            disk_percent=disk.percent,
            disk_gb=disk.total / (1024**3),
            disk_available_gb=disk.free / (1024**3),
            processes_count=len(psutil.pids()),
            threads_count=threading_count(),
            boot_time=datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S'),
            uptime_hours=uptime
        )
    
    def get_top_processes(self, count: int = 10) -> List[ProcessMetrics]:
        """Get top processes by CPU+Memory usage"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                proc_info = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'num_threads'])
                memory_mb = psutil.Process(proc.pid).memory_info().rss / (1024**2)
                
                processes.append(ProcessMetrics(
                    pid=proc_info['pid'],
                    name=proc_info['name'][:40],  # Truncate long names
                    cpu_percent=proc_info['cpu_percent'] or 0,
                    memory_percent=proc_info['memory_percent'] or 0,
                    memory_mb=memory_mb,
                    status=proc_info['status'],
                    num_threads=proc_info['num_threads'] or 1
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by combined CPU + Memory score
        processes.sort(key=lambda p: (p.cpu_percent + p.memory_percent), reverse=True)
        return processes[:count]
    
    def print_dashboard(self):
        """Print formatted dashboard"""
        metrics = self.get_system_metrics()
        top_procs = self.get_top_processes(15)
        
        print("\033[2J\033[H")  # Clear screen
        print("=" * 100)
        print("🦅 QuetzalCore Infrastructure Monitor - Real-time OS Utilization")
        print("=" * 100)
        
        # System Status Section
        print("\n📊 SYSTEM STATUS")
        print("-" * 100)
        
        # CPU metrics
        cpu_bar = self._draw_bar(metrics.cpu_percent, 100)
        print(f"CPU:       {metrics.cpu_percent:6.1f}% {cpu_bar} ({metrics.cpu_count} cores)")
        
        # Memory metrics
        memory_used = metrics.memory_gb - metrics.memory_available_gb
        memory_bar = self._draw_bar(metrics.memory_percent, 100)
        print(f"Memory:    {metrics.memory_percent:6.1f}% {memory_bar} ({memory_used:.1f}GB / {metrics.memory_gb:.1f}GB)")
        
        # Disk metrics
        disk_bar = self._draw_bar(metrics.disk_percent, 100)
        disk_used = metrics.disk_gb - metrics.disk_available_gb
        print(f"Disk:      {metrics.disk_percent:6.1f}% {disk_bar} ({disk_used:.1f}GB / {metrics.disk_gb:.1f}GB)")
        
        print(f"\n📈 SYSTEM INFO")
        print("-" * 100)
        print(f"Uptime:              {metrics.uptime_hours:.1f} hours (since {metrics.boot_time})")
        print(f"Processes:           {metrics.processes_count} running")
        print(f"Threads:             {metrics.threads_count} active")
        
        # Top Processes Section
        print(f"\n🔝 TOP 15 PROCESSES")
        print("-" * 100)
        print(f"{'PID':<8} {'CPU%':<8} {'MEM%':<8} {'Memory':<12} {'Threads':<8} {'Status':<10} {'Process Name':<40}")
        print("-" * 100)
        
        for proc in top_procs:
            if proc.cpu_percent > 0.1 or proc.memory_percent > 0.1:
                print(f"{proc.pid:<8} {proc.cpu_percent:<8.1f} {proc.memory_percent:<8.1f} "
                      f"{proc.memory_mb:<12.0f}MB {proc.num_threads:<8} {proc.status:<10} {proc.name:<40}")
        
        # Node Resource Utilization
        print(f"\n🖥️  DISTRIBUTED INFRASTRUCTURE SIMULATION")
        print("-" * 100)
        
        # Simulate 3 nodes in cluster
        nodes = self._simulate_cluster_nodes(metrics)
        for node in nodes:
            print(f"\nNode: {node['name']}")
            print(f"  CPU:    {node['cpu']:6.1f}% " + self._draw_bar(node['cpu'], 100))
            print(f"  Memory: {node['memory']:6.1f}% " + self._draw_bar(node['memory'], 100))
            print(f"  Disk:   {node['disk']:6.1f}% " + self._draw_bar(node['disk'], 100))
            print(f"  VMs:    {node['vms']} running | GPUs: {node['gpus']} utilized")
        
        # Cluster Overview
        avg_cpu = sum(n['cpu'] for n in nodes) / len(nodes)
        avg_mem = sum(n['memory'] for n in nodes) / len(nodes)
        avg_disk = sum(n['disk'] for n in nodes) / len(nodes)
        
        print(f"\n📊 CLUSTER AVERAGES")
        print("-" * 100)
        print(f"CPU:    {avg_cpu:6.1f}% " + self._draw_bar(avg_cpu, 100))
        print(f"Memory: {avg_mem:6.1f}% " + self._draw_bar(avg_mem, 100))
        print(f"Disk:   {avg_disk:6.1f}% " + self._draw_bar(avg_disk, 100))
        
        # Footer
        print("\n" + "=" * 100)
        print(f"Last updated: {metrics.timestamp} | Press Ctrl+C to exit | Refreshing every 2 seconds...")
        print("=" * 100 + "\n")
    
    def _draw_bar(self, percent: float, max_val: float = 100, width: int = 30) -> str:
        """Draw a colored progress bar"""
        filled = int(percent / max_val * width)
        
        # Color based on utilization
        if percent < 50:
            color = "\033[92m"  # Green
        elif percent < 75:
            color = "\033[93m"  # Yellow
        else:
            color = "\033[91m"  # Red
        
        reset = "\033[0m"
        bar = "█" * filled + "░" * (width - filled)
        return f"{color}{bar}{reset}"
    
    def _simulate_cluster_nodes(self, metrics: SystemMetrics) -> List[Dict]:
        """Simulate distributed cluster nodes"""
        # In a real scenario, these would come from actual cluster nodes
        # For now, we simulate them based on local metrics
        
        base_cpu = metrics.cpu_percent
        base_mem = metrics.memory_percent
        base_disk = metrics.disk_percent
        
        nodes = [
            {
                "name": "compute-node-1",
                "cpu": min(100, base_cpu + 10),
                "memory": min(100, base_mem + 5),
                "disk": min(100, base_disk),
                "vms": 3,
                "gpus": 2,
            },
            {
                "name": "compute-node-2",
                "cpu": min(100, base_cpu - 5),
                "memory": min(100, base_mem - 10),
                "disk": min(100, base_disk),
                "vms": 2,
                "gpus": 1,
            },
            {
                "name": "compute-node-3",
                "cpu": min(100, base_cpu + 5),
                "memory": min(100, base_mem + 15),
                "disk": min(100, base_disk + 5),
                "vms": 4,
                "gpus": 2,
            },
        ]
        
        return nodes
    
    def export_metrics(self, filename: str = None):
        """Export metrics to JSON"""
        if not filename:
            filename = f"infrastructure_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        metrics = self.get_system_metrics()
        top_procs = self.get_top_processes()
        
        data = {
            "system": asdict(metrics),
            "top_processes": [asdict(p) for p in top_procs],
            "exported_at": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Metrics exported to: {filename}")
        return filename
    
    async def run_continuous_monitor(self, refresh_interval: int = 2):
        """Run continuous monitoring"""
        try:
            while True:
                self.print_dashboard()
                await asyncio.sleep(refresh_interval)
        except KeyboardInterrupt:
            print("\n\n🛑 Monitor stopped")
            self.export_metrics()


def threading_count():
    """Get total thread count"""
    try:
        total = 0
        for proc in psutil.process_iter():
            try:
                total += proc.num_threads()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return total
    except:
        return 0


def main():
    import sys
    
    print("🦅 QuetzalCore Infrastructure Monitor Starting...\n")
    
    monitor = InfrastructureMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--export":
        # One-time export
        print("📊 Collecting metrics...")
        monitor.export_metrics()
        monitor.print_dashboard()
    else:
        # Continuous monitoring
        print("📊 Starting continuous monitoring (Ctrl+C to stop)...\n")
        asyncio.run(monitor.run_continuous_monitor())


if __name__ == "__main__":
    main()
