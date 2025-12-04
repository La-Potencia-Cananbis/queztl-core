# 💪 Queztl-Core Power Testing & Training Guide

## 🎯 Flexing & Measuring Queztl-Core's Power

This guide shows you creative ways to train and measure the system's capabilities!

---

## 🔥 Power Measurement

### Quick Power Check
```bash
# Measure current system power
curl http://localhost:8000/api/power/measure | jq

# You'll see:
# - CPU usage and core count
# - Memory usage and availability
# - Disk usage
# - Network stats
# - Overall power score (0-100)
```

### Get Detailed Report
```bash
curl http://localhost:8000/api/power/report | jq
```

---

## 💥 Stress Testing

### Light Stress Test (10 seconds)
```bash
curl -X POST "http://localhost:8000/api/power/stress-test?duration=10&intensity=light" | jq
```

### Medium Stress Test (15 seconds)
```bash
curl -X POST "http://localhost:8000/api/power/stress-test?duration=15&intensity=medium" | jq
```

### Heavy Stress Test (20 seconds)
```bash
curl -X POST "http://localhost:8000/api/power/stress-test?duration=20&intensity=heavy" | jq
```

### Extreme Stress Test (30 seconds)
```bash
curl -X POST "http://localhost:8000/api/power/stress-test?duration=30&intensity=extreme" | jq
```

**Results Include:**
- Operations per second
- Error rate
- CPU/Memory statistics
- Overall grade (F to S rank)

---

## 🏆 Benchmark Suite

Run a comprehensive benchmark to measure all capabilities:

```bash
curl -X POST http://localhost:8000/api/power/benchmark | jq
```

**Tests:**
- ⚡ Throughput Test - Operations per second
- ⏱️  Latency Test - Response time (avg, p95, p99)
- 🔀 Concurrency Test - Parallel operation handling
- 💾 Memory Test - Memory allocation and management

**Overall Score:** 0-100 points

---

## 🧠 Creative Training Scenarios

### 1. Chaos Monkey 🐵💀
Random service failures:
```bash
curl -X POST "http://localhost:8000/api/training/creative?mode=chaos_monkey" | jq
```

**Challenge:** 
- Random services fail unpredictably
- Maintain >90% uptime
- Recover within 2 seconds

### 2. Resource Starvation ⚠️
System with critically low resources:
```bash
curl -X POST "http://localhost:8000/api/training/creative?mode=resource_starving" | jq
```

**Challenge:**
- Limited CPU (20-50%)
- Limited Memory (128-512 MB)
- Small connection pool
- Maintain availability

### 3. Cascade Failure 🌊
One failure triggers others:
```bash
curl -X POST "http://localhost:8000/api/training/creative?mode=cascade_failure" | jq
```

**Challenge:**
- Initial failure propagates
- Isolate the failure
- Prevent spread
- Restore in correct order

### 4. Traffic Spike 📈
Sudden massive load:
```bash
curl -X POST "http://localhost:8000/api/training/creative?mode=traffic_spike" | jq
```

**Challenge:**
- 10-50x traffic increase
- Maintain response time <500ms
- Auto-scale efficiently

### 5. Adaptive Adversary 🤖
Intelligent opponent that learns:
```bash
curl -X POST "http://localhost:8000/api/training/creative?mode=adaptive_adversary" | jq
```

**Challenge:**
- Opponent learns from your defenses
- Detect patterns
- Implement countermeasures
- Stay ahead of adaptation

### Random Creative Scenario
Let the system choose:
```bash
curl -X POST http://localhost:8000/api/training/creative | jq
```

---

## 📊 View Available Modes

```bash
curl http://localhost:8000/api/training/creative/modes | jq
```

**Available Modes:**
- `chaos_monkey` - Random failures
- `resource_starving` - Limited resources
- `cascade_failure` - Chain reactions
- `traffic_spike` - Load surges
- `data_corruption` - Invalid data
- `time_pressure` - Time constraints
- `multi_attack` - Multiple challenges
- `adaptive_adversary` - Learning opponent

---

## 🏅 Leaderboard

