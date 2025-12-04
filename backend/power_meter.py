"""
Advanced Training & Benchmarking System for Queztl-Core
Stress testing, power measurement, and creative training scenarios
"""
import asyncio
import time
import random
import statistics
from typing import List, Dict, Any, Optional
from datetime import datetime
import psutil
import json

class PowerMeter:
    """Measure and track system performance and capabilities"""
    
    def __init__(self):
        self.metrics_history = []
        self.benchmark_results = {}
        self.stress_test_results = {}
        
    async def measure_power(self) -> Dict[str, Any]:
        """Comprehensive power measurement"""
        start_time = time.time()
        
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        # Memory metrics
        memory = psutil.virtual_memory()
        
        # Disk metrics
        disk = psutil.disk_usage('/')
        
        # Network metrics (if available)
        try:
            network = psutil.net_io_counters()
            network_stats = {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv,
            }
        except:
            network_stats = None
        
        measurement = {
            'timestamp': datetime.utcnow().isoformat(),
            'duration_ms': (time.time() - start_time) * 1000,
            'cpu': {
                'usage_percent': cpu_percent,
                'count': cpu_count,
                'frequency_mhz': cpu_freq.current if cpu_freq else None,
                'max_frequency_mhz': cpu_freq.max if cpu_freq else None,
            },
            'memory': {
                'total_gb': memory.total / (1024**3),
                'available_gb': memory.available / (1024**3),
                'used_gb': memory.used / (1024**3),
                'percent': memory.percent,
            },
            'disk': {
                'total_gb': disk.total / (1024**3),
                'used_gb': disk.used / (1024**3),
                'free_gb': disk.free / (1024**3),
                'percent': disk.percent,
            },
            'network': network_stats,
            'power_score': self._calculate_power_score(cpu_percent, memory.percent, cpu_count)
        }
        
        self.metrics_history.append(measurement)
        return measurement
    
    def _calculate_power_score(self, cpu_percent: float, memory_percent: float, cpu_count: int) -> float:
        """Calculate overall system power score (0-100)"""
        # Higher available resources = higher power
        cpu_score = (100 - cpu_percent) * 0.4
        memory_score = (100 - memory_percent) * 0.4
        core_bonus = min(cpu_count * 5, 20)  # Bonus for multi-core
        
        return min(cpu_score + memory_score + core_bonus, 100)
    
    async def run_stress_test(self, duration_seconds: int = 10, intensity: str = 'medium') -> Dict[str, Any]:
        """Run a stress test to measure maximum capacity"""
        print(f"🔥 Starting {intensity} stress test for {duration_seconds}s...")
        
        results = {
            'start_time': datetime.utcnow().isoformat(),
            'duration_seconds': duration_seconds,
            'intensity': intensity,
            'metrics': []
        }
        
        # Determine workload based on intensity
        workload_config = {
            'light': {'workers': 10, 'ops_per_worker': 100},
            'medium': {'workers': 50, 'ops_per_worker': 500},
            'heavy': {'workers': 100, 'ops_per_worker': 1000},
            'extreme': {'workers': 200, 'ops_per_worker': 2000},
        }
        
        config = workload_config.get(intensity, workload_config['medium'])
        
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        total_operations = 0
        errors = 0
        
        async def stress_worker(worker_id: int):
            nonlocal total_operations, errors
            ops = 0
            worker_errors = 0
            
            while time.time() < end_time:
                try:
                    # Simulate various operations
                    await self._simulate_workload()
                    ops += 1
                    total_operations += 1
                except Exception as e:
                    worker_errors += 1
                    errors += 1
                
                # Small delay to prevent total system lock
                await asyncio.sleep(0.001)
            
            return {'worker_id': worker_id, 'operations': ops, 'errors': worker_errors}
        
        # Run stress workers
        workers = [stress_worker(i) for i in range(config['workers'])]
        
        # Collect metrics while stress testing
        async def collect_metrics():
            while time.time() < end_time:
                metric = await self.measure_power()
                results['metrics'].append(metric)
                await asyncio.sleep(0.5)
        
        # Run workers and metric collection concurrently
        metric_task = asyncio.create_task(collect_metrics())
        worker_results = await asyncio.gather(*workers)
        await metric_task
        
        elapsed = time.time() - start_time
        
        # Calculate statistics
        cpu_usage = [m['cpu']['usage_percent'] for m in results['metrics']]
        memory_usage = [m['memory']['percent'] for m in results['metrics']]
        power_scores = [m['power_score'] for m in results['metrics']]
        
        results.update({
            'end_time': datetime.utcnow().isoformat(),
            'total_operations': total_operations,
            'operations_per_second': total_operations / elapsed,
            'total_errors': errors,
            'error_rate': errors / total_operations if total_operations > 0 else 0,
            'workers': config['workers'],
            'statistics': {
                'cpu': {
                    'avg': statistics.mean(cpu_usage),
                    'max': max(cpu_usage),
                    'min': min(cpu_usage),
                    'stddev': statistics.stdev(cpu_usage) if len(cpu_usage) > 1 else 0,
                },
                'memory': {
                    'avg': statistics.mean(memory_usage),
                    'max': max(memory_usage),
                    'min': min(memory_usage),
                    'stddev': statistics.stdev(memory_usage) if len(memory_usage) > 1 else 0,
                },
                'power_score': {
                    'avg': statistics.mean(power_scores),
                    'max': max(power_scores),
                    'min': min(power_scores),
                }
            },
            'grade': self._grade_stress_test(total_operations / elapsed, errors / total_operations if total_operations > 0 else 0)
        })
        
        self.stress_test_results[datetime.utcnow().isoformat()] = results
        
        print(f"✅ Stress test complete!")
        print(f"   Operations/sec: {results['operations_per_second']:.2f}")
        print(f"   Error rate: {results['error_rate']*100:.2f}%")
        print(f"   Grade: {results['grade']}")
        
        return results
    
    async def _simulate_workload(self):
        """Simulate various computational workloads"""
        # Random mix of operations
        operation = random.choice(['compute', 'memory', 'io', 'mixed'])
        
        if operation == 'compute':
            # CPU-intensive operation
            _ = sum([i**2 for i in range(random.randint(100, 500))])
        elif operation == 'memory':
            # Memory operation
            data = [random.random() for _ in range(random.randint(100, 1000))]
            _ = sorted(data)
        elif operation == 'io':
            # Simulate I/O delay
            await asyncio.sleep(random.uniform(0.001, 0.005))
        else:
            # Mixed operations
            data = [i * random.random() for i in range(random.randint(50, 200))]
            _ = sum(data) / len(data)
    
    def _grade_stress_test(self, ops_per_sec: float, error_rate: float) -> str:
        """Grade the stress test results"""
        if error_rate > 0.1:
            return 'F - High Error Rate'
        elif ops_per_sec > 10000:
            return 'S - Exceptional'
        elif ops_per_sec > 5000:
            return 'A - Excellent'
        elif ops_per_sec > 2000:
            return 'B - Very Good'
        elif ops_per_sec > 1000:
            return 'C - Good'
        elif ops_per_sec > 500:
            return 'D - Fair'
        else:
            return 'E - Poor'
    
    async def run_benchmark_suite(self) -> Dict[str, Any]:
        """Run comprehensive benchmark suite"""
        print("🏃 Running benchmark suite...")
        
        benchmarks = {
            'timestamp': datetime.utcnow().isoformat(),
            'tests': {}
        }
        
        # 1. Throughput test
        print("  📊 Testing throughput...")
        start = time.time()
        operations = 0
        duration = 5  # 5 seconds
        
        while time.time() - start < duration:
            await self._simulate_workload()
            operations += 1
        
        throughput = operations / duration
        benchmarks['tests']['throughput'] = {
            'operations_per_second': throughput,
            'duration': duration,
            'total_operations': operations
        }
        
        # 2. Latency test
        print("  ⏱️  Testing latency...")
        latencies = []
        for _ in range(100):
            start = time.perf_counter()
            await self._simulate_workload()
            latencies.append((time.perf_counter() - start) * 1000)
        
        benchmarks['tests']['latency'] = {
            'avg_ms': statistics.mean(latencies),
            'median_ms': statistics.median(latencies),
            'min_ms': min(latencies),
            'max_ms': max(latencies),
            'p95_ms': sorted(latencies)[int(len(latencies) * 0.95)],
            'p99_ms': sorted(latencies)[int(len(latencies) * 0.99)],
        }
        
        # 3. Concurrent operations test
        print("  🔀 Testing concurrency...")
        concurrent_workers = 50
        start = time.time()
        
        async def worker():
            for _ in range(20):
                await self._simulate_workload()
        
        await asyncio.gather(*[worker() for _ in range(concurrent_workers)])
        concurrent_duration = time.time() - start
        
        benchmarks['tests']['concurrency'] = {
            'workers': concurrent_workers,
            'operations_per_worker': 20,
            'total_time': concurrent_duration,
            'operations_per_second': (concurrent_workers * 20) / concurrent_duration
        }
        
        # 4. Memory test
        print("  💾 Testing memory...")
        memory_before = psutil.virtual_memory()
        
        # Allocate and process data
        test_data = []
        for _ in range(1000):
            test_data.append([random.random() for _ in range(1000)])
        
        memory_after = psutil.virtual_memory()
        test_data.clear()
        
        benchmarks['tests']['memory'] = {
            'allocated_mb': (memory_after.used - memory_before.used) / (1024**2),
            'available_percent': memory_after.available / memory_after.total * 100
        }
        
        # Calculate overall score
        benchmarks['overall_score'] = self._calculate_benchmark_score(benchmarks['tests'])
        
        self.benchmark_results = benchmarks
        
        print("✅ Benchmark suite complete!")
        print(f"   Overall Score: {benchmarks['overall_score']:.2f}/100")
        
        return benchmarks
    
    def _calculate_benchmark_score(self, tests: Dict) -> float:
        """Calculate overall benchmark score"""
        scores = []
        
        # Throughput score (0-25 points)
        throughput = tests['throughput']['operations_per_second']
        throughput_score = min(throughput / 100, 25)
        scores.append(throughput_score)
        
        # Latency score (0-25 points) - lower is better
        avg_latency = tests['latency']['avg_ms']
        latency_score = max(25 - (avg_latency / 10), 0)
        scores.append(latency_score)
        
        # Concurrency score (0-25 points)
        concurrency_ops = tests['concurrency']['operations_per_second']
        concurrency_score = min(concurrency_ops / 200, 25)
        scores.append(concurrency_score)
        
        # Memory score (0-25 points)
        memory_available = tests['memory']['available_percent']
        memory_score = memory_available / 4
        scores.append(memory_score)
        
        return sum(scores)
    
    def get_power_report(self) -> Dict[str, Any]:
        """Generate comprehensive power report"""
        if not self.metrics_history:
            return {'error': 'No metrics collected yet'}
        
        cpu_usage = [m['cpu']['usage_percent'] for m in self.metrics_history]
        memory_usage = [m['memory']['percent'] for m in self.metrics_history]
        power_scores = [m['power_score'] for m in self.metrics_history]
        
        return {
            'total_measurements': len(self.metrics_history),
            'time_range': {
                'start': self.metrics_history[0]['timestamp'],
                'end': self.metrics_history[-1]['timestamp'],
            },
            'cpu': {
                'avg_usage': statistics.mean(cpu_usage),
                'max_usage': max(cpu_usage),
                'min_usage': min(cpu_usage),
            },
            'memory': {
                'avg_usage': statistics.mean(memory_usage),
                'max_usage': max(memory_usage),
                'min_usage': min(memory_usage),
            },
            'power_score': {
                'avg': statistics.mean(power_scores),
                'max': max(power_scores),
                'min': min(power_scores),
                'current': power_scores[-1] if power_scores else 0,
            },
            'benchmark_results': self.benchmark_results,
            'stress_tests': list(self.stress_test_results.keys()),
        }


