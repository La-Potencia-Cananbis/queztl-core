# 🦅 Queztl-Core 3DMark - Standalone Deployment Guide

## Overview

The Queztl-Core 3DMark benchmark is a **standalone HTML file** that can be deployed **anywhere** to test **any** Queztl-Core API instance. Think of it like the real 3DMark software - it runs on your computer to test your GPU. This runs on any web host to test your API.

## 📦 What You Get

- **Single HTML file**: `dashboard/public/3dmark-benchmark.html`
- **No dependencies**: Pure HTML/CSS/JavaScript
- **No build step**: Works as-is
- **Portable**: Works on GitHub Pages, Netlify, Vercel, or even `file://`

## 🎯 Use Cases

### 1. **Test Your Local Development API**
```bash
# Run your API locally
docker-compose up -d

# Open benchmark in browser
open dashboard/public/3dmark-benchmark.html

# Select: 🏠 Localhost (http://localhost:8000)
# Click: Test Connection
# Click: RUN ALL BENCHMARKS
```

### 2. **Test Your Production API**
```bash
# Deploy benchmark to GitHub Pages
# (See deployment options below)

# Visit: https://yourusername.github.io/queztl-benchmark
# Enter: https://your-production-api.com
# Click: Test Connection
# Click: RUN ALL BENCHMARKS
```

### 3. **Share with Clients/Investors**
- Send them the HTML file (works offline!)
- Or share a hosted link
- They can test YOUR API from THEIR computer
- No installation required

### 4. **CI/CD Performance Testing**
```yaml
# GitHub Actions example
- name: Run Performance Benchmark
  run: |
    npx playwright test benchmark.spec.js
    # Opens 3dmark-benchmark.html
    # Points to staging API
    # Validates Grade A or higher
```

## 🚀 Deployment Options

### Option 1: GitHub Pages (Recommended)

**Step 1:** Create a new repo or use existing:
```bash
# Create gh-pages branch
git checkout -b gh-pages

# Copy benchmark file
cp dashboard/public/3dmark-benchmark.html index.html

# Commit and push
git add index.html
git commit -m "Deploy 3DMark benchmark"
git push origin gh-pages
```

**Step 2:** Enable GitHub Pages:
- Go to repo Settings > Pages
- Source: `gh-pages` branch
- Save

**Step 3:** Access at:
```
https://yourusername.github.io/repo-name/
```

### Option 2: Netlify

**Step 1:** Create `netlify.toml`:
```toml
[build]
  publish = "."
  
[[redirects]]
  from = "/*"
  to = "/3dmark-benchmark.html"
  status = 200
```

**Step 2:** Deploy:
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy single file
netlify deploy --prod --dir=dashboard/public
```

**Access at:** `https://your-site.netlify.app`

### Option 3: Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd dashboard/public
vercel --prod
```

### Option 4: Local File (No Server)

```bash
# Just open the file directly
open dashboard/public/3dmark-benchmark.html

# Or on Windows:
start dashboard/public/3dmark-benchmark.html

# Or on Linux:
xdg-open dashboard/public/3dmark-benchmark.html
```

⚠️ **Note:** CORS may block API calls when using `file://`. Use a local server for best results:

```bash
# Python 3
cd dashboard/public
python3 -m http.server 3001

# Node.js
npx http-server dashboard/public -p 3001

# Then open: http://localhost:3001/3dmark-benchmark.html
```

### Option 5: AWS S3 Static Website

```bash
# Upload to S3
aws s3 cp dashboard/public/3dmark-benchmark.html s3://your-bucket/index.html

# Enable static website hosting
aws s3 website s3://your-bucket --index-document index.html

# Access at: http://your-bucket.s3-website-us-east-1.amazonaws.com
```

## 🔧 Configuration

### Quick Presets

The benchmark includes 3 preset API endpoints:

1. **🏠 Localhost** - `http://localhost:8000`
   - For local development
   - API running in Docker or directly

2. **☁️ Production (Render)** - `https://queztl-core-api.onrender.com`
   - Your production deployment
   - Update this URL to match your actual production API

3. **🐝 Hive Backend** - `https://hive-backend.onrender.com`
   - Alternative deployment
   - Useful for testing multiple instances

### Custom API Endpoint

1. Enter your API URL in the input field
2. Click **🔌 Test Connection**
3. Wait for ✅ confirmation
4. Click **🚀 RUN ALL BENCHMARKS**

### Persistent Configuration

The benchmark saves your API URL to `localStorage`, so you don't have to re-enter it every time.

## 📊 How It Works

```
┌─────────────────────┐
│  3DMark Benchmark   │  ← Runs anywhere (GitHub Pages, Netlify, etc.)
│   (Static HTML)     │
└──────────┬──────────┘
           │
           │ HTTP/HTTPS
           │ Fetch API
           │
           ▼
┌─────────────────────┐
│  Queztl-Core API    │  ← Runs anywhere (Render, AWS, local Docker)
│   (FastAPI)         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  WebGPU Driver      │
│  (Python Backend)   │
└─────────────────────┘
```

**Key Points:**
- Benchmark and API are **completely separate**
- Benchmark is just an HTML file (can be anywhere)
- API is your FastAPI backend (can be anywhere)
- They communicate via HTTP REST API
- CORS must be enabled on API side

## 🛡️ CORS Configuration

Your API **must** have CORS enabled to allow the benchmark to connect:

