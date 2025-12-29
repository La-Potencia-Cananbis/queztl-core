#!/usr/bin/env python3
"""
🚀 QuetzalCore Auto-Scaling Infrastructure
Automatically scale nodes, GPUs, and resources when needed!
NO MORE OVERSUBSCRIPTION - WE SCALE UP!
"""

import asyncio
from datetime import datetime
from typing import Dict, List


class AutoScaler:
    """Intelligent auto-scaling for QuetzalCore infrastructure"""
    
    def __init__(self):
        self.nodes = []
        self.gpus = []
        self.vms = []
        self.node_count = 0
        self.gpu_count = 0
        
        # Scaling policies
        self.max_gpu_utilization = 80  # Scale at 80%
        self.max_memory_utilization = 85  # Scale at 85%
        self.max_cpu_utilization = 80  # Scale at 80%
        
    async def add_compute_node(self, name=None):
        """Add a new compute node to the cluster"""
        node_id = f"node-{self.node_count}"
        self.node_count += 1
        
        node = {
            'id': node_id,
            'name': name or f"compute-{self.node_count}",
            'memory_gb': 64,
            'vcpus': 32,
            'gpus': 2,  # Each node gets 2 GPUs
            'status': 'provisioning',
            'vms': [],
            'created': datetime.now().isoformat(),
        }
        
        print(f"\n🔨 Provisioning new compute node: {node['name']}")
        print(f"   ID: {node_id}")
        print(f"   Memory: {node['memory_gb']} GB")
        print(f"   vCPUs: {node['vcpus']}")
        print(f"   GPUs: {node['gpus']}x (GTX 1080 class)")
        
        # Simulate provisioning
        steps = [
            "Allocating hardware resources",
            "Installing QuetzalCore OS",
            "Configuring memory optimizer",
            "Setting up vGPU manager",
            "Joining cluster",
            "Ready for workloads",
        ]
        
        for step in steps:
            print(f"   ⏳ {step}...", end="", flush=True)
            await asyncio.sleep(0.3)
            print(" ✅")
        
        node['status'] = 'ready'
        self.nodes.append(node)
        
        # Add GPUs to pool
        for i in range(node['gpus']):
            gpu_id = f"{node_id}-gpu{i}"
            self.gpus.append({
                'id': gpu_id,
                'node': node_id,
                'memory_gb': 8,
                'cuda_cores': 2560,
                'utilization': 0,
                'vgpus': [],
            })
            self.gpu_count += 1
        
        print(f"   🎉 Node {node['name']} is READY! (+{node['gpus']} GPUs)")
        
        return node
    
    async def scale_for_vms(self, vm_requests):
        """Auto-scale infrastructure based on VM requirements"""
        print(f"\n{'='*70}")
        print(f"🧮 Analyzing VM Requirements")
        print(f"{'='*70}")
        
        # Calculate total requirements
        total_memory = sum(vm['memory_mb'] for vm in vm_requests) / 1024  # GB
        total_vcpus = sum(vm['vcpus'] for vm in vm_requests)
        total_vgpu_memory = sum(vm['vgpu_memory_mb'] for vm in vm_requests) / 1024  # GB
        
        print(f"\n📊 Total Requirements:")
        print(f"   Memory: {total_memory:.1f} GB")
        print(f"   vCPUs: {total_vcpus}")
        print(f"   vGPU Memory: {total_vgpu_memory:.1f} GB")
        print(f"   VMs: {len(vm_requests)}")
        
        # Calculate nodes needed
        nodes_for_memory = int(total_memory / (64 * 0.8)) + 1  # 80% utilization
        nodes_for_cpu = int(total_vcpus / (32 * 0.8)) + 1
        nodes_for_gpu = int(total_vgpu_memory / (16 * 0.8)) + 1  # 2 GPUs per node
        
        nodes_needed = max(nodes_for_memory, nodes_for_cpu, nodes_for_gpu)
        
        print(f"\n🎯 Scaling Decision:")
        print(f"   Current nodes: {len(self.nodes)}")
        print(f"   Nodes needed: {nodes_needed}")
        print(f"   Will provision: {nodes_needed} nodes")
        
        # Provision nodes in parallel
        print(f"\n🚀 Provisioning {nodes_needed} compute nodes in parallel...")
        
        tasks = [
            self.add_compute_node(f"compute-{i+1}")
            for i in range(nodes_needed)
        ]
        
        await asyncio.gather(*tasks)
        
        print(f"\n{'='*70}")
        print(f"✅ Infrastructure scaled successfully!")
        print(f"{'='*70}")
        
        return self.nodes
    
    async def create_vm_on_cluster(self, vm_config):
        """Create VM with intelligent placement"""
        # Find best node
        best_node = None
        best_score = -1
        
        for node in self.nodes:
            if node['status'] != 'ready':
                continue
            
            # Calculate available resources
            used_memory = sum(vm['memory_mb'] for vm in node['vms']) / 1024
            used_vcpus = sum(vm['vcpus'] for vm in node['vms'])
            
            available_memory = node['memory_gb'] - used_memory
            available_vcpus = node['vcpus'] - used_vcpus
            
            # Check if node can fit VM
            if (available_memory >= vm_config['memory_mb'] / 1024 and
                available_vcpus >= vm_config['vcpus']):
                
                # Score based on resource utilization
                memory_util = used_memory / node['memory_gb']
                cpu_util = used_vcpus / node['vcpus']
                score = 100 - (memory_util + cpu_util) * 50  # Prefer less utilized nodes
                
                if score > best_score:
                    best_score = score
                    best_node = node
        
        if not best_node:
            print(f"⚠️  No suitable node found for {vm_config['name']}")
            return None
        
        # Find available GPU
        available_gpu = None
        for gpu in self.gpus:
            if gpu['node'] == best_node['id']:
                used_gpu_memory = sum(vgpu['memory_mb'] for vgpu in gpu['vgpus'])
                if used_gpu_memory + vm_config['vgpu_memory_mb'] <= gpu['memory_gb'] * 1024:
                    available_gpu = gpu
                    break
        
        if not available_gpu:
            print(f"⚠️  No GPU capacity on {best_node['name']} for {vm_config['name']}")
            return None
        
        # Create VM
        vm_id = f"vm-{len(self.vms)}"
        vm = {
            'id': vm_id,
            'name': vm_config['name'],
            'node': best_node['id'],
            'memory_mb': vm_config['memory_mb'],
            'vcpus': vm_config['vcpus'],
            'vgpu_memory_mb': vm_config['vgpu_memory_mb'],
            'gpu': available_gpu['id'],
            'status': 'running',
            'created': datetime.now().isoformat(),
        }
        
        # Update tracking
        best_node['vms'].append(vm)
        available_gpu['vgpus'].append({
            'vm_id': vm_id,
            'memory_mb': vm_config['vgpu_memory_mb'],
        })
        available_gpu['utilization'] = sum(vgpu['memory_mb'] for vgpu in available_gpu['vgpus']) / (available_gpu['memory_gb'] * 1024) * 100
        self.vms.append(vm)
        
        print(f"\n✅ Created {vm['name']}")
        print(f"   VM ID: {vm_id}")
        print(f"   Node: {best_node['name']}")
        print(f"   GPU: {available_gpu['id']} ({available_gpu['utilization']:.1f}% utilized)")
        
        return vm
    
    def show_cluster_status(self):
        """Display complete cluster status"""
        print(f"\n{'='*70}")
        print(f"🏗️  QuetzalCore Cluster Status")
        print(f"{'='*70}")
        
        print(f"\n📊 Infrastructure:")
        print(f"   Compute Nodes: {len(self.nodes)}")
        print(f"   Total GPUs: {self.gpu_count}")
        print(f"   Running VMs: {len(self.vms)}")
        
        # Calculate totals
        total_memory = sum(node['memory_gb'] for node in self.nodes)
        total_vcpus = sum(node['vcpus'] for node in self.nodes)
        used_memory = sum(vm['memory_mb'] for vm in self.vms) / 1024
        used_vcpus = sum(vm['vcpus'] for vm in self.vms)
        
        print(f"\n💾 Resources:")
        print(f"   Total Memory: {total_memory} GB")
        print(f"   Used Memory: {used_memory:.1f} GB ({used_memory/total_memory*100:.1f}%)")
        print(f"   Total vCPUs: {total_vcpus}")
        print(f"   Used vCPUs: {used_vcpus} ({used_vcpus/total_vcpus*100:.1f}%)")
        
        print(f"\n🎮 GPU Pool:")
        for gpu in self.gpus:
            print(f"   {gpu['id']}: {gpu['utilization']:.1f}% utilized ({len(gpu['vgpus'])} vGPUs)")
        
        print(f"\n🖥️  Nodes:")
        for node in self.nodes:
            used_mem = sum(vm['memory_mb'] for vm in node['vms']) / 1024
            used_cpu = sum(vm['vcpus'] for vm in node['vms'])
            print(f"\n   📦 {node['name']} ({node['id']})")
            print(f"      Memory: {used_mem:.1f}/{node['memory_gb']} GB ({used_mem/node['memory_gb']*100:.1f}%)")
            print(f"      vCPUs: {used_cpu}/{node['vcpus']} ({used_cpu/node['vcpus']*100:.1f}%)")
            print(f"      VMs: {len(node['vms'])}")
        
        print(f"\n{'='*70}")
        print(f"✅ NO OVERSUBSCRIPTION - Perfect scaling! 🚀")
        print(f"{'='*70}\n")