class CreativeTrainer:
    """Generate creative and challenging training scenarios"""
    
    def __init__(self):
        self.creativity_modes = [
            'chaos_monkey',
            'resource_starving',
            'cascade_failure',
            'traffic_spike',
            'data_corruption',
            'time_pressure',
            'multi_attack',
            'adaptive_adversary'
        ]
    
    async def chaos_monkey_scenario(self) -> Dict[str, Any]:
        """Random failures and disruptions"""
        return {
            'name': 'Chaos Monkey',
            'description': 'Random services fail unpredictably',
            'parameters': {
                'failure_rate': random.uniform(0.1, 0.3),
                'recovery_time': random.randint(1, 5),
                'affected_services': random.sample(['api', 'database', 'cache', 'queue'], k=random.randint(1, 3))
            },
            'objectives': [
                'Maintain >90% uptime',
                'Recover within 2 seconds',
                'No data loss'
            ]
        }
    
    async def resource_starving_scenario(self) -> Dict[str, Any]:
        """Limited resources challenge"""
        return {
            'name': 'Resource Starvation',
            'description': 'System has critically low resources',
            'parameters': {
                'cpu_limit': random.randint(20, 50),
                'memory_limit_mb': random.randint(128, 512),
                'connection_pool': random.randint(5, 20),
                'duration': random.randint(30, 120)
            },
            'objectives': [
                'Maintain service availability',
                'Optimize resource usage',
                'Implement graceful degradation'
            ]
        }
    
    async def cascade_failure_scenario(self) -> Dict[str, Any]:
        """One failure triggers others"""
        return {
            'name': 'Cascade Failure',
            'description': 'Initial failure causes chain reaction',
            'parameters': {
                'initial_failure': random.choice(['database', 'cache', 'api_gateway', 'auth_service']),
                'propagation_speed': random.uniform(0.5, 2.0),
                'blast_radius': random.randint(3, 8),
                'recovery_difficulty': random.choice(['easy', 'medium', 'hard'])
            },
            'objectives': [
                'Isolate the failure',
                'Prevent propagation',
                'Restore services in order'
            ]
        }
    
    async def traffic_spike_scenario(self) -> Dict[str, Any]:
        """Sudden massive traffic increase"""
        return {
            'name': 'Traffic Spike',
            'description': 'Sudden surge in requests',
            'parameters': {
                'baseline_rps': random.randint(100, 500),
                'spike_multiplier': random.randint(10, 50),
                'duration': random.randint(10, 60),
                'request_types': random.sample(['read', 'write', 'search', 'compute'], k=random.randint(1, 3))
            },
            'objectives': [
                'Handle all requests',
                'Maintain response time <500ms',
                'Auto-scale efficiently'
            ]
        }
    
    async def adaptive_adversary_scenario(self) -> Dict[str, Any]:
        """Opponent that learns and adapts"""
        return {
            'name': 'Adaptive Adversary',
            'description': 'Intelligent system that learns from your defenses',
            'parameters': {
                'learning_rate': random.uniform(0.1, 0.5),
                'attack_patterns': random.randint(5, 15),
                'adaptation_speed': random.choice(['slow', 'medium', 'fast']),
                'sophistication': random.choice(['simple', 'intermediate', 'advanced'])
            },
            'objectives': [
                'Detect patterns',
                'Implement countermeasures',
                'Stay ahead of adaptation'
            ]
        }
    
    async def generate_creative_scenario(self, mode: Optional[str] = None) -> Dict[str, Any]:
        """Generate a creative training scenario"""
        if mode is None:
            mode = random.choice(self.creativity_modes)
        
        scenarios = {
            'chaos_monkey': self.chaos_monkey_scenario,
            'resource_starving': self.resource_starving_scenario,
            'cascade_failure': self.cascade_failure_scenario,
            'traffic_spike': self.traffic_spike_scenario,
            'adaptive_adversary': self.adaptive_adversary_scenario,
        }
        
        generator = scenarios.get(mode)
        if generator:
            scenario = await generator()
            scenario['mode'] = mode
            scenario['created_at'] = datetime.utcnow().isoformat()
            return scenario
        
        # Default scenario
        return await self.chaos_monkey_scenario()