Check top performance results:
```bash
curl http://localhost:8000/api/power/leaderboard | jq
```

Shows:
- Top 10 stress test results
- Operations per second
- Grades (F to S)
- Error rates

---

## 🎮 Interactive Dashboard

Visit **http://localhost:3000** for the full dashboard with:

### Power Meter Section
- Real-time system metrics
- CPU, Memory, Disk usage
- Power score visualization
- One-click stress tests (Light, Medium, Heavy, Extreme)
- Benchmark suite runner
- Live results display

### Creative Training Section
- Visual mode selector
- Scenario parameter display
- Objectives checklist
- One-click scenario generation

---

## 💡 Creative Ways to Flex

### 1. **Progressive Overload**
Start light, increase intensity:
```bash
# Day 1: Light
curl -X POST "http://localhost:8000/api/power/stress-test?duration=10&intensity=light"

# Day 2: Medium
curl -X POST "http://localhost:8000/api/power/stress-test?duration=15&intensity=medium"

# Day 3: Heavy
curl -X POST "http://localhost:8000/api/power/stress-test?duration=20&intensity=heavy"

# Day 4: Extreme
curl -X POST "http://localhost:8000/api/power/stress-test?duration=30&intensity=extreme"
```

### 2. **Endurance Training**
Long-duration stress tests:
```bash
# 1 minute medium intensity
curl -X POST "http://localhost:8000/api/power/stress-test?duration=60&intensity=medium"

# 5 minutes light intensity
curl -X POST "http://localhost:8000/api/power/stress-test?duration=300&intensity=light"
```

### 3. **Power Cycle**
Measure before and after:
```bash
# Before
curl http://localhost:8000/api/power/measure | jq '.power_score'

# Stress test
curl -X POST "http://localhost:8000/api/power/stress-test?duration=20&intensity=heavy"

# After
curl http://localhost:8000/api/power/measure | jq '.power_score'
```

### 4. **Multi-Modal Training**
Combine different scenarios:
```bash
# 1. Start with chaos
curl -X POST "http://localhost:8000/api/training/creative?mode=chaos_monkey"

# 2. Add resource pressure
curl -X POST "http://localhost:8000/api/training/creative?mode=resource_starving"

# 3. Simulate traffic spike
curl -X POST "http://localhost:8000/api/training/creative?mode=traffic_spike"
```

### 5. **Benchmark Competition**
Challenge yourself or others:
```bash
# Run benchmark and save result
curl -X POST http://localhost:8000/api/power/benchmark | jq '.overall_score' > score.txt

# Compare with previous best
echo "Previous best: $(cat best_score.txt)"
echo "Current score: $(cat score.txt)"

# If better, save as new best
if [ $(cat score.txt) > $(cat best_score.txt) ]; then
    cp score.txt best_score.txt
    echo "🎉 New record!"
fi
```

### 6. **Continuous Monitoring**
Watch power in real-time:
```bash
# Monitor power score every 2 seconds
while true; do
    curl -s http://localhost:8000/api/power/measure | jq -r '"Power: \(.power_score) | CPU: \(.cpu.usage_percent)% | Memory: \(.memory.percent)%"'
    sleep 2
done
```

---

## 🎯 Grade System

### Stress Test Grades
- **S** - Exceptional (>10,000 ops/sec)
- **A** - Excellent (>5,000 ops/sec)
- **B** - Very Good (>2,000 ops/sec)
- **C** - Good (>1,000 ops/sec)
- **D** - Fair (>500 ops/sec)
- **E** - Poor (<500 ops/sec)
- **F** - High Error Rate (>10% errors)

### Power Score (0-100)
- **90-100**: Excellent - System running smoothly
- **70-89**: Good - Normal operation
- **50-69**: Fair - Under load
- **30-49**: Poor - Heavy load
- **0-29**: Critical - System stressed

---

## 📈 Performance Goals

### Beginner Goals
- ✅ Run all 4 stress test intensities
- ✅ Complete benchmark suite
- ✅ Try 3 different creative scenarios
- ✅ Achieve Grade C or higher

