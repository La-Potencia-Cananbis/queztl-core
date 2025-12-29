# 🌐 Queztl-Core Web Deployment Guide

## Overview
The Queztl-Core 3DMark benchmark suite is now **fully web-deployable**! You can host it on GitHub Pages, Netlify, Vercel, or any static hosting service and connect it to your API backend.

---

## 🚀 Quick Deploy Options

### Option 1: GitHub Pages (FREE)
```bash
# 1. Create gh-pages branch
git checkout -b gh-pages

# 2. Copy benchmark to root
cp dashboard/public/3dmark-benchmark.html index.html

# 3. Push to GitHub
git add index.html
git commit -m "Deploy 3DMark benchmark to GitHub Pages"
git push origin gh-pages

# 4. Enable GitHub Pages
# Go to: Settings > Pages > Source: gh-pages branch
# Your site: https://yourusername.github.io/queztl-core/
```

### Option 2: Netlify (FREE, Auto-Deploy)
```bash
# 1. Create netlify.toml (already exists!)
# 2. Connect your repo to Netlify
# 3. Deploy settings:
#    - Build command: (leave empty)
#    - Publish directory: dashboard/public
#    - Auto-deploy: ON

# Your site: https://queztl-core.netlify.app/3dmark-benchmark.html
```

### Option 3: Vercel (FREE)
```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy
cd dashboard/public
vercel --prod

# Your site: https://queztl-core.vercel.app/3dmark-benchmark.html
```

### Option 4: Custom Domain
Just copy `3dmark-benchmark.html` to your web server!

---

## 🔧 API Backend Configuration

The benchmark automatically connects to your API. You have 3 options:

### Option A: Use Production API (Default)
```javascript
// Default in code (Render deployment)
https://queztl-core-api.onrender.com
```

### Option B: Use Local Development API
1. Open `3dmark-benchmark.html`
2. In the API Configuration panel, enter: `http://localhost:8000`
3. Click "Test Connection"
4. If successful, this will be saved in localStorage

### Option C: Use Custom API URL
1. Deploy your backend to any cloud provider
2. Update the API URL in the configuration panel
3. The URL persists across page reloads (localStorage)

---

## 📦 Deploy Backend to Production

### Render.com (Recommended, FREE tier)
```bash
# 1. Push your code to GitHub
git push origin main

# 2. Create new Web Service on Render
# - Repository: your-repo
# - Build Command: pip install -r backend/requirements.txt
# - Start Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
# - Environment: Python 3.11

# 3. Your API: https://your-app.onrender.com
```

### Heroku
```bash
# 1. Login to Heroku
heroku login

# 2. Create app
heroku create queztl-core-api

# 3. Deploy
git push heroku main

# Your API: https://queztl-core-api.herokuapp.com
```

### Railway
```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login and init
railway login
railway init

# 3. Deploy
railway up

# Your API: https://your-app.railway.app
```

### Docker (Any Cloud)
```bash
# Build and push
docker build -t queztl-core-backend ./backend
docker tag queztl-core-backend your-registry/queztl-core-backend
docker push your-registry/queztl-core-backend

# Deploy to AWS ECS, GCP Cloud Run, Azure Container Instances, etc.
```

---

## 🔐 CORS Configuration

Your backend **must** allow CORS from your frontend domain:

### Update backend/main.py:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://yourusername.github.io",
        "https://queztl-core.netlify.app",
        "https://queztl-core.vercel.app",
        "*"  # Or use wildcard (less secure)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🎯 Complete Deployment Flow

### 1. Deploy Backend First
```bash
# Option A: Render (easiest)
1. Push code to GitHub
2. Create Web Service on Render
3. Connect GitHub repo
4. Deploy automatically
5. Note your URL: https://queztl-core-api.onrender.com

# Option B: Docker Compose (self-hosted)
docker-compose up -d
# Expose port 8000 to internet
# Set up domain/SSL with nginx
```

### 2. Deploy Frontend
```bash
# Option A: Netlify (recommended)
netlify deploy --prod --dir=dashboard/public

# Option B: GitHub Pages
cp dashboard/public/3dmark-benchmark.html index.html
git add index.html
git commit -m "Deploy benchmark"
git push origin gh-pages

# Option C: Copy to your server
scp dashboard/public/3dmark-benchmark.html user@server:/var/www/html/
```

### 3. Configure API URL
```bash
# Open: https://your-frontend-url/3dmark-benchmark.html
# Enter: https://queztl-core-api.onrender.com
# Click: Test Connection
# See: ✅ Connected to API successfully!
```

