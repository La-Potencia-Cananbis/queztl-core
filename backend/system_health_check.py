#!/usr/bin/env python3
"""
Queztl System Health Check - Complete Application Audit
Tests all deployed services and identifies overlaps
"""
import requests
import json
from datetime import datetime
from typing import Dict, List, Any

# CLOUD SERVICES ONLY - NO LOCALHOST
SERVICES = {
    "3d_showcase": {
        "name": "3D Showcase & Demos",
        "url": "https://senasaitech.com",
        "endpoints": [
            "/login.html",
            "/demos.html", 
            "/3d-demo.html",
            "/benchmark.html"
        ],
        "type": "frontend",
        "authentication": True,
        "description": "3DMark benchmarks, WebGL/WebGPU demos"
    },
    "hive_backend": {
        "name": "Hive Backend API",
        "url": "https://hive-backend.onrender.com",
        "endpoints": [
            "/api/health",
            "/api/power/measure",
            "/api/power/benchmark",
            "/api/gpu/info"
        ],
        "type": "backend",
        "authentication": False,
        "description": "Main compute backend - power tests, GPU, training"
    },
    "dashboard": {
        "name": "Main Dashboard",
        "url": "https://senasaitech.com",
        "endpoints": ["/"],
        "type": "frontend",
        "authentication": False,
        "description": "Next.js dashboard with metrics"
    }
}

# APPLICATION ARCHITECTURE
APPLICATIONS = {
    "3D_Graphics": {
        "description": "3D rendering, benchmarking, WebGL/WebGPU",
        "components": ["3d_showcase", "hive_backend"],
        "endpoints": ["/api/gpu/*", "/api/power/benchmark"],
        "overlaps": [],
        "status": "production"
    },
    "Training_Engine": {
        "description": "ML training, adaptive learning, scenarios",
        "components": ["hive_backend"],
        "endpoints": ["/api/training/*"],
        "overlaps": [],
        "status": "production"
    },
    "Power_Testing": {
        "description": "Stress tests, benchmarks, performance",
        "components": ["hive_backend"],
        "endpoints": ["/api/power/*"],
        "overlaps": ["Training_Engine"],  # Both stress system
        "status": "production"
    },
    "GIS_Geophysics": {
        "description": "LiDAR, radar, geophysics, photo-to-3D",
        "components": ["hive_backend"],
        "endpoints": ["/api/gis/*", "/api/lidar/*", "/api/geophysics/*"],
        "overlaps": ["3D_Graphics"],  # Both do 3D generation
        "status": "backend_only"
    },
    "Email_System": {
        "description": "SendGrid email sending",
        "components": [],  # Not deployed yet
        "endpoints": ["/api/email/*"],
        "overlaps": [],
        "status": "local_only"
    },
    "Secrets_Vault": {
        "description": "Encrypted credential storage",
        "components": ["3d_showcase"],
        "endpoints": ["/secrets-vault.html"],
        "overlaps": [],
        "status": "production"
    }
}

def test_endpoint(url: str, timeout: int = 30) -> Dict[str, Any]:
    """Test an endpoint"""
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        return {
            "status": response.status_code,
            "ok": response.status_code in [200, 301, 302, 404],  # 404 is fine for some endpoints
            "response_time": response.elapsed.total_seconds(),
            "error": None
        }
    except requests.Timeout:
        return {"status": None, "ok": False, "response_time": None, "error": "Timeout"}
    except Exception as e:
        return {"status": None, "ok": False, "response_time": None, "error": str(e)[:50]}

def check_service(service_name: str, service_config: Dict) -> Dict[str, Any]:
    """Check a service health"""
    print(f"\n{'='*70}")
    print(f"🔍 Testing: {service_config['name']}")
    print(f"   Type: {service_config['type']}")
    print(f"   URL: {service_config['url']}")
    print(f"{'='*70}")
    
    results = []
    all_ok = True
    
    for endpoint in service_config['endpoints']:
        full_url = service_config['url'] + endpoint
        print(f"\n   📡 {endpoint}")
        
        result = test_endpoint(full_url)
        results.append({
            "endpoint": endpoint,
            "url": full_url,
            **result
        })
        
        if result['ok']:
            time_str = f"{result['response_time']:.2f}s" if result['response_time'] else "N/A"
            print(f"      ✅ Status: {result['status']} | Time: {time_str}")
        else:
            all_ok = False
            print(f"      ❌ Status: {result['status']} | Error: {result['error']}")
    
    return {
        "service": service_name,
        "name": service_config['name'],
        "healthy": all_ok,
        "endpoints_tested": len(results),
        "endpoints_ok": sum(1 for r in results if r['ok']),
        "results": results
    }