### Intermediate Goals
- ✅ Achieve Grade B on heavy stress test
- ✅ Benchmark score >60/100
- ✅ Complete all 8 creative scenarios
- ✅ Maintain <5% error rate

### Advanced Goals
- ✅ Achieve Grade A on extreme stress test
- ✅ Benchmark score >80/100
- ✅ Handle cascade failure successfully
- ✅ Beat adaptive adversary

### Expert Goals
- ✅ Achieve Grade S (>10,000 ops/sec)
- ✅ Benchmark score >90/100
- ✅ Zero errors on heavy stress test
- ✅ Create custom training scenarios

---

## 🔬 Advanced Testing

### Custom Stress Test Duration
```bash
# 2-minute medium test
curl -X POST "http://localhost:8000/api/power/stress-test?duration=120&intensity=medium"
```

### Monitor During Training
```bash
# Terminal 1: Start stress test
curl -X POST "http://localhost:8000/api/power/stress-test?duration=30&intensity=heavy"

# Terminal 2: Watch metrics
watch -n 1 'curl -s http://localhost:8000/api/power/measure | jq ".cpu.usage_percent, .memory.percent, .power_score"'
```

### Batch Testing Script
```bash
#!/bin/bash
echo "🔥 Running comprehensive test suite..."

for intensity in light medium heavy extreme; do
    echo "Testing $intensity..."
    curl -X POST "http://localhost:8000/api/power/stress-test?duration=10&intensity=$intensity" \
        | jq "{intensity: \"$intensity\", ops_per_sec: .operations_per_second, grade: .grade}"
    sleep 5
done

echo "✅ All tests complete!"
```

---

## 📊 Metrics to Track

1. **Operations/Second** - Raw throughput
2. **Error Rate** - Reliability (target: <1%)
3. **CPU Usage** - Resource efficiency
4. **Memory Usage** - Memory management
5. **Power Score** - Overall health
6. **Benchmark Score** - Comprehensive performance
7. **Latency** - Response time (p95, p99)
8. **Concurrency** - Parallel handling

---

## 🎓 Training Program

### Week 1: Foundation
- Day 1-2: Run all stress tests, understand metrics
- Day 3-4: Try each creative scenario
- Day 5: Run benchmark suite
- Day 6-7: Analyze results, identify weaknesses

### Week 2: Progression
- Day 1-3: Focus on weakest areas
- Day 4-5: Increase test duration
- Day 6: Combination training
- Day 7: Full benchmark

### Week 3: Mastery
- Day 1-2: Extreme stress tests only
- Day 3-4: Advanced creative scenarios
- Day 5: Endurance tests (5+ minutes)
- Day 6-7: Competition mode

---

## 🏆 Achievement Unlocks

- 🥉 **Bronze**: Complete first stress test
- 🥈 **Silver**: Achieve Grade B or higher
- 🥇 **Gold**: Achieve Grade A or higher
- 💎 **Diamond**: Achieve Grade S
- 🌟 **Legendary**: Grade S + Benchmark >90 + Zero errors

---

## 🛠️ Troubleshooting

### Low Performance
- Check system resources
- Close unnecessary applications
- Restart Docker containers
- Adjust stress test intensity

### High Error Rates
- Reduce intensity
- Increase test duration
- Check logs for issues
- Verify database connection

### Crashes During Tests
- Start with lower intensity
- Monitor system resources
- Check Docker logs
- Ensure adequate RAM/CPU

---

## 📚 Next Steps

1. **Start Simple**: Run a light stress test
2. **Measure Baseline**: Get your benchmark score
3. **Set Goals**: Choose target metrics
4. **Train Regularly**: Daily stress tests
5. **Track Progress**: Monitor improvements
6. **Share Results**: Post your leaderboard scores!

---

**Ready to flex Queztl-Core's muscles? Start with:**

```bash
curl -X POST "http://localhost:8000/api/power/stress-test?duration=10&intensity=medium" | jq
```

**Or visit the dashboard:** http://localhost:3000

Let's see what this system can do! 💪🦅