### 4. Run Benchmarks
```bash
# Click: 🚀 RUN ALL BENCHMARKS
# Wait: ~30-60 seconds
# See: Grade A - EXCELLENT ⭐
```

---

## 🌍 Example Production URLs

### Frontend (Static)
- **GitHub Pages**: `https://salchicano loco.github.io/queztl-core/3dmark-benchmark.html`
- **Netlify**: `https://queztl-core.netlify.app/3dmark-benchmark.html`
- **Vercel**: `https://queztl-core.vercel.app/3dmark-benchmark.html`

### Backend (API)
- **Render**: `https://queztl-core-api.onrender.com`
- **Heroku**: `https://queztl-core-api.herokuapp.com`
- **Railway**: `https://queztl-core-api.railway.app`

---

## 💾 Local Storage Features

The benchmark uses browser localStorage to remember:
- ✅ **API URL** - No need to re-enter on every visit
- ✅ **Last test results** - View previous benchmark scores
- ✅ **Connection status** - Auto-reconnect to last working API

### Clear cached data:
```javascript
// Open browser console
localStorage.removeItem('queztl_api_url');
localStorage.clear(); // Clear all Queztl data
```

---

## 🔮 Future: Local Cache Optimization

Coming soon:
- **Service Worker** - Offline benchmark capability
- **IndexedDB** - Store historical benchmark data
- **PWA Support** - Install as desktop/mobile app
- **Result Sync** - Sync results across devices

---

## 🎨 Customization

### Change Default API URL
Edit line ~430 in `3dmark-benchmark.html`:
```javascript
let API_URL = localStorage.getItem('queztl_api_url') || 
              'https://YOUR-CUSTOM-API.com'; // Change this!
```

### Disable API URL Input (Lock to Production)
Remove the API configuration panel from the HTML (lines ~334-348).

### Add Custom Branding
```html
<!-- Add your logo -->
<div class="header">
    <img src="your-logo.png" style="height: 60px; margin-bottom: 10px;">
    <h1>🦅 Your Company - GPU Benchmark</h1>
</div>
```

---

## 📊 Analytics & Monitoring

### Track Benchmark Usage
```html
<!-- Add Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Monitor API Health
```bash
# Set up Uptime monitoring (free services)
- UptimeRobot: https://uptimerobot.com
- Pingdom: https://pingdom.com
- StatusCake: https://statuscake.com

# Monitor: https://queztl-core-api.onrender.com/health
```

---

## 🛠️ Troubleshooting

### ❌ "Cannot reach API"
1. Check API is running: `curl https://your-api.com/health`
2. Verify CORS headers are set
3. Check firewall/security groups
4. Test with: `curl -I https://your-api.com`

### ❌ "Mixed Content" (HTTP/HTTPS)
- Frontend on HTTPS must connect to HTTPS API
- Solution: Use HTTPS for both, or HTTP for both (local only)

### ❌ "CORS Error"
```python
# Add to backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporary fix
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### ❌ API Returns 404
- Verify endpoints exist: `/health`, `/api/power/benchmark`, etc.
- Check backend logs: `docker-compose logs backend`

---

## ✅ Deployment Checklist

- [ ] Backend deployed to production
- [ ] Backend `/health` endpoint working
- [ ] CORS headers configured
- [ ] Frontend deployed to static host
- [ ] API URL configured in frontend
- [ ] Test connection successful
- [ ] All 6 benchmarks passing
- [ ] SSL/HTTPS enabled (production)
- [ ] DNS configured (custom domain)
- [ ] Monitoring set up
- [ ] Share benchmark URL! 🎉

---

## 🎉 Success!

Your Queztl-Core 3DMark benchmark is now live on the web!

**Share it:**
```
🦅 Check out my GPU benchmark!
🔗 https://your-site.com/3dmark-benchmark.html
⭐ Grade A - EXCELLENT Performance!
```

**Next Steps:**
1. Run benchmarks and screenshot results
2. Share on social media / GitHub
3. Add to your portfolio / resume
4. Compare with commercial tools (3DMark, Geekbench)

---

## 📚 Resources

- **3DMark Benchmark**: [3dmark-benchmark.html](./dashboard/public/3dmark-benchmark.html)
- **Backend API**: [backend/main.py](./backend/main.py)
- **Docker Compose**: [docker-compose.yml](./docker-compose.yml)
- **Render Deploy**: [render.yaml](./render.yaml)
- **Netlify Config**: [netlify.toml](./netlify.toml)

---

Built with 🦅 by Queztl-Core Team
