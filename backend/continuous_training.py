#!/usr/bin/env python3
"""
Continuous Autonomous Training System
Runs training loops, power tests, and benchmarks while you're away
"""
import requests
import time
import json
from datetime import datetime
import random
import sys

# CLOUD ONLY - No localhost!
BACKEND_URLS = [
    "https://hive-backend.onrender.com"
]

API_BASE = None

def find_backend():
    """Find available backend (handles cold starts)"""
    global API_BASE
    for url in BACKEND_URLS:
        print(f"🔍 Checking {url}...")
        # Try up to 3 times for cold starts (Render free tier)
        for attempt in range(3):
            try:
                print(f"   Attempt {attempt+1}/3...")
                response = requests.get(f"{url}/api/health", timeout=30)
                if response.status_code == 200:
                    API_BASE = url
                    print(f"✅ Connected to: {url}")
                    return True
                elif response.status_code == 404:
                    # Backend is up but endpoint might be different
                    print(f"   Backend responding, testing alternative endpoint...")
                    response = requests.get(url, timeout=10)
                    if response.status_code in [200, 404]:
                        API_BASE = url
                        print(f"✅ Connected to: {url} (backend is alive)")
                        return True
            except requests.Timeout:
                if attempt < 2:
                    print(f"   ⏳ Timeout, retrying... (cold start)")
                    time.sleep(10)
            except Exception as e:
                if attempt < 2:
                    print(f"   ⚠️ Error: {str(e)[:50]}, retrying...")
                    time.sleep(5)
    print("❌ No backend available")
    return False

def start_continuous_training():
    """Start continuous training loop"""
    try:
        response = requests.post(f"{API_BASE}/api/training/start", timeout=10)
        return response.status_code == 200
    except:
        return False

def get_training_status():
    """Get current training status"""
    try:
        response = requests.get(f"{API_BASE}/api/training/status", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def run_power_benchmark():
    """Run full power benchmark"""
    try:
        print("\n🏆 Running Power Benchmark...")
        response = requests.post(f"{API_BASE}/api/power/benchmark", timeout=60)
        if response.status_code == 200:
            data = response.json()
            print(f"  Overall Score: {data.get('overall_score', 0):.1f}/100")
            print(f"  Throughput: {data.get('throughput_ops_sec', 0)/1000000:.2f}M ops/sec")
            print(f"  Latency P95: {data.get('latency_p95_ms', 0):.2f}ms")
            return data
        return None
    except Exception as e:
        print(f"  ❌ Benchmark failed: {e}")
        return None

def run_stress_test(intensity="medium", duration=30):
    """Run stress test"""
    try:
        print(f"\n💪 Running {intensity.upper()} stress test ({duration}s)...")
        response = requests.post(
            f"{API_BASE}/api/power/stress-test",
            params={"intensity": intensity, "duration": duration},
            timeout=duration + 10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"  Peak Throughput: {data.get('peak_throughput', 0)/1000000:.2f}M ops/sec")
            print(f"  Stability: {data.get('stability_score', 0):.1f}%")
            return data
        return None
    except Exception as e:
        print(f"  ❌ Stress test failed: {e}")
        return None

def run_creative_scenario(mode=None):
    """Run creative training scenario"""
    try:
        mode_str = f" ({mode})" if mode else " (random)"
        print(f"\n🧠 Running Creative Scenario{mode_str}...")
        params = {"mode": mode} if mode else {}
        response = requests.post(
            f"{API_BASE}/api/training/creative",
            params=params,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"  Scenario: {data.get('name', 'Unknown')}")
            print(f"  Description: {data.get('description', 'N/A')}")
            objectives = data.get('objectives', [])
            if objectives:
                print(f"  Objectives:")
                for obj in objectives:
                    print(f"    • {obj}")
            return data
        return None
    except Exception as e:
        print(f"  ❌ Scenario failed: {e}")
        return None

def autonomous_training_loop(duration_minutes=60, benchmark_interval=10):
    """
    Run autonomous training loop
    
    Args:
        duration_minutes: How long to train (default: 60 min)
        benchmark_interval: Run benchmark every N minutes (default: 10)
    """
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║      QUEZTL AUTONOMOUS TRAINING SYSTEM - CONTINUOUS MODE       ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"\n⏱️  Duration: {duration_minutes} minutes")
    print(f"📊 Benchmark interval: {benchmark_interval} minutes")
    print(f"🚀 Start time: {datetime.now().strftime('%H:%M:%S')}\n")
    
    if not find_backend():
        print("❌ Cannot connect to backend. Exiting.")
        return
    
    # Start continuous training
    print("🎯 Starting continuous training...")
    if start_continuous_training():
        print("✅ Training started!\n")
    else:
        print("⚠️  Could not start training, but will continue with tests\n")
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    last_benchmark = start_time
    
    training_modes = ['chaos_monkey', 'resource_starving', 'cascade_failure', 
                     'traffic_spike', 'adaptive_adversary']
    stress_intensities = ['light', 'medium', 'heavy', 'extreme']
    
    iteration = 0
    
    try:
        while time.time() < end_time:
            iteration += 1
            elapsed = (time.time() - start_time) / 60
            remaining = (end_time - time.time()) / 60
            
            print("\n" + "="*70)
            print(f"📍 Iteration #{iteration} | Elapsed: {elapsed:.1f}min | Remaining: {remaining:.1f}min")
            print("="*70)
            
            # Check training status
            status = get_training_status()
            if status and status.get('is_training'):
                print(f"\n🎓 Training Status:")
                print(f"  Scenarios: {status.get('scenarios_completed', 0)}")
                print(f"  Success Rate: {status.get('average_success_rate', 0)*100:.1f}%")
                print(f"  Difficulty: {status.get('current_difficulty', 'unknown')}")
            
            # Run benchmark periodically
            if (time.time() - last_benchmark) / 60 >= benchmark_interval:
                run_power_benchmark()
                last_benchmark = time.time()
            
            # Random training activities
            activity = random.choice(['stress', 'creative', 'rest'])
            
            if activity == 'stress':
                intensity = random.choice(stress_intensities)
                duration = random.randint(15, 45)
                run_stress_test(intensity, duration)
                
            elif activity == 'creative':
                mode = random.choice(training_modes)
                run_creative_scenario(mode)
            
            else:
                print("\n💤 Rest period (30s)...")
                time.sleep(30)
            
            # Wait before next iteration
            wait_time = random.randint(30, 90)
            print(f"\n⏸️  Waiting {wait_time}s before next iteration...")
            time.sleep(wait_time)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user")
    
    # Final benchmark
    print("\n" + "="*70)
    print("🏁 FINAL BENCHMARK")
    print("="*70)
    run_power_benchmark()
    
    total_time = (time.time() - start_time) / 60
    print("\n" + "="*70)
    print("✅ TRAINING SESSION COMPLETE")
    print("="*70)
    print(f"⏱️  Total time: {total_time:.1f} minutes")
    print(f"🔄 Iterations: {iteration}")
    print(f"🎯 Backend: {API_BASE}")
    print(f"📅 End time: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    # Parse command line args
    duration = 60  # default 1 hour
    benchmark_interval = 10  # benchmark every 10 min
    
    if len(sys.argv) > 1:
        try:
            duration = int(sys.argv[1])
        except:
            pass
    
    if len(sys.argv) > 2:
        try:
            benchmark_interval = int(sys.argv[2])
        except:
            pass
    
    autonomous_training_loop(duration, benchmark_interval)
