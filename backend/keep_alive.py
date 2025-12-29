#!/usr/bin/env python3
"""
Backend Health Runner - Keeps cloud services awake and monitors health
Pings every 5 minutes to prevent cold starts on free tier services
"""
import requests
import time
from datetime import datetime
import sys

BACKENDS = [
    {
        "name": "Hive Backend (Render)",
        "url": "https://hive-backend.onrender.com",
        "health_endpoint": "/api/health",
        "ping_interval": 300  # 5 minutes
    }
]

def ping_backend(backend):
    """Ping backend to keep it alive"""
    try:
        url = backend["url"]
        health_url = f"{url}{backend['health_endpoint']}"
        
        # Try health endpoint first
        response = requests.get(health_url, timeout=30)
        if response.status_code == 200:
            return True, "✅ Healthy"
        elif response.status_code == 404:
            # Health endpoint not found, try root
            response = requests.get(url, timeout=30)
            if response.status_code in [200, 404]:
                return True, "✅ Alive (no health endpoint)"
        
        return False, f"❌ Status {response.status_code}"
        
    except requests.Timeout:
        return False, "⏳ Timeout (possibly cold start)"
    except Exception as e:
        return False, f"❌ Error: {str(e)[:50]}"

def run_health_monitor(duration_hours=24):
    """
    Run continuous health monitoring
    
    Args:
        duration_hours: How long to run (default: 24 hours)
    """
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║           QUEZTL BACKEND HEALTH RUNNER - KEEP ALIVE           ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"\n⏱️  Duration: {duration_hours} hours")
    print(f"🚀 Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📡 Monitoring {len(BACKENDS)} backend(s)\n")
    
    start_time = time.time()
    end_time = start_time + (duration_hours * 3600)
    
    # Initial ping
    print("="*70)
    print("🔄 Initial Health Check")
    print("="*70)
    for backend in BACKENDS:
        print(f"\n📍 {backend['name']}")
        print(f"   URL: {backend['url']}")
        is_healthy, status = ping_backend(backend)
        print(f"   Status: {status}")
    
    iteration = 0
    
    try:
        while time.time() < end_time:
            iteration += 1
            
            # Calculate next wake time
            next_wake = time.time() + min(b["ping_interval"] for b in BACKENDS)
            sleep_duration = next_wake - time.time()
            
            if sleep_duration > 0:
                elapsed_hours = (time.time() - start_time) / 3600
                remaining_hours = (end_time - time.time()) / 3600
                
                print(f"\n💤 Sleeping {sleep_duration:.0f}s | Elapsed: {elapsed_hours:.1f}h | Remaining: {remaining_hours:.1f}h")
                time.sleep(sleep_duration)
            
            # Ping all backends
            print("\n" + "="*70)
            print(f"🔄 Health Check #{iteration} - {datetime.now().strftime('%H:%M:%S')}")
            print("="*70)
            
            for backend in BACKENDS:
                print(f"\n📍 {backend['name']}")
                is_healthy, status = ping_backend(backend)
                print(f"   Status: {status}")
                
                if not is_healthy:
                    print(f"   ⚠️  Retrying in 10s...")
                    time.sleep(10)
                    is_healthy, status = ping_backend(backend)
                    print(f"   Retry Status: {status}")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Health monitor stopped by user")
    
    total_hours = (time.time() - start_time) / 3600
    print("\n" + "="*70)
    print("✅ HEALTH MONITOR COMPLETE")
    print("="*70)
    print(f"⏱️  Total runtime: {total_hours:.1f} hours")
    print(f"🔄 Health checks: {iteration}")
    print(f"📅 End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    # Parse command line args
    duration = 24  # default 24 hours
    
    if len(sys.argv) > 1:
        try:
            duration = float(sys.argv[1])
        except:
            pass
    
    run_health_monitor(duration)