```python
# backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

✅ **Already configured** in Queztl-Core v1.1.0+

## 🎭 Real-World Scenarios

### Scenario 1: Demo for Investor Meeting
```bash
# Deploy benchmark to GitHub Pages (one-time)
git checkout -b gh-pages
cp dashboard/public/3dmark-benchmark.html index.html
git push origin gh-pages

# During meeting:
# 1. Open: https://yourusername.github.io/queztl-benchmark
# 2. Click: ☁️ Production
# 3. Click: 🔌 Test Connection
# 4. Click: 🚀 RUN ALL BENCHMARKS
# 5. Watch live results appear
# 6. Show Grade A score
```

### Scenario 2: CI/CD Pipeline
```yaml
# .github/workflows/performance.yml
name: Performance Test

on:
  pull_request:
    branches: [main]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Start API
        run: |
          docker-compose up -d
          sleep 10
      
      - name: Run Benchmark
        run: |
          npm install -g puppeteer
          node scripts/run-benchmark.js
          # Opens 3dmark-benchmark.html
          # Runs all tests
          # Fails if score < 80
```

### Scenario 3: Load Testing Multiple Instances
```bash
# Deploy benchmark once
# Configure different API URLs:
# Instance 1: https://api-us-east.example.com
# Instance 2: https://api-eu-west.example.com
# Instance 3: https://api-asia.example.com

# Run benchmarks on each
# Compare results
# Identify best performing region
```

### Scenario 4: Customer Self-Service Testing
```bash
# Customer scenario:
# 1. You send them: https://benchmark.queztl.io
# 2. They deploy YOUR API to THEIR infrastructure
# 3. They enter their API URL
# 4. They click Test Connection
# 5. They run benchmarks
# 6. They see performance results
# 7. They decide to buy/upgrade
```

## 📈 Performance Expectations

| Test | Expected Score | What It Measures |
|------|---------------|------------------|
| Geometry | 85-95/100 | Buffer creation, mesh upload |
| Throughput | 80-90/100 | Operations per second |
| Latency | 70-85/100 | Response time (P95) |
| Concurrency | 75-90/100 | Parallel processing |
| Memory | 95-100/100 | Memory leaks, cleanup |
| Scene | 80-95/100 | Complex rendering |

**Overall Grade:**
- **S (90-100)**: 🌟 Exceptional - World-class
- **A (80-89)**: ⭐ Excellent - Production-ready
- **B (70-79)**: ✅ Very Good - Solid performance
- **C (60-69)**: 👍 Good - Adequate
- **D (0-59)**: 📊 Fair - Needs optimization

## 🔒 Security Considerations

### When Hosting Publicly

1. **No API Keys in HTML**: The benchmark doesn't store credentials
2. **HTTPS Required**: Use HTTPS for production benchmarks
3. **Rate Limiting**: Enable on your API to prevent abuse
4. **API Authentication**: Add if needed (benchmark supports custom headers)

### Adding Authentication

If your API requires auth, modify the fetch calls:

```javascript
// In 3dmark-benchmark.html, update fetch calls:
const response = await fetch(`${API_URL}/endpoint`, {
    headers: {
        'Authorization': 'Bearer YOUR_TOKEN',
        'X-API-Key': 'YOUR_KEY'
    }
});
```

## 🐛 Troubleshooting

### "Cannot reach API"
- ❌ API is not running
- ❌ URL is wrong
- ❌ CORS not enabled
- ❌ Firewall blocking
- ✅ Check API health: `curl https://your-api.com/health`

### "API returned error: 500"
- ❌ API crashed
- ❌ Database connection failed
- ✅ Check logs: `docker-compose logs backend`

### Tests Fail with Low Scores
- ⚠️ API under heavy load
- ⚠️ Network latency
- ⚠️ Cold start (serverless)
- ✅ Run tests multiple times
- ✅ Check API is warmed up

### CORS Errors
```javascript
// Error: "blocked by CORS policy"
// Fix in backend/main.py:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🎯 Next Steps

1. **Deploy Benchmark**
   ```bash
   # Choose your platform
   # Option 1: GitHub Pages (free, easy)
   # Option 2: Netlify (free, auto-deploy)
   # Option 3: Vercel (free, fast)
   ```

2. **Deploy API**
   ```bash
   # Your Queztl-Core API needs to be accessible
   # Option 1: Render.com (current)
   # Option 2: AWS/GCP/Azure
   # Option 3: Self-hosted
   ```

3. **Test Connection**
   - Open benchmark
   - Enter API URL
   - Click Test Connection
   - See ✅ confirmation

4. **Run Benchmarks**
   - Click RUN ALL BENCHMARKS
   - Wait 30-60 seconds
   - See Grade A results
   - Share with stakeholders

5. **Iterate**
   - Monitor performance over time
   - Compare different deployments
   - Track improvements
   - Celebrate victories 🎉

## 📚 Additional Resources

- **3DMark Guide**: `3DMARK_BENCHMARK_GUIDE.md`
- **API Connection**: `API_CONNECTION_GUIDE.md`
- **Deployment**: `DEPLOYMENT.md`
- **Performance Comparison**: `BLENDER_PERFORMANCE_COMPARISON.md`

---

**Built with ❤️ by Queztl-Core Team**

*This benchmark is inspired by 3DMark but 100% custom-built for Queztl-Core GPU testing.*
