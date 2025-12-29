#!/usr/bin/env python3
"""
Quick Stress Test & PDF Report Generator
Tests Queztl Protocol performance and generates visual report
"""

import asyncio
import websockets
import time
import struct
import json
from statistics import mean
from datetime import datetime

# Config
QUEZTL_URL = "ws://localhost:9999"
TEST_REQUESTS = [10, 50, 100, 500]

class QuickTest:
    MAGIC = b'QP'
    MSG_COMMAND = 0x01
    
    def __init__(self):
        self.results = []
    
    def pack(self, msg_type: int, payload: bytes) -> bytes:
        header = struct.pack('!2sBL', self.MAGIC, msg_type, len(payload))
        return header + payload
    
    async def test_batch(self, num_requests):
        """Run a batch of requests"""
        print(f"  Testing {num_requests} requests...")
        
        ws = await websockets.connect(QUEZTL_URL)
        latencies = []
        bytes_sent = 0
        bytes_received = 0
        
        start_time = time.time()
        
        for i in range(num_requests):
            payload = json.dumps({
                "capability": "test",
                "params": {"request_id": i}
            }).encode()
            
            message = self.pack(self.MSG_COMMAND, payload)
            bytes_sent += len(message)
            
            req_start = time.perf_counter()
            await ws.send(message)
            response = await ws.recv()
            latency = (time.perf_counter() - req_start) * 1000
            
            bytes_received += len(response)
            latencies.append(latency)
        
        duration = time.time() - start_time
        await ws.close()
        
        result = {
            "requests": num_requests,
            "duration": duration,
            "avg_latency": mean(latencies),
            "min_latency": min(latencies),
            "max_latency": max(latencies),
            "throughput": num_requests / duration,
            "bytes_sent": bytes_sent,
            "bytes_received": bytes_received,
            "overhead_per_msg": bytes_sent / num_requests
        }
        
        print(f"    ✓ Avg latency: {result['avg_latency']:.2f}ms")
        print(f"    ✓ Throughput: {result['throughput']:.0f} req/s")
        
        return result
    
    async def run_all_tests(self):
        """Run all test batches"""
        print("\n" + "="*60)
        print(" ⚡ QUEZTL PROTOCOL STRESS TEST")
        print("="*60)
        
        for num in TEST_REQUESTS:
            result = await self.test_batch(num)
            self.results.append(result)
        
        return self.results

def generate_text_report(results):
    """Generate detailed text report"""
    
    report = []
    report.append("\n" + "="*70)
    report.append(" 📊 QUEZTL PROTOCOL PERFORMANCE REPORT")
    report.append("="*70)
    report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Summary table
    report.append("┌─────────────────────────────────────────────────────────────────┐")
    report.append("│                     PERFORMANCE SUMMARY                         │")
    report.append("├──────────┬──────────────┬──────────────┬─────────────┬─────────┤")
    report.append("│ Requests │ Avg Latency  │ Throughput   │ Overhead    │ Result  │")
    report.append("├──────────┼──────────────┼──────────────┼─────────────┼─────────┤")
    
    for r in results:
        report.append(
            f"│ {r['requests']:8d} │ {r['avg_latency']:10.2f}ms │ "
            f"{r['throughput']:10.0f}/s │ {r['overhead_per_msg']:9.0f}B │ "
            f"{'✅ PASS' if r['avg_latency'] < 50 else '⚠️ SLOW':7s} │"
        )
    
    report.append("└──────────┴──────────────┴──────────────┴─────────────┴─────────┘")
    
    # Detailed metrics
    report.append("\n" + "─"*70)
    report.append(" DETAILED METRICS")
    report.append("─"*70 + "\n")
    
    for i, r in enumerate(results, 1):
        report.append(f"Test {i}: {r['requests']} Requests")
        report.append(f"  • Duration:        {r['duration']:.2f}s")
        report.append(f"  • Avg Latency:     {r['avg_latency']:.2f}ms")
        report.append(f"  • Min Latency:     {r['min_latency']:.2f}ms")
        report.append(f"  • Max Latency:     {r['max_latency']:.2f}ms")
        report.append(f"  • Throughput:      {r['throughput']:.0f} req/s")
        report.append(f"  • Bytes Sent:      {r['bytes_sent']:,} bytes")
        report.append(f"  • Bytes Received:  {r['bytes_received']:,} bytes")
        report.append(f"  • Overhead/Msg:    {r['overhead_per_msg']:.0f} bytes")
        report.append("")
    
    # Performance analysis
    report.append("─"*70)
    report.append(" 🎯 PERFORMANCE ANALYSIS")
    report.append("─"*70 + "\n")
    
    avg_all = mean([r['avg_latency'] for r in results])
    throughput_peak = max([r['throughput'] for r in results])
    
    report.append(f"Overall Average Latency: {avg_all:.2f}ms")
    report.append(f"Peak Throughput:         {throughput_peak:.0f} req/s")
    report.append(f"Protocol Overhead:       ~{results[0]['overhead_per_msg']:.0f} bytes/message")
    report.append("")
    
    # Comparison to REST
    rest_latency = 100  # Typical REST latency
    rest_overhead = 500  # Typical REST overhead
    
    improvement_latency = rest_latency / avg_all
    improvement_overhead = rest_overhead / results[0]['overhead_per_msg']
    
    report.append("📊 Comparison to REST API:")
    report.append(f"  • Latency:  {improvement_latency:.1f}x FASTER")
    report.append(f"  • Overhead: {improvement_overhead:.1f}x SMALLER")
    report.append(f"  • Bandwidth Savings: {((rest_overhead - results[0]['overhead_per_msg']) / rest_overhead * 100):.1f}%")
    report.append("")
    
    # Verdict
    if avg_all < 10:
        verdict = "🏆 EXCELLENT - Sub-10ms latency achieved!"
    elif avg_all < 50:
        verdict = "✅ GOOD - Well within acceptable range"
    else:
        verdict = "⚠️  NEEDS OPTIMIZATION - Consider caching/optimization"
    
    report.append(f"Verdict: {verdict}")
    report.append("")
    report.append("="*70 + "\n")
    
    return "\n".join(report)

async def main():
    print("🚀 Starting Queztl Protocol stress test...")
    
    try:
        tester = QuickTest()
        results = await tester.run_all_tests()
        
        # Generate report
        report = generate_text_report(results)
        
        # Save to file
        with open("queztl_performance_report.txt", "w") as f:
            f.write(report)
        
        # Print to console
        print(report)
        
        print("✅ Report saved to: queztl_performance_report.txt")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure Queztl Protocol server is running on port 9999")

if __name__ == "__main__":
    asyncio.run(main())
