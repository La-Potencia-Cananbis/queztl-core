#!/usr/bin/env python3
# """
#  QuetzalCore Custom Linux OS Builder

# Features:
# - Minimal Linux kernel build
# - Custom kernel configuration
# - QuetzalCore-optimized settings
# - Hypervisor integration
# - Fast boot optimization
# """

# import asyncio
# import json
# import subprocess
# from pathlib import Path
# from typing import List, Dict, Optional
# import logging

# logger = logging.getLogger(__name__)


# class QuetzalCoreOSBuilder:
    """
#     Build custom minimal Linux OS for QuetzalCore
#     Way better than Ubuntu/Debian - only what we need!
    """
    
#     def __init__(self, build_dir: str = "./quetzalcore-os"):
#         self.build_dir = Path(build_dir)
#         self.build_dir.mkdir(exist_ok=True)
        
#         self.kernel_version = "6.6.10"  # Latest stable
#         self.kernel_url = f"https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-{self.kernel_version}.tar.xz"
        
#         self.config = self._get_default_config()
        
#         logger.info(f" QuetzalCore OS Builder initialized")
    
#     def _get_default_config(self) -> Dict:
        """Get default kernel configuration"""
#         return {
            # Core kernel features
            "CONFIG_64BIT": "y",
            "CONFIG_X86_64": "y",
            "CONFIG_SMP": "y",
            "CONFIG_PREEMPT": "y",
            
            # Virtualization support
            "CONFIG_KVM": "y",
            "CONFIG_KVM_INTEL": "y",
            "CONFIG_KVM_AMD": "y",
            "CONFIG_VHOST_NET": "y",
            "CONFIG_VIRTIO": "y",
            "CONFIG_VIRTIO_PCI": "y",
            "CONFIG_VIRTIO_NET": "y",
            "CONFIG_VIRTIO_BLK": "y",
            
            # Performance optimizations
            "CONFIG_HZ_1000": "y",
            "CONFIG_NO_HZ_FULL": "y",
            "CONFIG_RCU_NOCB_CPU": "y",
            
            # Disable unnecessary features
            "CONFIG_SOUND": "n",
            "CONFIG_USB_SUPPORT": "n",
            "CONFIG_WIRELESS": "n",
            "CONFIG_BLUETOOTH": "n",
            "CONFIG_DRM": "n",
            
            # Networking (minimal)
            "CONFIG_NET": "y",
            "CONFIG_INET": "y",
            "CONFIG_PACKET": "y",
            
            # File systems (minimal)
            "CONFIG_EXT4_FS": "y",
            "CONFIG_TMPFS": "y",
            "CONFIG_PROC_FS": "y",
            "CONFIG_SYSFS": "y",
            
            # Security
            "CONFIG_SECURITY": "y",
            "CONFIG_SECCOMP": "y",
            
            # QuetzalCore specific
            "CONFIG_JUMP_LABEL": "y",
            "CONFIG_BPF_JIT": "y",
        }
    
#     async def download_kernel(self) -> bool:
        """Download Linux kernel source"""
#         try:
#             kernel_tarball = self.build_dir / f"linux-{self.kernel_version}.tar.xz"
            
#             if kernel_tarball.exists():
#                 logger.info(f" Kernel source already downloaded")
#                 return True
            
#             logger.info(f" Downloading kernel {self.kernel_version}...")
            
#             proc = await asyncio.create_subprocess_exec(
                "curl", "-L", "-o", str(kernel_tarball), self.kernel_url,
#                 stdout=asyncio.subprocess.PIPE,
#                 stderr=asyncio.subprocess.PIPE
            
#             await proc.communicate()
            
#             if proc.returncode == 0:
#                 logger.info(f" Kernel downloaded: {kernel_tarball}")
#                 return True
#             else:
#                 logger.error(f"Failed to download kernel")
#                 return False
                
#         except Exception as e:
#             logger.error(f"Error downloading kernel: {e}")
#             return False
    
#     async def extract_kernel(self) -> bool:
        """Extract kernel source"""
#         try:
#             kernel_tarball = self.build_dir / f"linux-{self.kernel_version}.tar.xz"
#             kernel_src = self.build_dir / f"linux-{self.kernel_version}"
            
#             if kernel_src.exists():
#                 logger.info(f" Kernel already extracted")
#                 return True
            
