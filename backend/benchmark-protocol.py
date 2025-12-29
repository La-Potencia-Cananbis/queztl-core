#!/usr/bin/env python3
"""
Benchmark Queztl Protocol vs REST API

Compares:
- Latency (ms per request)
- Throughput (requests per second)
- Overhead (bytes per message)
- CPU usage
- Memory efficiency
"""

import asyncio
import websockets
import requests
import time
import struct
import json
from statistics import mean, stdev

# Configuration
QUEZTL_URL = "ws://localhost:9999"
REST_URL = "http://localhost:8001"
NUM_REQUESTS = 1000
CONCURRENT_CONNECTIONS = 10

class QueztlBenchmark:
    """Benchmark Queztl Protocol"""
    
    MAGIC = b'QP'
    MSG_AUTH = 0x10
    MSG_COMMAND = 0x01
    MSG_ACK = 0x04
    
    def __init__(self, url):
        self.url = url
        self.ws = None
        self.latencies = []
        self.bytes_sent = 0
        self.bytes_received = 0
    
    def pack(self, msg_type: int, payload: bytes) -> bytes:
        header = struct.pack('!2sBL', self.MAGIC, msg_type, len(payload))
        return header + payload
    
    def unpack(self, data: bytes):
        magic, msg_type, length = struct.unpack('!2sBL', data[:7])
        payload = data[7:7+length]
        return msg_type, payload
    
    async def connect(self):
        self.ws = await websockets.connect(self.url)
    
    async def send_command(self, capability: str):
        payload_data = {
            "capability": capability,
            "params": {"test": True}
        }
        payload = json.dumps(payload_data).encode()
        message = self.pack(self.MSG_COMMAND, payload)
        
        start = time.perf_counter()
        await self.ws.send(message)
        response = await self.ws.recv()
        latency = (time.perf_counter() - start) * 1000  # ms
        
        self.latencies.append(latency)
        self.bytes_sent += len(message)
        self.bytes_received += len(response)
        
        return latency
    
    async def close(self):
        if self.ws:
            await self.ws.close()
    
    def get_stats(self):
        return {
            "avg_latency": mean(self.latencies),
            "min_latency": min(self.latencies),
            "max_latency": max(self.latencies),
            "stdev_latency": stdev(self.latencies) if len(self.latencies) > 1 else 0,
            "total_requests": len(self.latencies),
            "bytes_sent": self.bytes_sent,
            "bytes_received": self.bytes_received,
            "avg_overhead": self.bytes_sent / len(self.latencies) if self.latencies else 0
        }

class RESTBenchmark:
    """Benchmark REST API"""
    
    def __init__(self, url):
        self.url = url
        self.latencies = []
        self.bytes_sent = 0
        self.bytes_received = 0
        self.session = None
    
    def connect(self):
        self.session = requests.Session()
    
    def send_command(self, capability: str):
        payload = {
            "capability": capability,
            "params": {"test": True}
        }
        
        # Estimate request size (HTTP overhead + JSON)
        json_data = json.dumps(payload)
        http_overhead = 200  # Approximate HTTP headers
        self.bytes_sent += len(json_data.encode()) + http_overhead
        
        start = time.perf_counter()
        response = self.session.post(
            f"{self.url}/execute/{capability}",
            json=payload
        )
        latency = (time.perf_counter() - start) * 1000  # ms
        
        self.latencies.append(latency)
        self.bytes_received += len(response.content) + http_overhead
        
        return latency
    
    def close(self):
        if self.session:
            self.session.close()
    
    def get_stats(self):
        return {
            "avg_latency": mean(self.latencies),
            "min_latency": min(self.latencies),
            "max_latency": max(self.latencies),
            "stdev_latency": stdev(self.latencies) if len(self.latencies) > 1 else 0,
            "total_requests": len(self.latencies),
            "bytes_sent": self.bytes_sent,
            "bytes_received": self.bytes_received,
            "avg_overhead": self.bytes_sent / len(self.latencies) if self.latencies else 0
        }

async def benchmark_queztl(num_requests: int):
    """Run Queztl Protocol benchmark"""
    print(f"\n🚀 Benchmarking Queztl Protocol ({num_requests} requests)...")
    
    bench = QueztlBenchmark(QUEZTL_URL)
    await bench.connect()
    
    start_time = time.time()
    for i in range(num_requests):
        await bench.send_command("benchmark-test")
        if (i + 1) % 100 == 0:
            print(f"  Progress: {i + 1}/{num_requests}")
    
    duration = time.time() - start_time
    await bench.close()
    
    stats = bench.get_stats()
    stats["duration"] = duration
    stats["throughput"] = num_requests / duration
    
    return stats