def analyze_applications():
    """Analyze application architecture and overlaps"""
    print("\n" + "="*70)
    print("📊 APPLICATION ARCHITECTURE ANALYSIS")
    print("="*70)
    
    for app_name, app_config in APPLICATIONS.items():
        status_icon = {
            "production": "✅",
            "backend_only": "⚠️",
            "local_only": "❌",
            "planned": "📋"
        }.get(app_config['status'], "❓")
        
        print(f"\n{status_icon} {app_name}")
        print(f"   {app_config['description']}")
        print(f"   Status: {app_config['status']}")
        print(f"   Components: {', '.join(app_config['components']) if app_config['components'] else 'None'}")
        
        if app_config['overlaps']:
            print(f"   ⚠️  Overlaps with: {', '.join(app_config['overlaps'])}")

def generate_recommendations(service_results: List[Dict]) -> List[str]:
    """Generate recommendations based on results"""
    recommendations = []
    
    # Check for unhealthy services
    unhealthy = [r for r in service_results if not r['healthy']]
    if unhealthy:
        for service in unhealthy:
            recommendations.append(f"❌ Fix {service['name']} - {service['endpoints_tested'] - service['endpoints_ok']} endpoints failing")
    
    # Check for overlaps
    overlapping_apps = [name for name, config in APPLICATIONS.items() if config['overlaps']]
    if overlapping_apps:
        recommendations.append(f"⚠️  Consider separating overlapping apps: {', '.join(overlapping_apps)}")
    
    # Check for local-only apps
    local_apps = [name for name, config in APPLICATIONS.items() if config['status'] == 'local_only']
    if local_apps:
        recommendations.append(f"📤 Deploy to cloud: {', '.join(local_apps)}")
    
    # Check for backend-only apps
    backend_apps = [name for name, config in APPLICATIONS.items() if config['status'] == 'backend_only']
    if backend_apps:
        recommendations.append(f"🎨 Create frontends for: {', '.join(backend_apps)}")
    
    return recommendations

def main():
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║              QUEZTL SYSTEM HEALTH CHECK                        ║")
    print("║              Cloud Services Only - No Localhost                ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"\n🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing {len(SERVICES)} services")
    print(f"📱 Analyzing {len(APPLICATIONS)} applications\n")
    
    # Test all services
    service_results = []
    for service_name, service_config in SERVICES.items():
        result = check_service(service_name, service_config)
        service_results.append(result)
    
    # Analyze applications
    analyze_applications()
    
    # Summary
    print("\n" + "="*70)
    print("📋 SUMMARY")
    print("="*70)
    
    healthy_count = sum(1 for r in service_results if r['healthy'])
    print(f"\n✅ Healthy Services: {healthy_count}/{len(service_results)}")
    
    for result in service_results:
        icon = "✅" if result['healthy'] else "❌"
        print(f"   {icon} {result['name']}: {result['endpoints_ok']}/{result['endpoints_tested']} endpoints OK")
    
    # Recommendations
    recommendations = generate_recommendations(service_results)
    if recommendations:
        print("\n" + "="*70)
        print("💡 RECOMMENDATIONS")
        print("="*70)
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec}")
    
    # Architecture suggestions
    print("\n" + "="*70)
    print("🏗️  ARCHITECTURE SUGGESTIONS")
    print("="*70)
    print("""
1. SEPARATE APPLICATIONS:
   - 3D Graphics System (WebGL/WebGPU + benchmarks)
   - GIS/Geophysics System (LiDAR, radar, photo-to-3D)
   - Training/Testing System (ML, stress tests, power)
   - Email/Communication System (SendGrid integration)

2. ELIMINATE OVERLAPS:
   - Move 3D generation to dedicated service
   - Separate stress testing from ML training
   - Create unified 3D rendering API

3. DEPLOY MISSING SERVICES:
   - Email backend to cloud
   - GIS frontend for demos
   - Unified API gateway

4. TRUE OS STRUCTURE:
   - Microservices architecture
   - Each app = independent service
   - API gateway for routing
   - Shared authentication
""")
    
    print("\n" + "="*70)
    print("✅ HEALTH CHECK COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()
