#!/usr/bin/env python3
"""
🚀 AUTONOMOUS 5X TESTER
Stress test everything and identify improvements
"""

import asyncio
import json
import time
import requests
import random
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
from concurrent import futures
import subprocess

class Autonomous5XTester:
    """Test everything at 5x scale and identify bottlenecks"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "bottlenecks": [],
            "improvements": [],
            "master_plan_progress": {}
        }
        
    def log(self, msg: str, emoji: str = "🔍"):
        print(f"{emoji} {msg}")
        
    def test_endpoint(self, method: str, endpoint: str, data: dict = None, 
                     iterations: int = 5) -> Dict[str, Any]:
        """Test an endpoint multiple times"""
        self.log(f"Testing {method} {endpoint} ({iterations}x)", "🧪")
        
        times = []
        errors = []
        
        for i in range(iterations):
            start = time.time()
            try:
                if method == "GET":
                    resp = requests.get(f"{self.base_url}{endpoint}", timeout=30)
                else:
                    resp = requests.post(f"{self.base_url}{endpoint}", json=data, timeout=30)
                
                elapsed = time.time() - start
                times.append(elapsed)
                
                if resp.status_code != 200:
                    errors.append(f"Status {resp.status_code}")
                    
            except Exception as e:
                elapsed = time.time() - start
                times.append(elapsed)
                errors.append(str(e))
        
        avg_time = sum(times) / len(times) if times else 0
        success_rate = (iterations - len(errors)) / iterations * 100
        
        result = {
            "endpoint": endpoint,
            "method": method,
            "iterations": iterations,
            "avg_time": round(avg_time, 3),
            "min_time": round(min(times), 3) if times else 0,
            "max_time": round(max(times), 3) if times else 0,
            "success_rate": round(success_rate, 1),
            "errors": errors[:3]  # First 3 errors
        }
        
        # Identify bottlenecks
        if avg_time > 5.0:
            self.results["bottlenecks"].append({
                "endpoint": endpoint,
                "issue": "Slow response",
                "avg_time": avg_time,
                "recommendation": "Add caching or optimize computation"
            })
        
        if success_rate < 100:
            self.results["bottlenecks"].append({
                "endpoint": endpoint,
                "issue": "Reliability",
                "success_rate": success_rate,
                "recommendation": "Add error handling and retries"
            })
        
        self.results["tests"].append(result)
        return result
    
    def test_concurrent_load(self, endpoint: str, concurrent: int = 10) -> Dict[str, Any]:
        """Test concurrent requests"""
        self.log(f"Testing {endpoint} with {concurrent} concurrent requests", "⚡")
        
        def make_request():
            try:
                start = time.time()
                resp = requests.get(f"{self.base_url}{endpoint}", timeout=30)
                elapsed = time.time() - start
                return {"success": resp.status_code == 200, "time": elapsed}
            except Exception as e:
                return {"success": False, "time": 0, "error": str(e)}
        
        start_all = time.time()
        with futures.ThreadPoolExecutor(max_workers=concurrent) as executor:
            results = list(executor.map(lambda _: make_request(), range(concurrent)))
        total_time = time.time() - start_all
        
        successes = sum(1 for r in results if r["success"])
        avg_time = sum(r["time"] for r in results if r["success"]) / successes if successes > 0 else 0
        
        result = {
            "endpoint": endpoint,
            "concurrent_requests": concurrent,
            "total_time": round(total_time, 3),
            "success_rate": round(successes / concurrent * 100, 1),
            "avg_response_time": round(avg_time, 3),
            "requests_per_sec": round(concurrent / total_time, 2)
        }
        
        if result["success_rate"] < 80:
            self.results["bottlenecks"].append({
                "endpoint": endpoint,
                "issue": "Poor concurrency handling",
                "success_rate": result["success_rate"],
                "recommendation": "Implement connection pooling and async processing"
            })
        
        return result
    
    def test_mining_apis(self):
        """Test all mining endpoints at scale"""
        self.log("TESTING MINING APIS AT 5X SCALE", "⛏️")
        
        # Test cost endpoint (lightweight)
        self.test_endpoint("GET", "/api/mining/survey-cost?area_km2=50", iterations=10)
        
        # Test capabilities
        self.test_endpoint("GET", "/api/gen3d/capabilities", iterations=5)
        
        # Test concurrent load
        self.test_concurrent_load("/api/mining/survey-cost?area_km2=10", concurrent=20)
        
        # Test MAG survey upload (heavier)
        mag_data = {
            "survey_name": "stress_test",
            "data": [
                {"x": i*10, "y": j*10, "magnetic_field": 45000 + random.randint(-1000, 1000)}
                for i in range(20) for j in range(20)
            ]
        }
        self.test_endpoint("POST", "/api/mining/mag-survey", mag_data, iterations=3)
        
        # Test discrimination (heavy computation)
        self.test_endpoint("POST", "/api/mining/discriminate", mag_data, iterations=3)
    
    def test_gis_apis(self):
        """Test GIS endpoints"""
        self.log("TESTING GIS APIS", "🗺️")
        
        # Test geophysics calculations
        self.test_endpoint("POST", "/api/geophysics/magnetic-field", {
            "latitude": 37.7749,
            "longitude": -122.4194,
            "altitude": 0,
            "date": "2024-01-01"
        }, iterations=5)
        
        self.test_concurrent_load("/api/health", concurrent=50)
    
    def test_distributed_network(self):
        """Test distributed network performance"""
        self.log("TESTING DISTRIBUTED NETWORK", "🌐")
        
        try:
            resp = requests.get(f"{self.base_url}/api/v1.2/network/status", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                
                nodes = data.get("registry", {})
                active_nodes = sum(1 for n in nodes.values() if n.get("status") == "active")
                
                self.results["master_plan_progress"]["distributed_network"] = {
                    "status": "operational",
                    "active_nodes": active_nodes,
                    "total_capacity": data.get("capacity", {})
                }
                
                if active_nodes < 2:
                    self.results["improvements"].append({
                        "area": "Distributed Network",
                        "issue": "Only 1 node active",
                        "recommendation": "Deploy RGIS workers to scale training capacity",
                        "priority": "HIGH"
                    })
            else:
                self.results["improvements"].append({
                    "area": "Distributed Network",
                    "issue": "Network coordinator not responding",
                    "recommendation": "Check if backend is running",
                    "priority": "CRITICAL"
                })
        except Exception as e:
            self.results["improvements"].append({
                "area": "Distributed Network",
                "issue": f"Connection failed: {e}",
                "recommendation": "Start backend or check network configuration",
                "priority": "CRITICAL"
            })
    
    def check_master_plan_progress(self):
        """Check progress on master plan items"""
        self.log("CHECKING MASTER PLAN PROGRESS", "📋")
        
        # Read TODO list
        todo_file = Path(__file__).parent / "TODO.md"
        if todo_file.exists():
            content = todo_file.read_text()
            
            completed = content.count("[x]")
            total = content.count("- [")
            
            self.results["master_plan_progress"]["todo_completion"] = {
                "completed": completed,
                "total": total,
                "percentage": round(completed / total * 100, 1) if total > 0 else 0
            }
        
        # Check for missing features
        missing_features = []
        
        # Check if mining dashboard exists
        if not (Path(__file__).parent / "frontend" / "mining-dashboard").exists():
            missing_features.append({
                "feature": "Mining Dashboard Visualization",
                "status": "not_started",
                "priority": "MEDIUM",
                "recommendation": "Create interactive mining dashboard with Recharts"
            })
        
        # Check if deployment to production is done
        try:
            resp = requests.get("https://api.senasaitech.com/api/health", timeout=5)
            if resp.status_code == 200:
                self.results["master_plan_progress"]["production_deployment"] = "completed"
            else:
                missing_features.append({
                    "feature": "Production Deployment",
                    "status": "partial",
                    "priority": "HIGH",
                    "recommendation": "Complete senasaitech.com deployment with SSL"
                })
        except:
            missing_features.append({
                "feature": "Production Deployment",
                "status": "not_started",
                "priority": "HIGH",
                "recommendation": "Run deploy-to-senasaitech.sh with SERVER_IP set"
            })
        
        self.results["improvements"].extend(missing_features)
    
    def suggest_optimizations(self):
        """AI-driven optimization suggestions"""
        self.log("ANALYZING FOR OPTIMIZATIONS", "🧠")
        
        # Check response times
        slow_endpoints = [t for t in self.results["tests"] if t.get("avg_time", 0) > 2.0]
        
        if slow_endpoints:
            self.results["improvements"].append({
                "area": "Performance",
                "issue": f"{len(slow_endpoints)} slow endpoints detected",
                "endpoints": [e["endpoint"] for e in slow_endpoints],
                "recommendation": "Implement Redis caching for frequently accessed data",
                "priority": "MEDIUM",
                "code_snippet": """
