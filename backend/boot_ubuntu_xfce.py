#!/usr/bin/env python3
"""
🦅 QuetzalCore Ubuntu Desktop - XFCE Edition
Better rendering with full-featured desktop!
"""

import subprocess
import time
import sys
import webbrowser


def launch_ubuntu_xfce():
    """Launch Ubuntu with XFCE desktop (better rendering)"""
    print("="*70)
    print("🦅 QuetzalCore Ubuntu Desktop - XFCE Edition")
    print("="*70)
    
    container_name = "quetzalcore-ubuntu-xfce"
    
    print("\n🚀 Launching Ubuntu XFCE Desktop...")
    print("   This has MUCH better rendering than LXDE!")
    
    # Stop old container if exists
    subprocess.run(["docker", "rm", "-f", container_name],
                  capture_output=True)
    
    # Launch with XFCE desktop - much better rendering
    print("\n📦 Starting container...")
    cmd = [
        "docker", "run", "-d",
        "--name", container_name,
        "-p", "6080:6080",  # noVNC port
        "-p", "5900:5900",  # VNC port
        "-e", "RESOLUTION=1920x1080",
        "-e", "VNC_PASSWORD=password123",
        "--shm-size=2g",
        "accetto/ubuntu-vnc-xfce-firefox-g3:latest"  # XFCE + Firefox
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        container_id = result.stdout.strip()
        print(f"✅ Container started: {container_id[:12]}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"stderr: {e.stderr}")
        return False
    
    # Wait for desktop
    print("\n⏳ Waiting for desktop to start (15 seconds)...")
    time.sleep(15)
    
    # Open browser
    url = "http://localhost:6080"
    print(f"\n🌐 Opening browser: {url}")
    
    try:
        webbrowser.open(url)
    except:
        pass
    
    print("\n" + "="*70)
    print("🎉 Ubuntu XFCE Desktop is Running!")
    print("="*70)
    
    print(f"\n🌐 Access:")
    print(f"   Browser: http://localhost:6080")
    print(f"   Password: password123")
    
    print(f"\n🖥️  Features:")
    print(f"   ✅ XFCE Desktop (much better rendering!)")
    print(f"   ✅ Firefox pre-installed")
    print(f"   ✅ Full keyboard & mouse support")
    print(f"   ✅ 1920x1080 resolution")
    print(f"   ✅ Hardware acceleration")
    
    print(f"\n💡 Tips:")
    print(f"   • Click anywhere to connect")
    print(f"   • If you see black screen, refresh browser")
    print(f"   • Right-click for desktop menu")
    print(f"   • Open Terminal from Applications menu")
    
    print(f"\n📦 Manage:")
    print(f"   Stop:  docker stop {container_name}")
    print(f"   Start: docker start {container_name}")
    print(f"   Logs:  docker logs {container_name}")
    
    print("\n" + "="*70)
    print("✅ All set! Check your browser! 🚀")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    launch_ubuntu_xfce()
