"""
Virtual Memory Resistor (VMR) - Patent Pending Innovation
=========================================================

Simulates electrical resistor behavior in memory management:
- Resistance controls memory bandwidth (Ohm's law analogy)
- Dynamic resistance adjusts to workload
- Prevents memory bottlenecks through "current limiting"

Copyright (c) 2025 QuetzalCore-Core - All Rights Reserved
"""

import numpy as np
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
import asyncio


class ResistorMode(Enum):
    """Operating modes for VMR"""
    LOW_RESISTANCE = "low"      # High throughput, low latency
    MEDIUM_RESISTANCE = "medium" # Balanced
    HIGH_RESISTANCE = "high"     # Low throughput, prevent overload
    ADAPTIVE = "adaptive"        # Auto-adjust based on load


@dataclass
class MemoryFlow:
    """Represents memory data flow (analogous to electrical current)"""
    bytes_per_second: float
    voltage: float  # Memory pressure (priority)
    resistance: float  # Ohms (MB/s limitation)
    power: float  # Watts (computational cost)
    timestamp: float


class VirtualMemoryResistor:
    """
    🔌 Virtual Memory Resistor - Control memory flow like electrical circuit
    
    Ohm's Law Analogy:
    V = I * R
    Memory_Pressure = Data_Flow * Resistance
    
    Power = V * I
    Computational_Cost = Memory_Pressure * Data_Flow
    """
    
    def __init__(
        self,
        base_resistance: float = 10.0,  # Base resistance in "Ohms" (arbitrary unit)
        max_bandwidth_mbps: float = 1000.0,  # Maximum throughput
        mode: ResistorMode = ResistorMode.ADAPTIVE
    ):
        self.base_resistance = base_resistance
        self.max_bandwidth = max_bandwidth_mbps
        self.mode = mode
        
        # Dynamic state
        self.current_resistance = base_resistance
        self.current_flow = 0.0  # MB/s
        self.voltage = 1.0  # Memory pressure (priority multiplier)
        
        # History for adaptive behavior
        self.flow_history: List[MemoryFlow] = []
        self.max_history = 1000
        
        # Statistics
        self.total_bytes_transferred = 0
        self.total_operations = 0
        self.overload_events = 0
        
    def set_resistance(self, resistance: float):
        """Manually set resistance (Ohms)"""
        self.current_resistance = max(0.1, resistance)
        
    def set_voltage(self, voltage: float):
        """Set memory pressure (priority)"""
        self.voltage = max(0.1, min(10.0, voltage))
        
    def calculate_flow(self, requested_bytes: float) -> float:
        """
        Calculate actual data flow based on Ohm's law
        
        I = V / R
        Data_Flow = Memory_Pressure / Resistance
        """
        # Maximum theoretical flow
        max_flow = self.voltage / self.current_resistance
        
        # Limit to physical bandwidth
        actual_flow = min(max_flow, self.max_bandwidth)
        
        # Convert requested bytes to flow rate (MB/s)
        requested_mbps = requested_bytes / (1024 * 1024)
        
        # Return limited flow
        return min(actual_flow, requested_mbps)
        
    def calculate_power(self) -> float:
        """
        Calculate computational power consumption
        
        P = V * I
        Power = Memory_Pressure * Data_Flow
        """
        return self.voltage * self.current_flow
        
    def transfer_data(self, bytes_to_transfer: int, priority: float = 1.0) -> Dict:
        """
        Transfer data through VMR with resistance limiting
        
        Returns:
            - actual_bytes: Bytes successfully transferred
            - duration: Time taken (seconds)
            - throughput_mbps: Actual throughput
            - power: Computational cost
        """
        start_time = time.time()
        
        # Set voltage based on priority
        self.set_voltage(priority)
        
        # Calculate flow rate
        flow_mbps = self.calculate_flow(bytes_to_transfer)
        
        # Calculate transfer duration
        bytes_mb = bytes_to_transfer / (1024 * 1024)
        duration = bytes_mb / flow_mbps if flow_mbps > 0 else float('inf')
        
        # Simulate transfer delay
        if duration < 10:  # Only simulate if reasonable
            time.sleep(min(duration, 0.1))  # Cap at 100ms for responsiveness
        
        # Update state
        self.current_flow = flow_mbps
        actual_bytes = int(bytes_mb * flow_mbps * 1024 * 1024)
        
        # Calculate power
        power = self.calculate_power()
        
        # Record metrics
        flow_record = MemoryFlow(
            bytes_per_second=flow_mbps * 1024 * 1024,
            voltage=self.voltage,
            resistance=self.current_resistance,
            power=power,
            timestamp=time.time()
        )
        self.flow_history.append(flow_record)
        if len(self.flow_history) > self.max_history:
            self.flow_history.pop(0)
        
        self.total_bytes_transferred += actual_bytes
        self.total_operations += 1
        
        # Check for overload
        if flow_mbps >= self.max_bandwidth * 0.95:
            self.overload_events += 1
        
        # Adaptive resistance adjustment
        if self.mode == ResistorMode.ADAPTIVE:
            self._adjust_resistance()
        
        elapsed = time.time() - start_time
        
        return {
            "actual_bytes": actual_bytes,
            "requested_bytes": bytes_to_transfer,
            "duration_seconds": elapsed,
            "throughput_mbps": flow_mbps,
            "resistance_ohms": self.current_resistance,
            "voltage": self.voltage,
            "power_watts": power,
            "efficiency": (actual_bytes / bytes_to_transfer) * 100 if bytes_to_transfer > 0 else 0
        }
    
    def _adjust_resistance(self):
        """Adaptive resistance adjustment based on load history"""
        if len(self.flow_history) < 10:
            return
        
        recent = self.flow_history[-10:]
        avg_flow = np.mean([f.bytes_per_second for f in recent])
        avg_power = np.mean([f.power for f in recent])
        
        # Increase resistance if approaching overload
        utilization = avg_flow / (self.max_bandwidth * 1024 * 1024)
        
        if utilization > 0.9:
            # High load - increase resistance to prevent overload
            self.current_resistance *= 1.1
        elif utilization < 0.3 and avg_power < 2.0:
            # Low load and low power - decrease resistance for better performance
            self.current_resistance *= 0.9
        
        # Clamp resistance to reasonable range
        self.current_resistance = max(0.5, min(100.0, self.current_resistance))
    
    def get_stats(self) -> Dict:
        """Get VMR statistics"""
        avg_throughput = (self.total_bytes_transferred / self.total_operations / 1024 / 1024) if self.total_operations > 0 else 0
        
        recent_flows = self.flow_history[-100:] if self.flow_history else []
        recent_power = np.mean([f.power for f in recent_flows]) if recent_flows else 0
        
        return {
            "current_resistance_ohms": self.current_resistance,
            "current_voltage": self.voltage,
            "current_flow_mbps": self.current_flow,
            "current_power_watts": self.calculate_power(),
            "total_operations": self.total_operations,
            "total_bytes_transferred": self.total_bytes_transferred,
            "average_throughput_mbps": avg_throughput,
            "overload_events": self.overload_events,
            "mode": self.mode.value,
            "recent_power_watts": recent_power,
            "utilization_percent": (self.current_flow / self.max_bandwidth) * 100
        }
    
    def benchmark(self, test_sizes: List[int]) -> Dict:
        """Benchmark VMR with different data sizes"""
        results = []
        
        for size in test_sizes:
            result = self.transfer_data(size, priority=1.0)
            results.append({
                "size_mb": size / (1024 * 1024),
                "throughput_mbps": result["throughput_mbps"],
                "duration_ms": result["duration_seconds"] * 1000,
                "efficiency": result["efficiency"],
                "power_watts": result["power_watts"]
            })
        
        return {
            "benchmark_results": results,
            "vmr_stats": self.get_stats()
        }


