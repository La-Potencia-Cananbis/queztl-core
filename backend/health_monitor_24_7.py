#!/usr/bin/env python3
"""
QuetzalCore 24/7 Health Monitor
Runs independently, keeps services alive
"""

import requests
import time
import json
from datetime import datetime

SERVICES = {
    "backend": "https://queztl-core-backend.onrender.com/",
    "frontend": "https://lapotenciacann.com",
    "5k_renderer": "https://queztl-core-backend.onrender.com/api/render/5k"
}

def check_service(name, url):
    try:
        if "5k_renderer" in name:
            # POST request for 5K renderer
            response = requests.post(
                url,
                json={"scene_type": "benchmark", "width": 512, "height": 512, "return_image": False},
                timeout=30
            )
        else:
            response = requests.get(url, timeout=10)
        
        if response.status_code in [200, 201]:
            return True, f"✅ {name} is healthy"
        else:
            return False, f"⚠️ {name} returned {response.status_code}"
    except Exception as e:
        return False, f"❌ {name} error: {str(e)[:100]}"

def main():
    print("🦅 QuetzalCore Health Monitor Started")
    print("   Running 24/7 - No laptop required")
    print()
    
    cycle = 0
    while True:
        cycle += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{timestamp}] Health Check Cycle #{cycle}")
        print("=" * 60)
        
        all_healthy = True
        for name, url in SERVICES.items():
            healthy, message = check_service(name, url)
            print(f"  {message}")
            if not healthy:
                all_healthy = False
        
        if all_healthy:
            print("\n🎉 All services healthy!")
        else:
            print("\n⚠️ Some services need attention")
        
        # Wait 5 minutes between checks
        print(f"\n⏳ Next check in 5 minutes...")
        time.sleep(300)

if __name__ == "__main__":
    main()
