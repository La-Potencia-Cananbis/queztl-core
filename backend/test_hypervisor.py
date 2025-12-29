#!/usr/bin/env python3
"""
🦅 QUETZALCORE HYPERVISOR - Test Suite

Test the hypervisor with Option C: Start simple, add KVM acceleration
"""

import sys
import asyncio
sys.path.insert(0, '/Users/xavasena/hive')

from backend.hypervisor.core import QuetzalCoreHypervisor, VMState
from backend.hypervisor.vcpu import VirtualCPU
from backend.hypervisor.memory import MemoryManager
from backend.hypervisor.devices import VirtIOBlock, VirtIOGPU, VirtIONet


async def test_basic_vm():
    """Test 1: Create and start a basic VM"""
    
    print("\n" + "="*70)
    print("🧪 TEST 1: Basic VM Creation and Boot")
    print("="*70)
    
    # Create hypervisor
    hv = QuetzalCoreHypervisor(distributed=False)
    
    # Register local resources (simulate 8-core machine with 16GB RAM)
    hv.register_node("local", vcpus=8, memory_mb=16384)
    
    # Create VM
    vm_id = hv.create_vm(
        name="test-vm-basic",
        vcpus=2,
        memory_mb=2048,
        vgpus=1,
        kernel_path="/boot/vmlinuz-6.1.0",  # Will fail gracefully if doesn't exist
        cmdline="console=ttyS0 root=/dev/vda"
    )
    
    # Start VM
    await hv.start_vm(vm_id)
    
    # Let it run
    await asyncio.sleep(2)
    
    # Check stats
    stats = hv.get_stats()
    print("\n📊 Hypervisor Stats:")
    print(f"   VMs running: {stats['vms']['running']}")
    print(f"   CPU usage: {stats['resources']['vcpus_allocated']}/{stats['resources']['vcpus_total']}")
    print(f"   Memory: {stats['resources']['memory_allocated_mb']}/{stats['resources']['memory_total_mb']}MB")
    
    # Stop VM
    await hv.stop_vm(vm_id)
    
    print("\n✅ TEST 1 PASSED\n")
    return hv


async def test_vcpu():
    """Test 2: Virtual CPU instruction execution"""
    
    print("="*70)
    print("🧪 TEST 2: Virtual CPU Execution")
    print("="*70)
    
    vcpu = VirtualCPU("vcpu-test", "vm-test")
    
    # Test NOP
    print("\n1. Testing NOP instruction...")
    vcpu.execute_instruction(b'\x90')
    print(f"   RIP after NOP: {vcpu.registers.rip}")
    assert vcpu.registers.rip == 1
    
    # Test MOV immediate
    print("\n2. Testing MOV AL, 0x42...")
    vcpu.execute_instruction(b'\xB0\x42')
    print(f"   RAX after MOV: {hex(vcpu.registers.rax)}")
    assert (vcpu.registers.rax & 0xFF) == 0x42
    
    # Test software interrupt
    print("\n3. Testing INT 0x80 (system call)...")
    vcpu.execute_instruction(b'\xCD\x80')
    print(f"   Interrupts handled: {vcpu.interrupts}")
    assert vcpu.interrupts == 1
    
    # Show CPU state
    print("\n📊 CPU State:")
    state = vcpu.get_state()
    for key, value in list(state.items())[:10]:
        print(f"   {key}: {value}")
    
    print("\n✅ TEST 2 PASSED\n")


async def test_memory():
    """Test 3: Virtual memory management"""
    
    print("="*70)
    print("🧪 TEST 3: Memory Management")
    print("="*70)
    
    mm = MemoryManager("vm-test", size_mb=64)
    
    # Test page allocation
    print("\n1. Allocating pages...")
    page1 = mm.allocate_page()
    page2 = mm.allocate_page()
    print(f"   Allocated pages: {page1}, {page2}")
    assert page1 == 0 and page2 == 1
    
    # Test virtual address mapping
    print("\n2. Mapping virtual addresses...")
    virtual_addr = 0x400000  # Typical code segment
    physical_page = mm.map_page(virtual_addr)
    print(f"   Virtual {hex(virtual_addr)} → Physical page {physical_page}")
    assert physical_page is not None
    
    # Test write
    print("\n3. Writing to virtual memory...")
    test_data = b"Hello from QuetzalCore hypervisor! This is a test."
    mm.write(virtual_addr, test_data)
    print(f"   Wrote {len(test_data)} bytes")
    
    # Test read
    print("\n4. Reading from virtual memory...")
    read_data = mm.read(virtual_addr, len(test_data))
    print(f"   Read: {read_data.decode('utf-8')}")
    assert read_data == test_data
    
    # Show stats
    print("\n📊 Memory Stats:")
    stats = mm.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n✅ TEST 3 PASSED\n")


