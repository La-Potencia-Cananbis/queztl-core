#!/usr/bin/env python3
"""
Cluster CPU Workload - Distribute compute across all nodes
Actual computation to use CPU power
"""

import multiprocessing as mp
import time
import math
import random
from datetime import datetime

def cpu_intensive_task(task_id, iterations=10000000):
    """
    CPU-intensive computation: prime number generation
    """
    start = time.time()
    primes = []
    
    for num in range(2, iterations):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        
        # Progress indicator every 1M numbers
        if num % 1000000 == 0:
            print(f"  Task {task_id}: {num:,} numbers checked...")
    
    elapsed = time.time() - start
    return {
        'task_id': task_id,
        'primes_found': len(primes),
        'numbers_checked': iterations,
        'elapsed': elapsed
    }

def matrix_multiply_task(task_id, size=1000):
    """
    CPU-intensive computation: large matrix multiplication
    """
    import numpy as np
    
    start = time.time()
    print(f"  Task {task_id}: Multiplying {size}x{size} matrices...")
    
    # Create large random matrices
    matrix_a = np.random.rand(size, size)
    matrix_b = np.random.rand(size, size)
    
    # Multiply (CPU intensive)
    result = np.dot(matrix_a, matrix_b)
    
    elapsed = time.time() - start
    return {
        'task_id': task_id,
        'operation': 'matrix_multiply',
        'size': f'{size}x{size}',
        'elapsed': elapsed
    }

def run_parallel_workload(num_workers=None, duration_minutes=5):
    """
    Run CPU workload across all available cores
    """
    if num_workers is None:
        num_workers = mp.cpu_count()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  💻 CLUSTER CPU WORKLOAD RUNNER                             ║
║  Using {num_workers} CPU cores                                          ║
╚══════════════════════════════════════════════════════════════╝

Duration: {duration_minutes} minutes
Workload: Prime number generation + Matrix multiplication

Press Ctrl+C to stop early
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    
    tasks_completed = 0
    total_primes = 0
    
    try:
        while time.time() < end_time:
            print(f"\n🚀 Starting batch of {num_workers} parallel tasks...")
            
            # Create pool and run tasks
            with mp.Pool(processes=num_workers) as pool:
                # Mix of different task types
                tasks = []
                for i in range(num_workers):
                    if random.random() > 0.5:
                        tasks.append(pool.apply_async(cpu_intensive_task, (tasks_completed + i + 1, 1000000)))
                    else:
                        tasks.append(pool.apply_async(matrix_multiply_task, (tasks_completed + i + 1, 500)))
                
                # Wait for completion
                results = [task.get() for task in tasks]
            
            # Process results
            for result in results:
                tasks_completed += 1
                if 'primes_found' in result:
                    total_primes += result['primes_found']
                    print(f"  ✅ Task {result['task_id']}: Found {result['primes_found']:,} primes in {result['elapsed']:.1f}s")
                else:
                    print(f"  ✅ Task {result['task_id']}: {result['operation']} {result['size']} in {result['elapsed']:.1f}s")
            
            remaining = int((end_time - time.time()) / 60)
            print(f"\n📊 Progress: {tasks_completed} tasks completed | {remaining}min remaining")
    
    except KeyboardInterrupt:
        print(f"\n✋ Stopped by user")
    
    elapsed = (time.time() - start_time) / 60
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  📊 WORKLOAD COMPLETE                                       ║
╚══════════════════════════════════════════════════════════════╝

Duration:        {elapsed:.1f} minutes
Tasks completed: {tasks_completed}
Primes found:    {total_primes:,}
Workers used:    {num_workers} cores
Avg rate:        {tasks_completed/elapsed:.1f} tasks/min
""")

if __name__ == "__main__":
    import sys
    
    num_workers = int(sys.argv[1]) if len(sys.argv) > 1 else None
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    run_parallel_workload(num_workers, duration)
