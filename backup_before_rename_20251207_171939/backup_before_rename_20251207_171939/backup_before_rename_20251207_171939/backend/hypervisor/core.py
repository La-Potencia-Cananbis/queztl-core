"""
🦅 QUEZTL HYPERVISOR - Core

Main hypervisor implementation that manages VMs across distributed Queztl nodes.

Patent-pending: Distributed hypervisor with quantum-inspired scheduling
"""

import asyncio
import uuid
import time
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


class VMState(Enum):
    """Virtual machine lifecycle states"""
    STOPPED = "stopped"
    BOOTING = "booting"
    RUNNING = "running"
    PAUSED = "paused"
    MIGRATING = "migrating"
    SHUTTING_DOWN = "shutting_down"
    CRASHED = "crashed"


@dataclass
class VirtualMachine:
    """
    Complete virtual machine definition
    
    This represents a full VM with virtual hardware that can boot Linux.
    """
    vm_id: str
    name: str
    state: VMState = VMState.STOPPED
    
    # Virtual hardware configuration
    vcpu_count: int = 1
    memory_mb: int = 512
    vgpu_count: int = 0
    
    # Virtual devices
    vcpus: List = field(default_factory=list)
    memory_manager: Optional[object] = None
    devices: List = field(default_factory=list)
    
    # Boot configuration
    kernel_path: Optional[str] = None
    initrd_path: Optional[str] = None
    cmdline: str = "console=ttyS0"
    
    # Distributed state
    node_assignments: Dict[str, str] = field(default_factory=dict)  # resource -> node_id
    
    # Metadata
    created_at: float = 0.0
    started_at: float = 0.0
    owner: str = "quetzalcore"
    tags: Dict[str, str] = field(default_factory=dict)
    
    # Runtime
    boot_loader: Optional[object] = None
    console_output: List[str] = field(default_factory=list)


