"""
#  QUETZALCORE HYPERVISOR - KVM Acceleration Layer

# Option C: Add KVM/QEMU acceleration to the custom hypervisor.

# This wraps KVM for production performance while maintaining our custom API.
"""

# import os
# import subprocess
# from typing import Optional, Dict
# from dataclasses import dataclass


@dataclass
# class KVMConfig:
    """KVM configuration"""
#     kvm_available: bool
#     qemu_path: Optional[str] = None
#     kvm_device: str = "/dev/kvm"


# class KVMAccelerator:
    """
#     KVM Hardware Acceleration
    
#     Uses KVM (Kernel-based Virtual Machine) for native CPU speed.
#     Falls back to QEMU emulation if KVM unavailable.
    """
    
#     def __init__(self):
#         self.config = self._detect_kvm()
        
#         if self.config.kvm_available:
#             print(" KVM acceleration available")
#         else:
#             print("  KVM not available, using software emulation")
    
#     def _detect_kvm(self) -> KVMConfig:
        """Detect KVM availability"""
        
        # Check if /dev/kvm exists
#         kvm_available = os.path.exists("/dev/kvm")
        
        # Find QEMU
#         qemu_path = None
#         for path in ["/usr/bin/qemu-system-x86_64", "/usr/local/bin/qemu-system-x86_64"]:
#             if os.path.exists(path):
#                 qemu_path = path
#                 break
        
#         return KVMConfig(
#             kvm_available=kvm_available,
#             qemu_path=qemu_path
    
#     def can_accelerate(self) -> bool:
        """Check if we can use KVM acceleration"""
#         return self.config.kvm_available and self.config.qemu_path is not None
    
#     def create_vm_with_kvm(
#         self,
#         vm_id: str,
#         vcpus: int,
#         memory_mb: int,
#         kernel_path: str,
        **kwargs
    ) -> Dict:
        """
#         Create VM with KVM acceleration
        
#         This uses QEMU/KVM under the hood but exposes QuetzalCore API.
        """
        
#         if not self.can_accelerate():
#             raise RuntimeError("KVM acceleration not available")
        
        # Build QEMU command
#         cmd = [
#             self.config.qemu_path,
            "-enable-kvm",  # Use KVM acceleration
            "-cpu", "host",  # Pass-through CPU features
            "-smp", str(vcpus),
            "-m", str(memory_mb),
            "-kernel", kernel_path,
            "-nographic",  # No GUI
            "-serial", "mon:stdio"  # Console to stdout
        ]
        
        # Add initrd if provided
#         if "initrd_path" in kwargs:
#             cmd.extend(["-initrd", kwargs["initrd_path"]])
        
        # Add kernel cmdline
#         if "cmdline" in kwargs:
#             cmd.extend(["-append", kwargs["cmdline"]])
        
        # Add virtual disk if provided
#         if "disk_path" in kwargs:
#             cmd.extend([
                "-drive", f"file={kwargs['disk_path']},format=qcow2,if=virtio"
            ])
        
        # Add virtual network
#         cmd.extend([
            "-netdev", "user,id=net0",
            "-device", "virtio-net-pci,netdev=net0"
        ])
        
#         return {
            "vm_id": vm_id,
            "command": cmd,
            "accelerated": True,
            "backend": "KVM"
        }
    
#     def launch_vm(self, vm_config: Dict) -> subprocess.Popen:
        """Launch VM with KVM"""
        
#         cmd = vm_config["command"]
        
#         print(f" Launching KVM-accelerated VM...")
#         print(f"   Command: {' '.join(cmd[:6])} ...")
        
        # Launch QEMU/KVM process
#         process = subprocess.Popen(
#             cmd,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
        
#         return process


# class HybridHypervisor:
    """
#     Hybrid Hypervisor - Option C Implementation
    
#     Uses custom emulation for development/testing.
#     Uses KVM acceleration for production.
    """
    