# Add to backend/main.py
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/api/mining/survey-cost")
async def cached_survey_cost(area_km2: float):
    cache_key = f"cost:{area_km2}"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    result = calculate_survey_cost(area_km2)
    redis_client.setex(cache_key, 3600, json.dumps(result))
    return result
"""
            })
        
        # Check concurrent performance
        if any(t.get("requests_per_sec", 0) < 10 for t in self.results["tests"]):
            self.results["improvements"].append({
                "area": "Concurrency",
                "issue": "Low throughput under concurrent load",
                "recommendation": "Increase Uvicorn workers and add async endpoints",
                "priority": "MEDIUM",
                "code_snippet": """
# In systemd service:
ExecStart=/opt/quetzalcore/venv/bin/uvicorn backend.main:app \\
    --host 0.0.0.0 --port 8000 \\
    --workers 8 \\  # Increase workers
    --loop uvloop \\  # Use faster event loop
    --ws websockets
"""
            })
        
        # Check error rates
        failing_tests = [t for t in self.results["tests"] if t.get("success_rate", 100) < 100]
        if failing_tests:
            self.results["improvements"].append({
                "area": "Reliability",
                "issue": f"{len(failing_tests)} endpoints with failures",
                "recommendation": "Add comprehensive error handling and retries",
                "priority": "HIGH"
            })
    
    def generate_report(self):
        """Generate comprehensive report"""
        self.log("GENERATING REPORT", "📊")
        
        report_file = Path(__file__).parent / f"5X_TEST_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.write_text(json.dumps(self.results, indent=2))
        
        markdown_file = report_file.with_suffix(".md")
        
        md_content = f"""# 🚀 5X TEST REPORT
