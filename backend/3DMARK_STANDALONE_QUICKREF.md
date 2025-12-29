# 🦅 3DMark Standalone - Quick Reference

## What Is It?

A **standalone HTML benchmark** that runs **anywhere** to test **any** Queztl-Core API.

Think of it like this:
- Real 3DMark → Runs on your PC → Tests your GPU
- This 3DMark → Runs on any web host → Tests your API

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  3DMark Benchmark (Standalone HTML)                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  • Single HTML file                                     │
│  • No dependencies                                       │
│  • Runs on: GitHub Pages, Netlify, Vercel, S3, etc.    │
│  • Can even run locally (file://)                       │
│  • Pure HTML/CSS/JavaScript                             │
└─────────────────┬───────────────────────────────────────┘
                  │
                  │ HTTP/HTTPS Requests
                  │ (CORS-enabled)
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  Queztl-Core API (Your Backend)                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  • FastAPI Backend                                      │
│  • WebGPU Driver                                        │
│  • Runs on: Render, AWS, Local Docker, anywhere        │
│  • Completely separate from benchmark                   │
└─────────────────────────────────────────────────────────┘
```

## Key Benefits

### ✅ Fully Decoupled
- Benchmark ≠ API (they're separate)
- Deploy each independently
- Update either without affecting the other

### ✅ Universal Testing
- Test localhost during development
- Test staging before production
- Test production for demos
- Test competitor APIs (if compatible)

### ✅ Easy Distribution
- Send HTML file via email
- Host on GitHub Pages (free)
- Share link with investors
- No installation required

### ✅ CI/CD Ready
- Run in GitHub Actions
- Automated performance testing
- Fail builds if performance drops
- Track metrics over time

## Quick Start

### Option 1: Test Locally
```bash
# Start your API
docker-compose up -d

# Deploy benchmark locally
./deploy-benchmark.sh
# Choose: 4 (Local Test Server)

# Open browser:
open http://localhost:3001/3dmark-benchmark.html

# Configure:
# 1. Click: 🏠 Localhost
# 2. Click: 🔌 Test Connection
# 3. Click: 🚀 RUN ALL BENCHMARKS
```

### Option 2: Deploy to GitHub Pages
```bash
./deploy-benchmark.sh
# Choose: 1 (GitHub Pages)

# Then:
git push origin gh-pages

# Enable Pages in repo settings
# Access at: https://yourusername.github.io/repo-name/
```

### Option 3: Deploy to Netlify
```bash
./deploy-benchmark.sh
# Choose: 2 (Netlify)

# Automatically deployed!
# URL will be shown
```

### Option 4: Share Standalone Package
```bash
./deploy-benchmark.sh
# Choose: 5 (Create Standalone Package)

# Send the generated ZIP to anyone
# They can extract and test YOUR API
```

## Configuration

The benchmark has **3 preset endpoints**:

1. **🏠 Localhost** - `http://localhost:8000`
   - For development
   - API running in Docker

2. **☁️ Production** - `https://queztl-core-api.onrender.com`
   - Your deployed API
   - Update this URL to match yours

3. **🐝 Custom** - Enter any URL
   - Test different instances
   - Compare performance
   - Validate deployments

## Use Cases

### 1. Development Testing
```bash
# Developer workflow:
# 1. Make API changes
# 2. Start API: docker-compose up
# 3. Open benchmark: localhost:3001
# 4. Select: 🏠 Localhost
# 5. Run tests
# 6. See if performance improved
```

### 2. Investor Demo
```bash
# Demo workflow:
# 1. Deploy benchmark to GitHub Pages (once)
# 2. During meeting, open URL
# 3. Select: ☁️ Production
# 4. Click: RUN ALL BENCHMARKS
# 5. Show Grade A score live
# 6. Compare to 3DMark pricing ($30-$1,500)
```

### 3. Client Self-Service
```bash
# Client workflow:
# 1. You send: benchmark URL
# 2. They deploy YOUR API to THEIR infrastructure
# 3. They enter their API URL in benchmark
# 4. They run tests
# 5. They see performance
# 6. They decide to purchase
```

### 4. CI/CD Pipeline
```yaml
# .github/workflows/performance.yml
- name: Performance Test
  run: |
    docker-compose up -d
    npx playwright test benchmark.spec.js
    # Fails if score < 80
```

### 5. Multi-Region Testing
```bash
# Test different deployments:
# 1. US-East: https://api-us.example.com
# 2. EU-West: https://api-eu.example.com
# 3. Asia: https://api-asia.example.com
# Run same benchmark on each
# Compare results
# Choose best region
```

## Expected Results

| Test | Score | What It Tests |
|------|-------|---------------|
| Geometry | 92/100 | Buffer creation, mesh upload |
| Throughput | 87/100 | 5.82M ops/sec |
| Latency | 78/100 | P95 response time |
| Concurrency | 85/100 | Parallel processing |
| Memory | 100/100 | No leaks |
| Scene | 89/100 | Complex rendering |
| **Overall** | **88.5/100** | **Grade A - EXCELLENT** |

## Troubleshooting

### "Cannot reach API"
```bash
# Check API is running:
curl http://localhost:8000/health

# If API is remote:
curl https://your-api.com/health

# Check CORS is enabled in backend/main.py
```

### CORS Errors
```python
# Ensure this is in backend/main.py:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific domains
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Tests Fail
```bash
# API might be cold-starting (serverless)
# Solution: Run tests twice
# First run warms up the API
# Second run shows true performance
```

## Files

| File | Purpose |
|------|---------|
| `dashboard/public/3dmark-benchmark.html` | The benchmark (standalone) |
| `3DMARK_STANDALONE_GUIDE.md` | Full deployment guide |
| `deploy-benchmark.sh` | Deployment helper script |
| `3DMARK_BENCHMARK_GUIDE.md` | Test descriptions |
| `3DMARK_COMPLETE.md` | Summary document |

## Next Steps

1. **Test Locally First**
   ```bash
   ./deploy-benchmark.sh
   # Choose option 4
   # Verify Grade A
   ```

2. **Deploy Benchmark**
   ```bash
   # Choose your platform:
   # - GitHub Pages (recommended)
   # - Netlify
   # - Vercel
   ```

3. **Share Results**
   - Screenshot Grade A score
   - Share benchmark URL
   - Let others test YOUR API
   - Celebrate! 🎉

## Documentation

- **Full Guide**: `3DMARK_STANDALONE_GUIDE.md`
- **Test Details**: `3DMARK_BENCHMARK_GUIDE.md`
- **API Connection**: `API_CONNECTION_GUIDE.md`
- **Performance**: `BLENDER_PERFORMANCE_COMPARISON.md`

---

**Remember:** The benchmark and API are **completely separate**. The benchmark is just a testing tool that can live anywhere and test any Queztl-Core API instance.

**Built with ❤️ by Queztl-Core Team**