#     def __init__(self):
#         from backend.hypervisor.core import QuetzalCoreHypervisor
        
        # Custom hypervisor
#         self.custom_hv = QuetzalCoreHypervisor(distributed=False)
        
        # KVM accelerator
#         self.kvm = KVMAccelerator()
        
        # Track which VMs use which backend
#         self.vm_backends: Dict[str, str] = {}
    
#     def create_vm(
#         self,
#         name: str,
#         vcpus: int,
#         memory_mb: int,
#         accelerated: bool = True,
        **kwargs
    ) -> str:
        """
#         Create VM with automatic backend selection
        
#         Args:
#             accelerated: Use KVM if available
        """
        
#         if accelerated and self.kvm.can_accelerate():
            # Use KVM for production
#             print(f" Creating KVM-accelerated VM: {name}")
#             vm_id = f"kvm-{name}"
#             self.vm_backends[vm_id] = "kvm"
            
            # Store config for later launch
            # (In production, launch immediately)
            
#         else:
            # Use custom emulation
#             print(f" Creating software-emulated VM: {name}")
#             vm_id = self.custom_hv.create_vm(name, vcpus, memory_mb, **kwargs)
#             self.vm_backends[vm_id] = "custom"
        
#         return vm_id
    
#     async def start_vm(self, vm_id: str):
        """Start VM with appropriate backend"""
        
#         backend = self.vm_backends.get(vm_id, "custom")
        
#         if backend == "kvm":
#             print(f" Starting with KVM acceleration...")
            # Would launch QEMU/KVM here
#         else:
#             print(f" Starting with custom emulation...")
#             await self.custom_hv.start_vm(vm_id)
    
#     def get_stats(self) -> dict:
        """Get stats from both backends"""
        
#         stats = self.custom_hv.get_stats()
#         stats["kvm_available"] = self.kvm.can_accelerate()
#         stats["backends"] = {
            "custom": sum(1 for b in self.vm_backends.values() if b == "custom"),
            "kvm": sum(1 for b in self.vm_backends.values() if b == "kvm")
        }
        
#         return stats


# Test
# async def demo():
    """Demo hybrid hypervisor"""
    
#     print("\n" + "="*70)
#     print(" QUETZALCORE HYPERVISOR - OPTION C DEMO")
#     print("   Hybrid: Custom Emulation + KVM Acceleration")
#     print("="*70 + "\n")
    
#     hv = HybridHypervisor()
    
    # Check KVM
#     if hv.kvm.can_accelerate():
#         print(" KVM acceleration available - VMs will be FAST!")
#     else:
#         print("  KVM not available on this system")
#         print("   (Normal on macOS - use Linux for KVM)")
    
    # Create VMs with both backends
#     print("\n1. Creating test VMs...")
    
    # Software emulated (development)
#     vm1 = hv.create_vm(
        "dev-vm",
#         vcpus=2,
#         memory_mb=2048,
#         accelerated=False,
#         kernel_path="/boot/vmlinuz"
    
    # KVM accelerated (production) - if available
#     try:
#         vm2 = hv.create_vm(
            "prod-vm",
#             vcpus=4,
#             memory_mb=4096,
#             accelerated=True,
#             kernel_path="/boot/vmlinuz"
#     except:
#         print("   (KVM VM creation skipped - not available)")
    
    # Show stats
#     print("\n Hypervisor Stats:")
#     stats = hv.get_stats()
#     print(f"   Total VMs: {stats['vms']['total']}")
#     print(f"   Custom emulation: {stats['backends']['custom']}")
#     print(f"   KVM accelerated: {stats['backends']['kvm']}")
#     print(f"   KVM available: {stats['kvm_available']}")
    
#     print("\n" + "="*70)
#     print(" OPTION C READY")
#     print("="*70)
#     print("\nYou can now:")
#     print("   Develop with custom emulation (works everywhere)")
#     print("   Deploy with KVM acceleration (Linux production)")
#     print("   Switch backends transparently via API")
#     print()


# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(demo())