#             logger.info(f" Extracting kernel source...")
            
#             proc = await asyncio.create_subprocess_exec(
                "tar", "-xf", str(kernel_tarball), "-C", str(self.build_dir),
#                 stdout=asyncio.subprocess.PIPE,
#                 stderr=asyncio.subprocess.PIPE
            
#             await proc.communicate()
            
#             if proc.returncode == 0:
#                 logger.info(f" Kernel extracted: {kernel_src}")
#                 return True
#             else:
#                 logger.error(f"Failed to extract kernel")
#                 return False
                
#         except Exception as e:
#             logger.error(f"Error extracting kernel: {e}")
#             return False
    
#     async def configure_kernel(self) -> bool:
        """Configure kernel with QuetzalCore settings"""
#         try:
#             kernel_src = self.build_dir / f"linux-{self.kernel_version}"
#             config_file = kernel_src / ".config"
            
#             logger.info(f" Configuring kernel...")
            
            # Start with minimal config
#             proc = await asyncio.create_subprocess_exec(
                "make", "tinyconfig",
#                 cwd=kernel_src,
#                 stdout=asyncio.subprocess.PIPE,
#                 stderr=asyncio.subprocess.PIPE
            
#             await proc.communicate()
            
            # Apply QuetzalCore configuration
#             with open(config_file, 'a') as f:
#                 f.write("\n# QuetzalCore Custom Configuration\n")
#                 for key, value in self.config.items():
#                     f.write(f"{key}={value}\n")
            
            # Run olddefconfig to resolve dependencies
#             proc = await asyncio.create_subprocess_exec(
                "make", "olddefconfig",
#                 cwd=kernel_src,
#                 stdout=asyncio.subprocess.PIPE,
#                 stderr=asyncio.subprocess.PIPE
            
#             await proc.communicate()
            
#             logger.info(f" Kernel configured")
#             return True
            
#         except Exception as e:
#             logger.error(f"Error configuring kernel: {e}")
#             return False
    
#     async def build_kernel(self, num_cores: int = 8) -> bool:
        """Build the kernel"""
#         try:
#             kernel_src = self.build_dir / f"linux-{self.kernel_version}"
            
#             logger.info(f" Building kernel with {num_cores} cores...")
#             logger.info(f" This will take 10-30 minutes...")
            
#             proc = await asyncio.create_subprocess_exec(
                "make", "-j", str(num_cores),
#                 cwd=kernel_src,
#                 stdout=asyncio.subprocess.PIPE,
#                 stderr=asyncio.subprocess.PIPE
            
#             stdout, stderr = await proc.communicate()
            
#             if proc.returncode == 0:
#                 logger.info(f" Kernel built successfully!")
#                 return True
#             else:
#                 logger.error(f"Failed to build kernel")
#                 logger.error(stderr.decode())
#                 return False
                
#         except Exception as e:
#             logger.error(f"Error building kernel: {e}")
#             return False
    
#     async def build_initramfs(self) -> bool:
        """Build minimal initramfs"""
#         try:
#             initramfs_dir = self.build_dir / "initramfs"
#             initramfs_dir.mkdir(exist_ok=True)
            
#             logger.info(f" Building initramfs...")
            
            # Create basic directory structure
#             dirs = ["bin", "sbin", "etc", "proc", "sys", "dev", "tmp", "lib", "lib64"]
#             for d in dirs:
                (initramfs_dir / d).mkdir(exist_ok=True)
            
            # Create init script
#             init_script = initramfs_dir / "init"
#             init_script.write_text("""#!/bin/sh

# QuetzalCore minimal init

# mount -t proc none /proc
# mount -t sysfs none /sys
# mount -t devtmpfs none /dev

# echo " QuetzalCore OS booting..."

# Start QuetzalCore hypervisor
/sbin/quetzalcore-hypervisor

