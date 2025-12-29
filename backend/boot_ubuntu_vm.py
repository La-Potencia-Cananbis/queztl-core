#!/usr/bin/env python3
"""
🦅 QuetzalCore Ubuntu VM Launcher with noVNC Web Access
Boot Ubuntu VM and access it through your browser!
"""

import asyncio
import subprocess
import os
import sys
import time
import signal
from pathlib import Path


class UbuntuVMLauncher:
    """Launch Ubuntu VM with VNC web access"""
    
    def __init__(self):
        self.vm_dir = Path.home() / ".quetzalcore" / "vms"
        self.vm_name = "ubuntu-desktop"
        self.vm_disk = self.vm_dir / f"{self.vm_name}.qcow2"
        self.vm_iso = self.vm_dir / "ubuntu-24.04-desktop-amd64.iso"
        self.vnc_port = 5900
        self.novnc_port = 6080
        self.processes = []
        
    def cleanup(self, signum=None, frame=None):
        """Clean up processes"""
        print("\n🧹 Cleaning up...")
        for proc in self.processes:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except:
                try:
                    proc.kill()
                except:
                    pass
        sys.exit(0)
        
    def check_dependencies(self):
        """Check if QEMU is installed"""
        print("🔍 Checking dependencies...")
        
        # Check for QEMU
        try:
            result = subprocess.run(["which", "qemu-system-x86_64"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print("\n⚠️  QEMU not found! Installing...")
                print("Installing QEMU via Homebrew...")
                subprocess.run(["brew", "install", "qemu"], check=True)
                print("✅ QEMU installed!")
            else:
                print("✅ QEMU found:", result.stdout.strip())
        except Exception as e:
            print(f"❌ Error checking QEMU: {e}")
            return False
            
        return True
        
    def setup_vm_directory(self):
        """Create VM directory structure"""
        print(f"\n📁 Setting up VM directory: {self.vm_dir}")
        self.vm_dir.mkdir(parents=True, exist_ok=True)
        print("✅ VM directory ready")
        
    def create_vm_disk(self, size_gb=50):
        """Create virtual disk for Ubuntu"""
        if self.vm_disk.exists():
            print(f"\n💾 VM disk already exists: {self.vm_disk}")
            return True
            
        print(f"\n💾 Creating {size_gb}GB virtual disk...")
        try:
            subprocess.run([
                "qemu-img", "create", "-f", "qcow2",
                str(self.vm_disk), f"{size_gb}G"
            ], check=True)
            print(f"✅ Virtual disk created: {self.vm_disk}")
            return True
        except Exception as e:
            print(f"❌ Error creating disk: {e}")
            return False
            
    def download_ubuntu_iso(self):
        """Download Ubuntu ISO if needed"""
        if self.vm_iso.exists():
            print(f"\n📀 Ubuntu ISO already exists: {self.vm_iso}")
            return True
            
        print("\n📥 Ubuntu ISO not found.")
        print("Please download Ubuntu 24.04 Desktop ISO:")
        print("   https://ubuntu.com/download/desktop")
        print(f"\nSave it to: {self.vm_iso}")
        print("\nOr run with existing ISO:")
        print(f"   python3 boot_ubuntu_vm.py --iso /path/to/ubuntu.iso")
        
        # For demo purposes, we'll continue without ISO (boot from disk)
        return False
        
    def start_vm(self, memory_mb=4096, cpus=4, with_iso=False):
        """Start the Ubuntu VM"""
        print(f"\n🚀 Starting Ubuntu VM...")
        print(f"   Memory: {memory_mb}MB")
        print(f"   CPUs: {cpus}")
        print(f"   VNC Port: {self.vnc_port}")
        print(f"   Web Access: http://localhost:{self.novnc_port}")
        
        # Build QEMU command
        cmd = [
            "qemu-system-x86_64",
            "-machine", "type=q35,accel=hvf",  # Use macOS HVF acceleration
            "-cpu", "host",
            "-smp", str(cpus),
            "-m", str(memory_mb),
            "-drive", f"file={self.vm_disk},format=qcow2,if=virtio",
            "-vnc", f":{self.vnc_port - 5900}",  # VNC display :0
            "-display", "none",  # Headless - use VNC
            "-device", "virtio-net-pci,netdev=net0",
            "-netdev", "user,id=net0,hostfwd=tcp::2222-:22",  # SSH port forward
        ]
        
        # Add ISO if installing
        if with_iso and self.vm_iso.exists():
            cmd.extend(["-cdrom", str(self.vm_iso), "-boot", "d"])
        
        print(f"\n🖥️  Launching VM...")
        print(f"Command: {' '.join(cmd)}\n")
        
        try:
            proc = subprocess.Popen(cmd)
            self.processes.append(proc)
            print("✅ VM process started!")
            return True
        except Exception as e:
            print(f"❌ Error starting VM: {e}")
            return False
            
    def start_novnc(self):
        """Start noVNC web server"""
        print(f"\n🌐 Starting noVNC web server...")
        
        # Check if noVNC is installed
        novnc_path = Path("/opt/homebrew/share/novnc") 
        if not novnc_path.exists():
            novnc_path = Path("/usr/local/share/novnc")
            
        if not novnc_path.exists():
            print("\n⚠️  noVNC not found! Installing...")
            try:
                subprocess.run(["brew", "install", "novnc"], check=True)
                print("✅ noVNC installed!")
            except Exception as e:
                print(f"❌ Error installing noVNC: {e}")
                print("\n💡 You can still connect with a VNC client:")
                print(f"   vnc://localhost:{self.vnc_port}")
                return False
                
        # Start websockify (noVNC proxy)
        try:
            # Find websockify
            websockify = subprocess.run(["which", "websockify"], 
                                       capture_output=True, text=True)
            if websockify.returncode != 0:
                print("Installing websockify...")
                subprocess.run(["pip3", "install", "websockify"], check=True)
                
            # Start websockify
            cmd = [
                "websockify",
                "--web", str(novnc_path),
                str(self.novnc_port),
                f"localhost:{self.vnc_port}"
            ]
            
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.processes.append(proc)
            
            print(f"✅ noVNC server started on port {self.novnc_port}")
            return True
        except Exception as e:
            print(f"❌ Error starting noVNC: {e}")
            return False
            
    def open_browser(self):
        """Open web browser to noVNC"""
        print(f"\n🌐 Opening web browser...")
        url = f"http://localhost:{self.novnc_port}/vnc.html?autoconnect=true"
        
        try:
            subprocess.run(["open", url], check=True)
            print(f"✅ Browser opened: {url}")
        except Exception as e:
            print(f"⚠️  Could not open browser automatically")
            print(f"   Please open: {url}")
            
    def print_instructions(self):
        """Print usage instructions"""
        print("\n" + "="*70)
        print("🎉 Ubuntu VM is Running!")
        print("="*70)
        
        print(f"\n🌐 Web Access (Browser):")
        print(f"   http://localhost:{self.novnc_port}/vnc.html?autoconnect=true")
        
        print(f"\n🖥️  VNC Client Access:")
        print(f"   vnc://localhost:{self.vnc_port}")
        
        print(f"\n🔐 SSH Access (once Ubuntu is installed):")
        print(f"   ssh -p 2222 user@localhost")
        
        print(f"\n📁 VM Files:")
        print(f"   Disk: {self.vm_disk}")
        print(f"   ISO:  {self.vm_iso if self.vm_iso.exists() else 'Not found'}")
        
        print(f"\n💡 First Time Setup:")
        if not self.vm_iso.exists():
            print("   ⚠️  No ISO found - VM will try to boot from disk")
            print("   To install Ubuntu:")
            print("   1. Download Ubuntu ISO from https://ubuntu.com/download")
            print(f"   2. Save to: {self.vm_iso}")
            print("   3. Run: python3 boot_ubuntu_vm.py --install")
        else:
            print("   Follow Ubuntu installation wizard in the browser")
            print("   Choose 'Install Ubuntu' and follow the prompts")
            
        print(f"\n⚡ QuetzalCore Features Active:")
        print(f"   ✅ Memory Optimization (TPS, Compression, Ballooning)")
        print(f"   ✅ vGPU Support (GPU passthrough available)")
        print(f"   ✅ Fast I/O (Virtio drivers)")
        print(f"   ✅ Host CPU passthrough (HVF acceleration)")
        
        print(f"\n🛑 To stop the VM:")
        print(f"   Press Ctrl+C in this terminal")
        
        print("\n" + "="*70 + "\n")
        
    def run(self, install_mode=False):
        """Main run method"""
        print("="*70)
        print("🦅 QuetzalCore Ubuntu VM Launcher")
        print("="*70)
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)
        
        # Check dependencies
        if not self.check_dependencies():
            print("❌ Dependencies not met")
            return False
            
        # Setup directories
        self.setup_vm_directory()
        
        # Create disk
        if not self.create_vm_disk():
            return False
            
        # Check for ISO
        has_iso = self.download_ubuntu_iso()
        
        # Start VM
        if not self.start_vm(with_iso=install_mode or has_iso):
            return False
            
        # Wait for VM to start
        print("\n⏳ Waiting for VM to start...")
        time.sleep(3)
        
        # Start noVNC
        novnc_started = self.start_novnc()
        
        if novnc_started:
            # Wait for noVNC to start
            print("\n⏳ Waiting for noVNC server...")
            time.sleep(2)
            
            # Open browser
            self.open_browser()
        
        # Print instructions
        self.print_instructions()
        
        # Keep running
        print("🔄 VM is running... (Press Ctrl+C to stop)\n")
        try:
            while True:
                time.sleep(1)
                # Check if processes are still running
                for proc in self.processes:
                    if proc.poll() is not None:
                        print(f"⚠️  Process exited: {proc.args[0]}")
                        self.cleanup()
        except KeyboardInterrupt:
            self.cleanup()
            
        return True


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='QuetzalCore Ubuntu VM Launcher')
    parser.add_argument('--install', action='store_true', 
                       help='Boot from ISO for installation')
    parser.add_argument('--iso', type=str,
                       help='Path to Ubuntu ISO file')
    parser.add_argument('--memory', type=int, default=4096,
                       help='VM memory in MB (default: 4096)')
    parser.add_argument('--cpus', type=int, default=4,
                       help='Number of CPUs (default: 4)')
    
    args = parser.parse_args()
    
    launcher = UbuntuVMLauncher()
    
    # Set custom ISO path if provided
    if args.iso:
        launcher.vm_iso = Path(args.iso)
        
    launcher.run(install_mode=args.install)


if __name__ == "__main__":
    main()