async def main():
    print(f"\n{'='*70}")
    print(f"🦅 QuetzalCore Auto-Scaling Infrastructure")
    print(f"{'='*70}")
    print(f"Intelligent resource management - NO oversubscription!")
    print()
    
    scaler = AutoScaler()
    
    # Define VM requests (same as before)
    vm_requests = [
        {"name": "web-server", "memory_mb": 2048, "vcpus": 2, "vgpu_memory_mb": 1024},
        {"name": "dev-machine", "memory_mb": 4096, "vcpus": 4, "vgpu_memory_mb": 2048},
        {"name": "gaming-rig", "memory_mb": 8192, "vcpus": 4, "vgpu_memory_mb": 4096},
        {"name": "ml-trainer", "memory_mb": 8192, "vcpus": 8, "vgpu_memory_mb": 4096},
    ]
    
    # Auto-scale infrastructure
    await scaler.scale_for_vms(vm_requests)
    
    # Create VMs with intelligent placement
    print(f"\n{'='*70}")
    print(f"🚀 Creating VMs with intelligent placement...")
    print(f"{'='*70}")
    
    for vm_config in vm_requests:
        await scaler.create_vm_on_cluster(vm_config)
        await asyncio.sleep(0.2)
    
    # Show final status
    scaler.show_cluster_status()
    
    print(f"\n🎉 All VMs running on properly scaled infrastructure!")
    print(f"🚗💨 Drive safe - the cluster handles everything!\n")


if __name__ == "__main__":
    asyncio.run(main())
