#!/usr/bin/env python3
"""
Test Mining Magnetometry API Endpoints
Quick validation script for new mining features
"""

import requests
import json
import numpy as np

BASE_URL = "http://localhost:8000"

def test_capabilities():
    """Test that mining capabilities are exposed"""
    print("\n🔍 Testing Capabilities Endpoint...")
    response = requests.get(f"{BASE_URL}/api/gen3d/capabilities")
    
    if response.status_code == 200:
        caps = response.json()
        if 'mining_magnetometry' in caps:
            print("✅ Mining capabilities found:")
            print(json.dumps(caps['mining_magnetometry'], indent=2))
            return True
        else:
            print("❌ Mining capabilities not found")
            return False
    else:
        print(f"❌ Failed: {response.status_code}")
        return False

def test_discriminate():
    """Test mineral discrimination endpoint"""
    print("\n🔬 Testing Mineral Discrimination...")
    
    # Create synthetic MAG data
    # Strong iron anomaly in center
    locations = []
    magnetic_data = []
    
    for x in range(-5, 6):
        for y in range(-5, 6):
            locations.append([x * 100, y * 100, 0])  # Grid spacing 100m
            
            # Distance from center
            dist = np.sqrt(x**2 + y**2)
            
            # Magnetic anomaly (iron-like signature)
            if dist < 2:
                anomaly = 800 - dist * 100  # Strong central anomaly
            elif dist < 4:
                anomaly = 200 - dist * 20   # Moderate halo
            else:
                anomaly = 50 + np.random.randn() * 10  # Background noise
            
            magnetic_data.append(anomaly)
    
    payload = {
        "magnetic_data": magnetic_data,
        "locations": locations,
        "target_minerals": ["iron", "copper"]
    }
    
    response = requests.post(
        f"{BASE_URL}/api/mining/discriminate",
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Discrimination successful:")
        print(f"   Num stations: {result['num_stations']}")
        
        targets = result['discrimination_results'].get('targets', [])
        print(f"   Mineral targets found: {len(targets)}")
        
        for target in targets:
            print(f"   - {target['mineral_type']}: {target['confidence']} confidence, "
                  f"{target['num_targets']} locations")
        
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return False

def test_drill_targets():
    """Test drill target recommendation"""
    print("\n🎯 Testing Drill Target Recommendation...")
    
    # Create synthetic data with 2 strong anomalies
    locations = []
    magnetic_data = []
    
    # Anomaly 1: Iron deposit at (0, 0)
    for x in range(-10, 11):
        for y in range(-10, 11):
            locations.append([x * 50, y * 50, 0])
            
            # Distance from (0, 0)
            dist1 = np.sqrt(x**2 + y**2)
            anomaly1 = 1000 * np.exp(-(dist1**2) / 16) if dist1 < 5 else 0
            
            # Distance from (5, 5) - secondary target
            dist2 = np.sqrt((x-5)**2 + (y-5)**2)
            anomaly2 = 400 * np.exp(-(dist2**2) / 9) if dist2 < 4 else 0
            
            # Background + noise
            total = 50 + anomaly1 + anomaly2 + np.random.randn() * 10
            magnetic_data.append(total)
    
    payload = {
        "magnetic_data": magnetic_data,
        "locations": locations,
        "min_anomaly": 100.0,
        "top_n": 5
    }
    
    response = requests.post(
        f"{BASE_URL}/api/mining/target-drills",
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Drill targeting successful:")
        print(f"   Total stations: {result['parameters']['num_stations']}")
        print(f"   Min anomaly threshold: {result['parameters']['min_anomaly_nt']} nT")
        
        targets = result['drill_targets']
        print(f"\n   🎯 Top {len(targets)} drill targets:")
        for i, target in enumerate(targets, 1):
            print(f"   {i}. {target['mineral_type']}")
            print(f"      Location: {target['location'][:2]}")
            print(f"      Anomaly: {target['anomaly_nT']:.1f} nT")
            print(f"      Priority: {target['priority']}, Confidence: {target['confidence']}")
        
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return False

def test_cost_analysis():
    """Test survey cost analysis"""
    print("\n💰 Testing Cost Analysis...")
    
    params = {
        "area_km2": 10.0,
        "line_spacing_m": 100.0,
        "station_spacing_m": 25.0,
        "cost_per_station": 50.0,
        "cost_per_drill": 100000.0
    }
    
    response = requests.get(
        f"{BASE_URL}/api/mining/survey-cost",
        params=params
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Cost analysis successful:")
        
        design = result['survey_design']
        print(f"\n   📊 Survey Design:")
        print(f"   Area: {design['area_km2']} km²")
        print(f"   Total stations: {design['total_stations']}")
        print(f"   Line spacing: {design['line_spacing_m']} m")
        
        costs = result['cost_analysis']
        print(f"\n   💵 Cost Analysis:")
        print(f"   MAG survey: ${costs['mag_survey_cost_usd']:,.0f}")
        print(f"   Blind drilling: ${costs['blind_drilling_cost_usd']:,.0f}")
        print(f"   MAG + Targeted drilling: ${costs['total_cost_with_mag_usd']:,.0f}")
        print(f"   Savings: ${costs['savings_usd']:,.0f}")
        print(f"   ROI: {costs['roi_percent']:.0f}%")
        
        rec = result['recommendations']
        print(f"\n   📋 Recommendation: {rec['optimal_strategy']}")
        print(f"   Confidence: {rec['confidence']}")
        
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return False

def main():
    print("=" * 70)
    print("🧲 MINING MAGNETOMETRY API TEST SUITE")
    print("=" * 70)
    
    # Check if backend is running
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=2)
        if response.status_code != 200:
            print("❌ Backend not responding. Start it with: .venv/bin/python -m backend.main")
            return
    except:
        print("❌ Backend not running on port 8000")
        print("Start it with: .venv/bin/python -m backend.main")
        return
    
    print("✅ Backend is running\n")
    
    # Run tests
    results = []
    results.append(("Capabilities", test_capabilities()))
    results.append(("Mineral Discrimination", test_discriminate()))
    results.append(("Drill Targets", test_drill_targets()))
    results.append(("Cost Analysis", test_cost_analysis()))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Mining API is ready for your project!")
    else:
        print("\n⚠️ Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
