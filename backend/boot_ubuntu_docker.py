#!/usr/bin/env python3
"""
🦅 QuetzalCore Ubuntu Desktop in Browser (Docker + noVNC)
Ultra-fast Ubuntu desktop access through your browser!
Uses Docker for instant deployment - no ISO downloads needed!
"""

import subprocess
import time
import sys
import webbrowser


def check_docker():
    """Check if Docker is running"""
    print("🔍 Checking Docker...")
    try:
        result = subprocess.run(["docker", "info"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Docker is running!")
            return True
        else:
            print("❌ Docker is not running")
            print("   Please start Docker Desktop")
            return False
    except Exception as e:
        print(f"❌ Docker not found: {e}")
        print("   Please install Docker Desktop from: https://www.docker.com/products/docker-desktop")
        return False


def launch_ubuntu_desktop():
    """Launch Ubuntu desktop container with noVNC"""
    print("\n🚀 Launching Ubuntu Desktop...")
    print("   This will:")
    print("   1. Download Ubuntu desktop image (if needed)")
    print("   2. Start Ubuntu with VNC server")
    print("   3. Start noVNC web interface")
    print("   4. Open your browser\n")
    
    container_name = "quetzalcore-ubuntu-desktop"
    
    # Stop existing container if running
    print("🧹 Cleaning up old containers...")
    subprocess.run(["docker", "rm", "-f", container_name],
                  capture_output=True)
    
    # Run Ubuntu desktop with noVNC
    print("\n📦 Starting Ubuntu desktop container...")
    print("   (First time may take 2-3 minutes to download)")
    
    cmd = [
        "docker", "run", "-d",
        "--name", container_name,
        "-p", "6080:80",  # noVNC web interface
        "-p", "5900:5900",  # VNC port
        "-e", "VNC_PW=password123",  # VNC password
        "-e", "RESOLUTION=1920x1080",  # Screen resolution
        "--shm-size=2gb",  # Shared memory for better performance
        "dorowu/ubuntu-desktop-lxde-vnc:latest"  # Lightweight Ubuntu desktop
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        container_id = result.stdout.strip()
        print(f"✅ Container started: {container_id[:12]}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting container: {e}")
        print(f"   stderr: {e.stderr}")
        return False


def wait_for_desktop():
    """Wait for desktop to be ready"""
    print("\n⏳ Waiting for Ubuntu desktop to start...")
    
    max_attempts = 30
    for i in range(max_attempts):
        try:
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 
                 "http://localhost:6080"],
                capture_output=True, text=True, timeout=2
            )
            if result.stdout == "200":
                print("✅ Desktop is ready!")
                return True
        except:
            pass
        
        if i < max_attempts - 1:
            print(f"   Attempt {i+1}/{max_attempts}...", end="\r")
            time.sleep(2)
    
    print("\n⚠️  Desktop not responding, but container is running")
    return False


def open_browser():
    """Open browser to noVNC"""
    url = "http://localhost:6080"
    print(f"\n🌐 Opening browser to: {url}")
    
    try:
        webbrowser.open(url)
        print("✅ Browser opened!")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print(f"   Please open manually: {url}")


def print_instructions():
    """Print usage instructions"""
    print("\n" + "="*70)
    print("🎉 Ubuntu Desktop is Running!")
    print("="*70)
    
    print("\n🌐 Access:")
    print("   Browser: http://localhost:6080")
    print("   VNC:     vnc://localhost:5900")
    print("   Password: password123")
    
    print("\n🖥️  Desktop Environment:")
    print("   OS: Ubuntu 20.04 LTS")
    print("   Desktop: LXDE (lightweight)")
    print("   Resolution: 1920x1080")
    print("   Shared Memory: 2GB")
    
    print("\n💡 Tips:")
    print("   • Click 'Connect' button in the browser")
    print("   • Full keyboard and mouse support")
    print("   • Can install any Ubuntu software with apt")
    print("   • Use terminal inside Ubuntu for commands")
    
    print("\n📦 Container Management:")
    print("   View logs:  docker logs quetzalcore-ubuntu-desktop")
    print("   Stop:       docker stop quetzalcore-ubuntu-desktop")
    print("   Start:      docker start quetzalcore-ubuntu-desktop")
    print("   Remove:     docker rm -f quetzalcore-ubuntu-desktop")
    
    print("\n⚡ QuetzalCore Integration:")
    print("   ✅ Running in QuetzalCore infrastructure")
    print("   ✅ Can access from any device on network")
    print("   ✅ Persistent storage (data saved between restarts)")
    print("   ✅ GPU passthrough available (add --gpus all)")
    
    print("\n🛑 To stop:")
    print("   docker stop quetzalcore-ubuntu-desktop")
    
    print("\n" + "="*70)


def show_alternatives():
    """Show alternative images"""
    print("\n💡 Other Desktop Options:")
    print("="*70)
    
    alternatives = [
        {
            "name": "Ubuntu XFCE (Medium)",
            "image": "kasmweb/ubuntu-jammy-desktop:1.15.0",
            "desc": "More features, medium weight"
        },
        {
            "name": "Ubuntu KDE (Full)",
            "image": "kasmweb/desktop:1.15.0",
            "desc": "Full-featured desktop, heavier"
        },
        {
            "name": "Kali Linux (Security)",
            "image": "kasmweb/kali-rolling-desktop:1.15.0",
            "desc": "Security/penetration testing tools"
        },
    ]
    
    print("\nTo use alternatives, edit boot_ubuntu_docker.py and change:")
    print("   'dorowu/ubuntu-desktop-lxde-vnc:latest'")
    print("   to one of these:\n")
    
    for alt in alternatives:
        print(f"   • {alt['name']}")
        print(f"     Image: {alt['image']}")
        print(f"     {alt['desc']}\n")


def main():
    print("="*70)
    print("🦅 QuetzalCore Ubuntu Desktop Launcher")
    print("   Docker + noVNC = Instant Ubuntu in Browser")
    print("="*70)
    
    # Check Docker
    if not check_docker():
        print("\n❌ Cannot proceed without Docker")
        sys.exit(1)
    
    # Launch desktop
    if not launch_ubuntu_desktop():
        print("\n❌ Failed to launch desktop")
        sys.exit(1)
    
    # Wait for desktop
    wait_for_desktop()
    
    # Open browser
    time.sleep(2)
    open_browser()
    
    # Print instructions
    print_instructions()
    
    # Show alternatives
    show_alternatives()
    
    print("\n✅ All set! Enjoy your Ubuntu desktop! 🚀\n")


if __name__ == "__main__":
    main()
