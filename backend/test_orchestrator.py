#!/usr/bin/env python3
"""
Test QuetzalCore Orchestrator - Auto-scaling VM manager
"""

import asyncio
import sys
from backend.quetzalcore_orchestrator import (
    QuetzalCoreOrchestrator, 
    WorkloadRequest,
    VMSize
)


async def test_basic_workloads():
    """Test basic workload execution"""
    print("🧪 TEST 1: Basic Workload Execution")
    print("="*60)
    
    orchestrator = QuetzalCoreOrchestrator(max_vms=10, enable_super_vms=True)
    
    # Small API workload
    workload = WorkloadRequest(
        workload_id="test_api_1",
        workload_type="api",
        priority=5,
        estimated_duration=10,
        data={"test": "data"}
    )
    
    result = await orchestrator.execute_workload(workload)
    print(f"✅ API workload completed: {result}")
    print()


async def test_super_vm():
    """Test Super VM for mining workload"""
    print("🧪 TEST 2: Super VM Mining Workload")
    print("="*60)
    
    orchestrator = QuetzalCoreOrchestrator(max_vms=5, enable_super_vms=True)
    
    # Heavy mining workload
    workload = WorkloadRequest(
        workload_id="mining_super_1",
        workload_type="mining",
        priority=10,
        estimated_duration=600,
        data={
            "mag_readings": list(range(10000)),
            "survey_area": "test_site_1"
        }
    )
    
    print(f"Requesting Super VM for mining analysis...")
    result = await orchestrator.execute_workload(workload)
    print(f"✅ Mining workload completed:")
    print(f"   Anomalies detected: {result.get('anomalies_detected', 0)}")
    print(f"   Mineral signatures: {result.get('mineral_signatures', {})}")
    print()


async def test_concurrent_workloads():
    """Test concurrent execution of multiple workloads"""
    print("🧪 TEST 3: Concurrent Workload Execution")
    print("="*60)
    
    orchestrator = QuetzalCoreOrchestrator(max_vms=20, enable_super_vms=True)
    
    workloads = [
        WorkloadRequest(f"api_{i}", "api", priority=3, estimated_duration=5)
        for i in range(5)
    ] + [
        WorkloadRequest(f"mining_{i}", "mining", priority=10, estimated_duration=300,
                       data={"mag_readings": list(range(1000))})
        for i in range(2)
    ] + [
        WorkloadRequest(f"3d_{i}", "3d_gen", priority=7, estimated_duration=200)
        for i in range(3)
    ]
    
    print(f"Executing {len(workloads)} concurrent workloads...")
    
    # Execute all concurrently
    results = await asyncio.gather(
        *[orchestrator.execute_workload(w) for w in workloads],
        return_exceptions=True
    )
    
    success_count = sum(1 for r in results if not isinstance(r, Exception))
    print(f"✅ Completed: {success_count}/{len(workloads)} workloads")
    print()
    
    # Show cluster status
    status = orchestrator.get_cluster_status()
    print("\n📊 CLUSTER STATUS:")
    print(f"   Active VMs: {status['vms']['active']}")
    print(f"   Pooled VMs: {status['vms']['pooled']}")
    print(f"   VM Breakdown: {status['vms']['breakdown']}")
    print(f"   CPU Usage: {status['resources']['cpu_usage_percent']:.1f}%")
    print(f"   Memory Used: {status['resources']['memory_used_mb']}MB")
    print()


async def test_auto_scaling():
    """Test auto-scaling behavior"""
    print("🧪 TEST 4: Auto-Scaling")
    print("="*60)
    
    orchestrator = QuetzalCoreOrchestrator(max_vms=15, enable_super_vms=True)
    
    print("Phase 1: Light load (5 small workloads)")
    light_workloads = [
        WorkloadRequest(f"light_{i}", "api", priority=3, estimated_duration=5)
        for i in range(5)
    ]
    await asyncio.gather(*[orchestrator.execute_workload(w) for w in light_workloads])
    
    status1 = orchestrator.get_cluster_status()
    print(f"   VMs after light load: {status1['vms']['total']}")
    
    print("\nPhase 2: Heavy load (10 mining workloads)")
    heavy_workloads = [
        WorkloadRequest(f"heavy_{i}", "mining", priority=10, estimated_duration=300,
                       data={"mag_readings": list(range(5000))})
        for i in range(10)
    ]
    await asyncio.gather(*[orchestrator.execute_workload(w) for w in heavy_workloads])
    
    status2 = orchestrator.get_cluster_status()
    print(f"   VMs after heavy load: {status2['vms']['total']}")
    
    print("\n✅ Auto-scaling test completed")
    print(f"   VM growth: {status1['vms']['total']} → {status2['vms']['total']}")
    print()


async def test_vm_size_detection():
    """Test automatic VM size detection"""
    print("🧪 TEST 5: VM Size Auto-Detection")
    print("="*60)
    
    orchestrator = QuetzalCoreOrchestrator(max_vms=10, enable_super_vms=True)
    
    test_cases = [
        ("api", None, VMSize.SMALL),
        ("mining", None, VMSize.SUPER),
        ("3d_gen", None, VMSize.XLARGE),
        ("ml_training", None, VMSize.SUPER),
        ("geophysics", None, VMSize.LARGE),
    ]
    
    for workload_type, required_size, expected_size in test_cases:
        workload = WorkloadRequest(
            workload_id=f"detect_{workload_type}",
            workload_type=workload_type,
            required_size=required_size,
            data={"test": "data"}
        )
        
        detected = orchestrator.detect_workload_size(workload)
        status = "✅" if detected == expected_size else "❌"
        print(f"{status} {workload_type:15} → {detected.value:10} (expected: {expected_size.value})")
    
    print()


async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🦅 QUETZALCORE ORCHESTRATOR TEST SUITE")
    print("="*60 + "\n")
    
    tests = [
        ("Basic Workloads", test_basic_workloads),
        ("Super VM", test_super_vm),
        ("Concurrent Workloads", test_concurrent_workloads),
        ("Auto-Scaling", test_auto_scaling),
        ("VM Size Detection", test_vm_size_detection),
    ]
    
    for name, test_func in tests:
        try:
            await test_func()
        except Exception as e:
            print(f"❌ {name} failed: {e}\n")
            import traceback
            traceback.print_exc()
    
    print("="*60)
    print("✅ TEST SUITE COMPLETE")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