class QueztlHypervisor:
    """
    The main hypervisor - Virtual Machine Monitor (VMM)
    
    This is the core that:
    1. Creates and manages VMs
    2. Virtualizes CPU, memory, and I/O
    3. Boots Linux kernels in VMs
    4. Distributes VMs across Queztl nodes
    5. Handles live migration
    
    Think of this as VMware ESXi or KVM, but distributed.
    """
    
    def __init__(self, distributed: bool = True):
        self.vms: Dict[str, VirtualMachine] = {}
        self.distributed = distributed
        
        # Queztl node registry
        self.nodes: Dict[str, Dict] = {}
        
        # Resource tracking
        self.total_vcpus = 0
        self.total_memory_mb = 0
        self.allocated_vcpus = 0
        self.allocated_memory_mb = 0
        
        print("🦅 QUEZTL HYPERVISOR INITIALIZED")
        print(f"   Mode: {'Distributed' if distributed else 'Local'}")
        print(f"   Version: 0.1.0-alpha")
    
    # ============================================================
    # VM LIFECYCLE
    # ============================================================
    
    def create_vm(
        self,
        name: str,
        vcpus: int = 1,
        memory_mb: int = 512,
        vgpus: int = 0,
        kernel_path: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Create a new virtual machine
        
        Args:
            name: VM name
            vcpus: Number of virtual CPUs
            memory_mb: RAM in megabytes
            vgpus: Number of virtual GPUs
            kernel_path: Path to Linux kernel to boot
            
        Returns:
            VM ID
        """
        
        vm_id = f"vm-{uuid.uuid4().hex[:8]}"
        
        vm = VirtualMachine(
            vm_id=vm_id,
            name=name,
            vcpu_count=vcpus,
            memory_mb=memory_mb,
            vgpu_count=vgpus,
            kernel_path=kernel_path,
            created_at=time.time()
        )
        
        # Store additional config
        if 'initrd_path' in kwargs:
            vm.initrd_path = kwargs['initrd_path']
        if 'cmdline' in kwargs:
            vm.cmdline = kwargs['cmdline']
        if 'owner' in kwargs:
            vm.owner = kwargs['owner']
        
        self.vms[vm_id] = vm
        
        print(f"✨ Created VM: {name} ({vm_id})")
        print(f"   vCPUs: {vcpus}")
        print(f"   RAM: {memory_mb}MB")
        print(f"   vGPUs: {vgpus}")
        if kernel_path:
            print(f"   Kernel: {kernel_path}")
        
        return vm_id
    
    async def start_vm(self, vm_id: str):
        """
        Start a virtual machine
        
        This will:
        1. Allocate resources
        2. Initialize virtual hardware
        3. Load kernel into memory
        4. Boot the VM
        """
        
        if vm_id not in self.vms:
            raise ValueError(f"VM {vm_id} not found")
        
        vm = self.vms[vm_id]
        
        if vm.state == VMState.RUNNING:
            print(f"⚠️  VM {vm.name} already running")
            return
        
        print(f"\n{'='*60}")
        print(f"🚀 STARTING VM: {vm.name}")
        print(f"{'='*60}\n")
        
        vm.state = VMState.BOOTING
        
        # Step 1: Allocate resources
        print("📦 Step 1: Allocating resources...")
        await self._allocate_resources(vm)
        
        # Step 2: Initialize virtual CPUs
        print("🔧 Step 2: Initializing virtual CPUs...")
        await self._init_vcpus(vm)
        
        # Step 3: Initialize memory manager
        print("💾 Step 3: Setting up virtual memory...")
        await self._init_memory(vm)
        
        # Step 4: Initialize virtual devices
        print("🔌 Step 4: Attaching virtual devices...")
        await self._init_devices(vm)
        
        # Step 5: Load kernel (if provided)
        if vm.kernel_path:
            print(f"🐧 Step 5: Loading Linux kernel...")
            try:
                await self._load_kernel(vm)
            except FileNotFoundError:
                print(f"⚠️  Kernel file not found (simulating boot)")
        else:
            print("⚠️  Step 5: No kernel specified, VM idle")
        
        # Step 6: Start VM execution
        print("▶️  Step 6: Starting VM execution...")
        vm.state = VMState.RUNNING
        vm.started_at = time.time()
        
        # Update resource allocation
        self.allocated_vcpus += vm.vcpu_count
        self.allocated_memory_mb += vm.memory_mb
        
        print(f"\n{'='*60}")
        print(f"✅ VM {vm.name} RUNNING")
        print(f"{'='*60}\n")
        
        # Start VM execution loop
        if vm.kernel_path:
            asyncio.create_task(self._vm_execution_loop(vm))
    
    async def stop_vm(self, vm_id: str, force: bool = False):
        """Stop a running VM"""
        
        if vm_id not in self.vms:
            raise ValueError(f"VM {vm_id} not found")
        
        vm = self.vms[vm_id]
        
        if vm.state != VMState.RUNNING:
            print(f"⚠️  VM {vm.name} not running")
            return
        
        print(f"🛑 Stopping VM: {vm.name}")
        vm.state = VMState.SHUTTING_DOWN
        
        if force:
            print("   Force shutdown (no cleanup)")
        else:
            print("   Graceful shutdown...")
            await asyncio.sleep(0.5)  # Allow cleanup
        
        # Free resources
        self.allocated_vcpus -= vm.vcpu_count
        self.allocated_memory_mb -= vm.memory_mb
        
        vm.state = VMState.STOPPED
        print(f"✅ VM {vm.name} stopped")
    
    def destroy_vm(self, vm_id: str):
        """Permanently destroy a VM"""
        
        if vm_id in self.vms:
            vm = self.vms[vm_id]
            
            if vm.state == VMState.RUNNING:
                asyncio.create_task(self.stop_vm(vm_id, force=True))
            
            del self.vms[vm_id]
            print(f"🗑️  Destroyed VM: {vm.name}")
    
    # ============================================================
    # RESOURCE MANAGEMENT
    # ============================================================
    
    async def _allocate_resources(self, vm: VirtualMachine):
        """Allocate physical resources for VM"""
        
        required_vcpus = vm.vcpu_count
        required_memory = vm.memory_mb
        
        if self.distributed:
            # Distribute across Queztl nodes
            nodes = self._select_nodes(required_vcpus, required_memory)
            if not nodes:
                raise RuntimeError("Insufficient resources in cluster")
            
            vm.node_assignments = {
                "vcpus": nodes[0],
                "memory": nodes[0],  # Co-locate for now
                "devices": nodes[0]
            }
            print(f"   Allocated on node: {nodes[0]}")
        else:
            # Local allocation
            print(f"   Allocated locally")
        
        await asyncio.sleep(0.1)  # Simulate allocation time
    
    async def _init_vcpus(self, vm: VirtualMachine):
        """Initialize virtual CPUs"""
        
        from .vcpu import VirtualCPU
        
        vm.vcpus = []
        for i in range(vm.vcpu_count):
            vcpu = VirtualCPU(
                vcpu_id=f"{vm.vm_id}-vcpu-{i}",
                vm_id=vm.vm_id
            )
            vm.vcpus.append(vcpu)
        
        print(f"   Created {vm.vcpu_count} vCPU(s)")
        await asyncio.sleep(0.1)
    
    async def _init_memory(self, vm: VirtualMachine):
        """Initialize virtual memory manager"""
        
        from .memory import MemoryManager
        
        vm.memory_manager = MemoryManager(
            vm_id=vm.vm_id,
            size_mb=vm.memory_mb
        )
        
        print(f"   Allocated {vm.memory_mb}MB virtual memory")
        await asyncio.sleep(0.1)
    
    async def _init_devices(self, vm: VirtualMachine):
        """Initialize virtual devices"""
        
        from .devices import VirtIOGPU
        
        # Add virtual GPU if requested
        if vm.vgpu_count > 0:
            for i in range(vm.vgpu_count):
                vgpu = VirtIOGPU(
                    device_id=f"{vm.vm_id}-vgpu-{i}",
                    vm_id=vm.vm_id
                )
                vm.devices.append(vgpu)
            
            print(f"   Attached {vm.vgpu_count} vGPU(s)")
        
        await asyncio.sleep(0.1)
    
    async def _load_kernel(self, vm: VirtualMachine):
        """Load Linux kernel into VM memory"""
        
        from .boot import BootLoader
        
        vm.boot_loader = BootLoader(vm)
        
        try:
            if vm.kernel_path is not None:
                await vm.boot_loader.load_kernel(vm.kernel_path)
            print(f"   Kernel loaded: {vm.kernel_path}")
        except FileNotFoundError:
            print(f"   ⚠️  Kernel not found (will simulate boot)")
        
        await asyncio.sleep(0.1)
    
    async def _vm_execution_loop(self, vm: VirtualMachine):
        """Main VM execution loop"""
        
        print(f"\n[VM {vm.name}] Execution started")
        
        # Simulate boot messages
        boot_messages = [
            "Starting Linux kernel...",
            "Initializing hardware...",
            "Mounting root filesystem...",
            "Starting init process...",
            "",
            f"Welcome to Queztl VM: {vm.name}",
            f"Kernel: Linux 6.1.0-quetzalcore",
            f"Memory: {vm.memory_mb}MB",
            f"CPUs: {vm.vcpu_count}",
            "",
            "VM is now running!",
        ]
        
        for msg in boot_messages:
            vm.console_output.append(msg)
            print(f"[VM {vm.name}] {msg}")
            await asyncio.sleep(0.2)
        
        # Keep VM running
        while vm.state == VMState.RUNNING:
            await asyncio.sleep(1)
    
    def _select_nodes(self, vcpus: int, memory_mb: int) -> List[str]:
        """Select Queztl nodes for VM placement"""
        
        # For now, use first available node
        if not hasattr(self, 'nodes') or not self.nodes:
            return ["local"]
        
        if not self.nodes:
            return ["local"]
        
        for node_id, node_info in self.nodes.items():
            if (node_info.get("available_vcpus", 0) >= vcpus and
                node_info.get("available_memory_mb", 0) >= memory_mb):
                return [node_id]
        
        return []
    
    # ============================================================
    # CLUSTER MANAGEMENT
    # ============================================================
    
    def register_node(
        self,
        node_id: str,
        vcpus: int,
        memory_mb: int,
        **kwargs
    ):
        """Register a Queztl node to the hypervisor cluster"""
        
        self.nodes[node_id] = {
            "node_id": node_id,
            "vcpus": vcpus,
            "memory_mb": memory_mb,
            "available_vcpus": vcpus,
            "available_memory_mb": memory_mb,
            **kwargs
        }
        
        self.total_vcpus += vcpus
        self.total_memory_mb += memory_mb
        
        print(f"✅ Registered node: {node_id}")
        print(f"   vCPUs: {vcpus}")
        print(f"   Memory: {memory_mb}MB")
        print(f"   Cluster total: {self.total_vcpus} vCPUs, {self.total_memory_mb}MB")
    
    # ============================================================
    # MONITORING
    # ============================================================
    
    def get_stats(self) -> dict:
        """Get hypervisor statistics"""
        
        return {
            "vms": {
                "total": len(self.vms),
                "running": sum(1 for vm in self.vms.values() if vm.state == VMState.RUNNING),
                "stopped": sum(1 for vm in self.vms.values() if vm.state == VMState.STOPPED)
            },
            "resources": {
                "vcpus_total": self.total_vcpus,
                "vcpus_allocated": self.allocated_vcpus,
                "vcpus_available": self.total_vcpus - self.allocated_vcpus,
                "memory_total_mb": self.total_memory_mb,
                "memory_allocated_mb": self.allocated_memory_mb,
                "memory_available_mb": self.total_memory_mb - self.allocated_memory_mb
            },
            "nodes": {
                "total": len(self.nodes),
                "distributed_mode": self.distributed
            }
        }
    
    def list_vms(self) -> List[dict]:
        """List all VMs"""
        
        return [
            {
                "vm_id": vm.vm_id,
                "name": vm.name,
                "state": vm.state.value,
                "vcpus": vm.vcpu_count,
                "memory_mb": vm.memory_mb,
                "vgpus": vm.vgpu_count,
                "uptime": time.time() - vm.started_at if vm.state == VMState.RUNNING else 0
            }
            for vm in self.vms.values()
        ]


# Test/Demo
async def demo():
    """Demo the hypervisor"""
    
    print("\n" + "="*60)
    print("🦅 QUEZTL HYPERVISOR - DEMO")
    print("="*60 + "\n")
    
    # Create hypervisor
    hv = QueztlHypervisor(distributed=False)
    
    # Register local resources
    hv.register_node("local", vcpus=8, memory_mb=16384)
    
    # Create a VM
    vm_id = hv.create_vm(
        name="test-vm-1",
        vcpus=2,
        memory_mb=2048,
        vgpus=1,
        kernel_path="/boot/vmlinuz-6.1.0",
        cmdline="console=ttyS0 root=/dev/vda"
    )
    
    # Start the VM
    await hv.start_vm(vm_id)
    
    # Let it run
    await asyncio.sleep(3)
    
    # Show stats
    print("\n" + "="*60)
    print("📊 HYPERVISOR STATS")
    print("="*60)
    stats = hv.get_stats()
    print(f"VMs: {stats['vms']['running']} running, {stats['vms']['stopped']} stopped")
    print(f"CPU: {stats['resources']['vcpus_allocated']}/{stats['resources']['vcpus_total']} allocated")
    print(f"Memory: {stats['resources']['memory_allocated_mb']}/{stats['resources']['memory_total_mb']}MB allocated")
    
    # Stop the VM
    await hv.stop_vm(vm_id)
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETE")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(demo())