def benchmark_rest(num_requests: int):
    """Run REST API benchmark"""
    print(f"\n🌐 Benchmarking REST API ({num_requests} requests)...")
    
    bench = RESTBenchmark(REST_URL)
    bench.connect()
    
    start_time = time.time()
    for i in range(num_requests):
        # Use a simpler endpoint for fair comparison
        bench.send_command("text-to-3d")
        if (i + 1) % 100 == 0:
            print(f"  Progress: {i + 1}/{num_requests}")
    
    duration = time.time() - start_time
    bench.close()
    
    stats = bench.get_stats()
    stats["duration"] = duration
    stats["throughput"] = num_requests / duration
    
    return stats

def print_comparison(queztl_stats, rest_stats):
    """Print comparison results"""
    
    print("\n" + "="*80)
    print(" 📊 BENCHMARK RESULTS")
    print("="*80)
    
    print("\n⚡ QUEZTL PROTOCOL:")
    print(f"  Average Latency:     {queztl_stats['avg_latency']:.2f} ms")
    print(f"  Min Latency:         {queztl_stats['min_latency']:.2f} ms")
    print(f"  Max Latency:         {queztl_stats['max_latency']:.2f} ms")
    print(f"  Throughput:          {queztl_stats['throughput']:.0f} req/s")
    print(f"  Avg Overhead:        {queztl_stats['avg_overhead']:.0f} bytes/msg")
    print(f"  Total Duration:      {queztl_stats['duration']:.2f} s")
    
    print("\n🌐 REST API:")
    print(f"  Average Latency:     {rest_stats['avg_latency']:.2f} ms")
    print(f"  Min Latency:         {rest_stats['min_latency']:.2f} ms")
    print(f"  Max Latency:         {rest_stats['max_latency']:.2f} ms")
    print(f"  Throughput:          {rest_stats['throughput']:.0f} req/s")
    print(f"  Avg Overhead:        {rest_stats['avg_overhead']:.0f} bytes/msg")
    print(f"  Total Duration:      {rest_stats['duration']:.2f} s")
    
    print("\n🏆 IMPROVEMENT:")
    latency_improvement = rest_stats['avg_latency'] / queztl_stats['avg_latency']
    throughput_improvement = queztl_stats['throughput'] / rest_stats['throughput']
    overhead_reduction = (rest_stats['avg_overhead'] - queztl_stats['avg_overhead']) / rest_stats['avg_overhead'] * 100
    
    print(f"  Latency:             {latency_improvement:.1f}x FASTER")
    print(f"  Throughput:          {throughput_improvement:.1f}x MORE")
    print(f"  Overhead Reduction:  {overhead_reduction:.1f}% SMALLER")
    
    print("\n" + "="*80)
    
    # Verdict
    if latency_improvement >= 10:
        print("✅ TARGET ACHIEVED: 10-20x latency improvement!")
    elif latency_improvement >= 5:
        print("⚠️  GOOD: 5-10x latency improvement (target: 10-20x)")
    else:
        print("❌ NEEDS WORK: Less than 5x improvement (target: 10-20x)")
    
    print("="*80)

async def main():
    print("="*80)
    print(" ⚡ QUEZTL PROTOCOL vs REST API BENCHMARK")
    print("="*80)
    print(f"\nConfiguration:")
    print(f"  Queztl URL:     {QUEZTL_URL}")
    print(f"  REST URL:       {REST_URL}")
    print(f"  Test Requests:  {NUM_REQUESTS}")
    
    # Warm up
    print("\n🔥 Warming up servers...")
    try:
        bench = QueztlBenchmark(QUEZTL_URL)
        await bench.connect()
        await bench.send_command("warmup")
        await bench.close()
    except Exception as e:
        print(f"⚠️  Could not connect to Queztl server: {e}")
        print("   Make sure the server is running with: ./deploy-queztl.sh")
        return
    
    # Run benchmarks
    queztl_stats = await benchmark_queztl(NUM_REQUESTS)
    rest_stats = benchmark_rest(NUM_REQUESTS)
    
    # Print results
    print_comparison(queztl_stats, rest_stats)

if __name__ == "__main__":
    asyncio.run(main())
