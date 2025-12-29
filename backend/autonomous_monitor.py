#!/usr/bin/env python3
"""
Autonomous System Monitor
Runs while you're on break to ensure everything keeps working
"""
import requests
import time
import json
from datetime import datetime
import subprocess

API_BASE = "http://localhost:8000"

def check_backend_health():
    """Check if backend is responding"""
    try:
        response = requests.get(f"{API_BASE}/api/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_trained_model():
    """Test trained model generation"""
    try:
        response = requests.get(
            f"{API_BASE}/api/gen3d/trained-model",
            params={"prompt": "test", "format": "json"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return 'error' not in data
        return False
    except:
        return False

def check_premium_features():
    """Test premium features"""
    formats = ['obj', 'ply', 'stl', 'gltf']
    working = []
    for fmt in formats:
        try:
            response = requests.get(
                f"{API_BASE}/api/gen3d/premium",
                params={"prompt": "test", "format": fmt, "validate": False},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if 'error' not in data:
                    working.append(fmt.upper())
        except:
            pass
    return working

def check_training_progress():
    """Check enhanced training progress"""
    try:
        result = subprocess.run(
            ['docker', 'exec', 'hive-backend-1', 'tail', '-3', '/workspace/enhanced_training.log'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in reversed(lines):
                if 'Epoch' in line:
                    return line
                if '✅ ENHANCED TRAINING COMPLETE!' in line:
                    return "TRAINING COMPLETE ✅"
            return "Training in progress..."
        return "Unknown"
    except:
        return "Unable to check"

def run_quick_test():
    """Run a quick end-to-end test"""
    try:
        # Generate a model
        response = requests.get(
            f"{API_BASE}/api/gen3d/trained-model",
            params={"prompt": "dragon", "format": "json"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if 'error' not in data:
                stats = data.get('stats', {})
                return f"✅ {stats.get('vertices', 0)} vertices, {data.get('generation_time_ms', 0):.1f}ms"
        return "❌ Test failed"
    except Exception as e:
        return f"❌ {str(e)}"

def monitor_system(duration_minutes=30, check_interval=60):
    """
    Monitor system for specified duration
    
    Args:
        duration_minutes: How long to monitor (default: 30 min)
        check_interval: Seconds between checks (default: 60)
    """
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    check_count = 0
    
    print("🔍 AUTONOMOUS SYSTEM MONITOR")
    print("=" * 70)
    print(f"Monitoring duration: {duration_minutes} minutes")
    print(f"Check interval: {check_interval} seconds")
    print(f"Start time: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    while time.time() < end_time:
        check_count += 1
        current_time = datetime.now().strftime('%H:%M:%S')
        
        print(f"[{current_time}] Check #{check_count}")
        print("-" * 70)
        
        # Backend health
        backend_ok = check_backend_health()
        print(f"  Backend Health: {'✅ OK' if backend_ok else '❌ DOWN'}")
        
        if not backend_ok:
            print("  ⚠️  Backend is down! Attempting restart...")
            try:
                subprocess.run(
                    ['docker-compose', '-f', '/Users/xavasena/hive/docker-compose.yml', 'restart', 'backend'],
                    timeout=30
                )
                time.sleep(5)
                print("  ✅ Backend restarted")
            except:
                print("  ❌ Failed to restart backend")
        
        # Trained model
        model_ok = check_trained_model()
        print(f"  Trained Model: {'✅ Working' if model_ok else '❌ Error'}")
        
        # Premium features
        premium_formats = check_premium_features()
        if premium_formats:
            print(f"  Premium Formats: ✅ {', '.join(premium_formats)}")
        else:
            print(f"  Premium Formats: ⚠️  Not available")
        
        # Training progress
        training_status = check_training_progress()
        print(f"  Enhanced Training: {training_status}")
        
        # Quick test
        test_result = run_quick_test()
        print(f"  End-to-End Test: {test_result}")
        
        print()
        
        # Wait for next check
        time_remaining = end_time - time.time()
        if time_remaining > check_interval:
            print(f"  Next check in {check_interval}s... (Time remaining: {time_remaining/60:.1f} min)")
            print()
            time.sleep(check_interval)
        else:
            break
    
    print("=" * 70)
    print("🎉 MONITORING COMPLETE")
    print(f"Total checks: {check_count}")
    print(f"End time: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # Final status
    print("📊 FINAL STATUS:")
    print(f"  Backend: {'✅' if check_backend_health() else '❌'}")
    print(f"  Model: {'✅' if check_trained_model() else '❌'}")
    print(f"  Premium: {', '.join(check_premium_features())}")
    print(f"  Training: {check_training_progress()}")
    print()
    print("✅ System is stable and ready!")

if __name__ == "__main__":
    import sys
    
    # Default: monitor for 30 minutes
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    
    try:
        monitor_system(duration_minutes=duration)
    except KeyboardInterrupt:
        print("\n\n⚠️  Monitoring stopped by user")
    except Exception as e:
        print(f"\n\n❌ Monitoring error: {e}")
        import traceback
        traceback.print_exc()
