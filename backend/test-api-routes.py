#!/usr/bin/env python3
"""
QuetzalCore API Route Tester
Test all API endpoints to verify routing is working
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_route(method: str, path: str, data: Dict[str, Any] = None) -> tuple[bool, str]:
    """Test a single route"""
    url = f"{BASE_URL}{path}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data or {}, timeout=5)
        else:
            return False, f"Unknown method: {method}"
        
        if response.status_code < 500:
            return True, f"{response.status_code}"
        else:
            return False, f"{response.status_code}: {response.text[:100]}"
    except Exception as e:
        return False, str(e)

def main():
    print("🧪 QuetzalCore API Route Testing")
    print("=" * 70)
    
    # Test routes
    routes = [
        # Core
        ("GET", "/"),
        ("GET", "/api/health"),
        
        # GPU Operations
        ("GET", "/api/gpu/parallel/status"),
        ("POST", "/api/gpu/parallel/matmul", {"size": 128, "num_units": 2}),
        ("POST", "/api/gpu/parallel/conv2d", {"input_size": [64, 64], "kernel_size": [3, 3]}),
        
        # System
        ("GET", "/api/v1.2/network/status"),
        ("GET", "/api/v1.2/autoscaler/status"),
        
        # Metrics
        ("GET", "/api/problems/recent"),
        ("GET", "/api/analytics/performance"),
    ]
    
    print(f"\nTesting {len(routes)} routes...\n")
    
    passed = 0
    failed = 0
    
    for method, path, *data in routes:
        payload = data[0] if data else None
        success, result = test_route(method, path, payload)
        
        status = "✅" if success else "❌"
        print(f"{status} {method:6} {path:40} → {result}")
        
        if success:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✅ All routes working!")
    else:
        print(f"⚠️  {failed} routes have issues")
    
    return failed == 0

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted")
        exit(1)