# Keep running
# exec /bin/sh
""")
#             init_script.chmod(0o755)
            
            # Create initramfs archive
#             initramfs_file = self.build_dir / "initramfs.cpio.gz"
            
#             proc = await asyncio.create_subprocess_exec(
                "sh", "-c",
#                 f"cd {initramfs_dir} && find . | cpio -o -H newc | gzip > {initramfs_file}",
#                 stdout=asyncio.subprocess.PIPE,
#                 stderr=asyncio.subprocess.PIPE
            
#             await proc.communicate()
            
#             logger.info(f" Initramfs built: {initramfs_file}")
#             return True
            
#         except Exception as e:
#             logger.error(f"Error building initramfs: {e}")
#             return False
    
#     async def create_bootable_image(self) -> bool:
        """Create bootable disk image"""
#         try:
#             kernel_src = self.build_dir / f"linux-{self.kernel_version}"
#             kernel_image = kernel_src / "arch/x86/boot/bzImage"
#             initramfs_file = self.build_dir / "initramfs.cpio.gz"
            
#             iso_dir = self.build_dir / "iso"
#             iso_dir.mkdir(exist_ok=True)
            
#             boot_dir = iso_dir / "boot"
#             boot_dir.mkdir(exist_ok=True)
            
            # Copy kernel and initramfs
#             import shutil
#             shutil.copy(kernel_image, boot_dir / "vmlinuz")
#             shutil.copy(initramfs_file, boot_dir / "initramfs.gz")
            
            # Create GRUB config
#             grub_dir = iso_dir / "boot/grub"
#             grub_dir.mkdir(exist_ok=True)
            
#             grub_cfg = grub_dir / "grub.cfg"
#             grub_cfg.write_text("""
# set timeout=0
# set default=0

# menuentry "QuetzalCore OS" {
#     linux /boot/vmlinuz quiet
#     initrd /boot/initramfs.gz
}
""")
            
            # Create ISO
#             iso_file = self.build_dir / "quetzalcore-os.iso"
            
#             logger.info(f" Creating bootable ISO...")
            
#             proc = await asyncio.create_subprocess_exec(
                "grub-mkrescue", "-o", str(iso_file), str(iso_dir),
#                 stdout=asyncio.subprocess.PIPE,
#                 stderr=asyncio.subprocess.PIPE
            
#             await proc.communicate()
            
#             if proc.returncode == 0:
#                 logger.info(f" Bootable ISO created: {iso_file}")
#                 return True
#             else:
#                 logger.warning(f" ISO creation failed (grub-mkrescue not installed?)")
#                 logger.info(f" Kernel and initramfs available in {boot_dir}")
#                 return False
                
#         except Exception as e:
#             logger.error(f"Error creating bootable image: {e}")
#             return False
    
#     async def build_full_os(self) -> bool:
        """Build complete QuetzalCore OS"""
#         logger.info(f" Starting QuetzalCore OS build...")
        
#         steps = [
            ("Download kernel", self.download_kernel),
            ("Extract kernel", self.extract_kernel),
            ("Configure kernel", self.configure_kernel),
            ("Build kernel", self.build_kernel),
            ("Build initramfs", self.build_initramfs),
            ("Create bootable image", self.create_bootable_image),
        ]
        
#         for step_name, step_func in steps:
#             logger.info(f"\n {step_name}...")
#             success = await step_func()
            
#             if not success:
#                 logger.error(f" Failed at: {step_name}")
#                 return False
        
#         logger.info(f"\n QuetzalCore OS build complete!")
#         logger.info(f" Build directory: {self.build_dir}")
#         logger.info(f" ISO image: {self.build_dir}/quetzalcore-os.iso")
        
#         return True
    
#     def get_build_info(self) -> Dict:
        """Get build information"""
#         kernel_src = self.build_dir / f"linux-{self.kernel_version}"
#         kernel_image = kernel_src / "arch/x86/boot/bzImage"
#         iso_file = self.build_dir / "quetzalcore-os.iso"
        
#         return {
            "kernel_version": self.kernel_version,
            "build_dir": str(self.build_dir),
            "kernel_built": kernel_image.exists(),
            "iso_created": iso_file.exists(),
            "config_options": len(self.config)
        }


# Example usage
# async def main():
    """Build QuetzalCore OS"""
    
#     builder = QuetzalCoreOSBuilder()
    
    # Build full OS
#     success = await builder.build_full_os()
    
#     if success:
#         info = builder.get_build_info()
#         print(f"\n Build successful!")
#         print(f"Kernel: {info['kernel_version']}")
#         print(f"Config options: {info['config_options']}")


# if __name__ == "__main__":
#     asyncio.run(main())