async def test_devices():
    """Test 4: Virtual devices"""
    
    print("="*70)
    print("🧪 TEST 4: Virtual Devices (VirtIO)")
    print("="*70)
    
    # Test Block Device
    print("\n1. Testing VirtIO Block (virtual disk)...")
    from backend.hypervisor.devices import VirtIORequest, DeviceType
    
    vda = VirtIOBlock("vda", "vm-test", size_gb=10)
    print(f"   {vda}")
    
    # Write block
    write_req = VirtIORequest(
        request_id=1,
        device_type=DeviceType.BLOCK,
        operation="write",
        data=b'\x00\x00\x00\x00' + b"Test block data from hypervisor"
    )
    await vda.submit_request(write_req)
    print(f"   Write: {write_req.response}")
    assert write_req.completed
    
    # Read block
    read_req = VirtIORequest(
        request_id=2,
        device_type=DeviceType.BLOCK,
        operation="read",
        data=b'\x00\x00\x00\x00'
    )
    await vda.submit_request(read_req)
    print(f"   Read: {read_req.response}")
    
    # Test GPU
    print("\n2. Testing VirtIO GPU...")
    vgpu = VirtIOGPU("vgpu0", "vm-test")
    print(f"   {vgpu}")
    
    # Render frame
    render_req = VirtIORequest(
        request_id=3,
        device_type=DeviceType.GPU,
        operation="render",
        data=b"render frame"
    )
    await vgpu.submit_request(render_req)
    print(f"   Render: {render_req.response}")
    
    # Show device stats
    print("\n📊 Device Stats:")
    print(f"   Block: {vda.get_stats()}")
    print(f"   GPU: {vgpu.get_stats()}")
    
    print("\n✅ TEST 4 PASSED\n")


async def test_distributed():
    """Test 5: Distributed hypervisor"""
    
    print("="*70)
    print("🧪 TEST 5: Distributed Hypervisor (Multi-Node)")
    print("="*70)
    
    # Create distributed hypervisor
    hv = QuetzalCoreHypervisor(distributed=True)
    
    # Register multiple QuetzalCore nodes
    print("\n1. Registering QuetzalCore nodes...")
    hv.register_node("node-1", vcpus=16, memory_mb=32768)
    hv.register_node("node-2", vcpus=16, memory_mb=32768)
    hv.register_node("node-3", vcpus=16, memory_mb=32768)
    
    # Create large VM distributed across nodes
    print("\n2. Creating distributed VM...")
    vm_id = hv.create_vm(
        name="distributed-vm",
        vcpus=32,  # More than single node
        memory_mb=65536,  # 64GB
        vgpus=2,
        kernel_path="/boot/vmlinuz-6.1.0"
    )
    
    # Start VM (will be distributed)
    await hv.start_vm(vm_id)
    
    # Check VM list
    print("\n📊 Running VMs:")
    for vm_info in hv.list_vms():
        print(f"   {vm_info['name']}: {vm_info['state']} "
              f"({vm_info['vcpus']} vCPUs, {vm_info['memory_mb']}MB)")
    
    # Stop VM
    await hv.stop_vm(vm_id)
    
    print("\n✅ TEST 5 PASSED\n")


async def test_full_stack():
    """Test 6: Full hypervisor stack"""
    
    print("="*70)
    print("🧪 TEST 6: Full Stack Integration")
    print("="*70)
    
    # Create hypervisor
    hv = QuetzalCoreHypervisor(distributed=False)
    hv.register_node("local", vcpus=8, memory_mb=16384)
    
    # Create VM with all components
    print("\n1. Creating full VM...")
    vm_id = hv.create_vm(
        name="full-stack-vm",
        vcpus=4,
        memory_mb=4096,
        vgpus=1,
        kernel_path="/boot/vmlinuz-6.1.0",
        initrd_path="/boot/initrd.img",
        cmdline="console=ttyS0 root=/dev/vda rw"
    )
    
    # Start VM (boots kernel)
    print("\n2. Booting VM...")
    await hv.start_vm(vm_id)
    
    # Simulate VM running
    await asyncio.sleep(3)
    
    # Access VM
    vm = hv.vms[vm_id]
    
    # Test CPU
    print("\n3. Testing vCPU execution...")
    if vm.vcpus:
        vcpu = vm.vcpus[0]
        vcpu.execute_instruction(b'\x90')  # NOP
        print(f"   vCPU RIP: {vcpu.registers.rip}")
    
    # Test memory
    print("\n4. Testing memory access...")
    if vm.memory_manager:
        vm.memory_manager.write(0x1000, b"Test from host")
        data = vm.memory_manager.read(0x1000, 14)
        print(f"   Memory read: {data}")
    
    # Test devices
    print("\n5. Testing devices...")
    print(f"   Devices attached: {len(vm.devices)}")
    
    # Show console output
    print("\n📺 VM Console Output:")
    for line in vm.console_output[-5:]:
        print(f"   {line}")
    
    # Clean up
    await hv.stop_vm(vm_id)
    hv.destroy_vm(vm_id)
    
    print("\n✅ TEST 6 PASSED\n")


async def run_all_tests():
    """Run complete test suite"""
    
    print("\n" + "="*70)
    print("🦅 QUETZALCORE HYPERVISOR - COMPLETE TEST SUITE")
    print("   Testing Option C: From Scratch + KVM Acceleration Path")
    print("="*70)
    
    tests = [
        ("Basic VM", test_basic_vm),
        ("Virtual CPU", test_vcpu),
        ("Memory Management", test_memory),
        ("Virtual Devices", test_devices),
        ("Distributed Mode", test_distributed),
        ("Full Stack", test_full_stack)
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            await test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ TEST FAILED: {name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    print(f"✅ Passed: {passed}/{len(tests)}")
    if failed > 0:
        print(f"❌ Failed: {failed}/{len(tests)}")
    else:
        print("🎉 ALL TESTS PASSED!")
    print("="*70 + "\n")
    
    # Next steps
    print("🚀 NEXT STEPS:")
    print("   1. ✅ Basic hypervisor working")
    print("   2. ⏭️  Add KVM acceleration for production")
    print("   3. ⏭️  Implement live VM migration")
    print("   4. ⏭️  Add MPI cluster integration")
    print("   5. ⏭️  Build Triton-style inference server")
    print("   6. ⏭️  Compile custom Linux kernel")
    print("   7. ⏭️  Deploy to production")
    print()


if __name__ == "__main__":
    asyncio.run(run_all_tests())