Generated: {self.results['timestamp']}

## 📊 Test Results Summary

Total Tests: {len(self.results['tests'])}
Bottlenecks Found: {len(self.results['bottlenecks'])}
Improvements Suggested: {len(self.results['improvements'])}

## 🧪 Endpoint Performance

| Endpoint | Avg Time | Success Rate | Requests/Sec |
|----------|----------|--------------|--------------|
"""
        
        for test in self.results['tests']:
            md_content += f"| {test['endpoint']} | {test.get('avg_time', 'N/A')}s | {test.get('success_rate', 'N/A')}% | {test.get('requests_per_sec', 'N/A')} |\n"
        
        md_content += "\n## 🚨 Bottlenecks Identified\n\n"
        for i, bottleneck in enumerate(self.results['bottlenecks'], 1):
            md_content += f"{i}. **{bottleneck['endpoint']}**\n"
            md_content += f"   - Issue: {bottleneck['issue']}\n"
            md_content += f"   - Recommendation: {bottleneck['recommendation']}\n\n"
        
        md_content += "## 💡 Improvement Suggestions\n\n"
        for i, improvement in enumerate(self.results['improvements'], 1):
            md_content += f"{i}. **{improvement.get('area', 'General')}** (Priority: {improvement.get('priority', 'MEDIUM')})\n"
            md_content += f"   - Issue: {improvement.get('issue', 'N/A')}\n"
            md_content += f"   - Recommendation: {improvement['recommendation']}\n"
            if 'code_snippet' in improvement:
                md_content += f"   ```python\n{improvement['code_snippet']}\n   ```\n"
            md_content += "\n"
        
        md_content += "## 📋 Master Plan Progress\n\n"
        progress = self.results['master_plan_progress']
        if 'todo_completion' in progress:
            todo = progress['todo_completion']
            md_content += f"- TODO List: {todo['completed']}/{todo['total']} items ({todo['percentage']}%)\n"
        
        if 'distributed_network' in progress:
            network = progress['distributed_network']
            md_content += f"- Distributed Network: {network['status']} ({network['active_nodes']} nodes)\n"
        
        if 'production_deployment' in progress:
            md_content += f"- Production Deployment: {progress['production_deployment']}\n"
        
        md_content += "\n## 🎯 Next Actions\n\n"
        
        high_priority = [i for i in self.results['improvements'] if i.get('priority') == 'HIGH' or i.get('priority') == 'CRITICAL']
        
        for i, action in enumerate(high_priority[:5], 1):
            md_content += f"{i}. {action['recommendation']}\n"
        
        md_content += "\n---\n*Generated by Autonomous 5X Tester*\n"
        
        markdown_file.write_text(md_content)
        
        self.log(f"Report saved to {markdown_file}", "✅")
        
        # Print summary
        print("\n" + "="*60)
        print("🎯 5X TEST SUMMARY")
        print("="*60)
        print(f"Tests Run: {len(self.results['tests'])}")
        print(f"Bottlenecks: {len(self.results['bottlenecks'])}")
        print(f"Improvements: {len(self.results['improvements'])}")
        print(f"\n📄 Full report: {markdown_file}")
        print("="*60 + "\n")
    
    async def run_all_tests(self):
        """Run all tests"""
        self.log("STARTING 5X TEST SUITE", "🚀")
        
        # Check if backend is running
        try:
            resp = requests.get(f"{self.base_url}/api/health", timeout=5)
            if resp.status_code != 200:
                self.log("Backend not responding! Start it first.", "❌")
                return
        except Exception as e:
            self.log(f"Cannot connect to backend: {e}", "❌")
            self.log("Run: cd backend && uvicorn main:app", "💡")
            return
        
        # Run test suites
        self.test_mining_apis()
        self.test_gis_apis()
        self.test_distributed_network()
        self.check_master_plan_progress()
        self.suggest_optimizations()
        
        # Generate report
        self.generate_report()

def main():
    import sys
    
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    tester = Autonomous5XTester(base_url)
    asyncio.run(tester.run_all_tests())

if __name__ == "__main__":
    main()