class ParallelVMRArray:
    """
    🔌🔌🔌 Array of VMRs working in parallel (like resistors in parallel)
    
    Total Resistance = 1 / (1/R1 + 1/R2 + ... + 1/Rn)
    Total Throughput = Sum of individual throughputs
    """
    
    def __init__(self, num_resistors: int = 4, base_resistance: float = 10.0):
        self.vmrs = [
            VirtualMemoryResistor(
                base_resistance=base_resistance,
                max_bandwidth_mbps=1000.0,
                mode=ResistorMode.ADAPTIVE
            )
            for _ in range(num_resistors)
        ]
        self.num_resistors = num_resistors
        
    def parallel_transfer(self, total_bytes: int, priority: float = 1.0) -> Dict:
        """Transfer data across parallel VMRs"""
        # Split data across resistors
        bytes_per_vmr = total_bytes // self.num_resistors
        
        start_time = time.time()
        
        # Parallel transfers
        results = []
        for vmr in self.vmrs:
            result = vmr.transfer_data(bytes_per_vmr, priority)
            results.append(result)
        
        # Aggregate results
        total_transferred = sum(r["actual_bytes"] for r in results)
        avg_throughput = np.mean([r["throughput_mbps"] for r in results])
        total_throughput = sum(r["throughput_mbps"] for r in results)
        total_power = sum(r["power_watts"] for r in results)
        
        # Equivalent parallel resistance
        parallel_resistance = 1.0 / sum(1.0 / vmr.current_resistance for vmr in self.vmrs)
        
        elapsed = time.time() - start_time
        
        return {
            "total_bytes_transferred": total_transferred,
            "requested_bytes": total_bytes,
            "duration_seconds": elapsed,
            "average_throughput_mbps": avg_throughput,
            "total_throughput_mbps": total_throughput,
            "parallel_resistance_ohms": parallel_resistance,
            "total_power_watts": total_power,
            "num_vmrs": self.num_resistors,
            "speedup": total_throughput / avg_throughput if avg_throughput > 0 else 1.0,
            "efficiency": (total_transferred / total_bytes) * 100 if total_bytes > 0 else 0
        }
    
    def get_array_stats(self) -> Dict:
        """Get statistics for entire array"""
        individual_stats = [vmr.get_stats() for vmr in self.vmrs]
        
        return {
            "num_vmrs": self.num_resistors,
            "parallel_resistance_ohms": 1.0 / sum(1.0 / vmr.current_resistance for vmr in self.vmrs),
            "total_throughput_mbps": sum(vmr.current_flow for vmr in self.vmrs),
            "total_power_watts": sum(vmr.calculate_power() for vmr in self.vmrs),
            "individual_vmrs": individual_stats
        }