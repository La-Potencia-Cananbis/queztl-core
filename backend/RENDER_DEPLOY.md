# 🚀 Deploy Queztl-Core Backend to Render

## Quick Deploy (5 minutes)

### Step 1: Push to GitHub

```bash
# Create a new repository on GitHub (github.com/new)
# Name it: queztl-core

# Then run:
git remote add origin https://github.com/YOUR_USERNAME/queztl-core.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. **Go to [render.com](https://render.com)** and sign up/login
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository: `YOUR_USERNAME/queztl-core`
4. Render will automatically detect `render.yaml` and create:
   - ✅ Backend API (Python)
   - ✅ PostgreSQL Database
   - ✅ Redis Cache

5. Click **"Apply"** and wait ~5 minutes for deployment

### Step 3: Get Your Backend URL

After deployment completes:
1. Go to your **queztl-core-backend** service
2. Copy the URL (e.g., `https://queztl-core-backend.onrender.com`)
3. Test it:
   ```bash
   curl https://YOUR-BACKEND-URL.onrender.com/api/health
   ```

### Step 4: Update Frontend

Update the dashboard to use your production backend:

```bash
# In your local terminal
cd /Users/xavasena/hive/dashboard
```

Create `.env.production`:
```bash
NEXT_PUBLIC_API_URL=https://YOUR-BACKEND-URL.onrender.com
NEXT_PUBLIC_WS_URL=wss://YOUR-BACKEND-URL.onrender.com
```

Then rebuild and redeploy:
```bash
npm run build
cd ..
netlify deploy --prod
```

### Step 5: Test Everything! 🎉

Visit **https://senzeni.netlify.app** and:
- ✅ Click "Measure Power"
- ✅ Run a stress test
- ✅ Generate creative scenarios
- ✅ Run benchmark suite

Everything should work! 🦅

---

## Alternative: Manual Render Setup

If blueprint doesn't work, do it manually:

### 1. Create Web Service

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo
4. Configure:
   - **Name**: `queztl-core-backend`
   - **Region**: Oregon (or closest to you)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

### 2. Add PostgreSQL Database

1. Click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `queztl-db`
   - **Database**: `queztl_core`
   - **Plan**: Free
3. After creation, go to your backend service
4. Add environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Copy from PostgreSQL "Internal Database URL"

### 3. Add Redis

1. Click **"New +"** → **"Redis"**
2. Configure:
   - **Name**: `queztl-redis`
   - **Plan**: Free
3. After creation, go to your backend service
4. Add environment variable:
   - **Key**: `REDIS_URL`
   - **Value**: Copy from Redis "Internal Redis URL"

### 4. Deploy!

Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## Environment Variables for Render

Your backend needs these (Render will auto-populate most):

```bash
DATABASE_URL=postgresql://user:pass@host:5432/queztl_core
REDIS_URL=redis://host:6379
PORT=10000  # Auto-set by Render
PYTHON_VERSION=3.11.0
```

---

## Troubleshooting

### "Application failed to start"
- Check logs in Render dashboard
- Verify `requirements.txt` has all dependencies
- Make sure `PORT` environment variable is used

### Database connection errors
- Ensure `DATABASE_URL` is set correctly
- Check if PostgreSQL service is running
- Verify database name is `queztl_core`

### CORS errors
- Backend already allows all origins (`*`)
- If issues persist, check browser console

### Slow first request
- Render free tier spins down after 15 min of inactivity
- First request takes ~30 seconds to wake up
- Subsequent requests are fast

---

## Cost

**Everything is FREE on Render:**
- ✅ Web Service (750 hours/month free)
- ✅ PostgreSQL (90 days free, then $7/month)
- ✅ Redis (30 days free, then $10/month)

**For production:**
- Consider upgrading to paid plans for:
  - No spin-down (instant responses)
  - More resources
  - Better performance

---

## Monitoring

### Check Backend Health
```bash
curl https://YOUR-BACKEND-URL.onrender.com/api/health
```

### View Logs
Go to Render dashboard → Your service → Logs

### Monitor Performance
```bash
curl https://YOUR-BACKEND-URL.onrender.com/api/power/measure
```

---

## Next Steps After Deployment

1. **Update CORS** (if needed):
   - Add your specific domains to `main.py`
   - Currently allows all (`*`)

2. **Add Authentication** (for production):
   - Implement API keys
   - Add JWT tokens
   - Rate limiting

3. **Set up monitoring**:
   - Use Render's built-in metrics
   - Set up uptime monitoring (UptimeRobot)

4. **Optimize performance**:
   - Upgrade to paid plan (no cold starts)
   - Add Redis caching
   - Database indexing

---

## Full Stack Architecture (After Deployment)

```
┌─────────────────────────────────────┐
│   Frontend (Netlify)                │
│   https://senzeni.netlify.app       │
│   - Next.js Static Site             │
│   - Dashboard UI                    │
└──────────────┬──────────────────────┘
               │
               │ API Requests
               ▼
┌─────────────────────────────────────┐
│   Backend (Render)                  │
│   https://your-backend.onrender.com │
│   - FastAPI + Python                │
│   - Power Measurement               │
│   - Stress Testing                  │
│   - Creative Training               │
└──────┬──────────────┬───────────────┘
       │              │
       ▼              ▼
┌─────────────┐ ┌─────────────┐
│ PostgreSQL  │ │   Redis     │
│  (Render)   │ │  (Render)   │
└─────────────┘ └─────────────┘
```

---

## Quick Commands Reference

```bash
# Push to GitHub
git add .
git commit -m "Update"
git push

# This auto-deploys to Render!

# Update frontend
cd dashboard
npm run build
cd ..
netlify deploy --prod

# Test backend
curl https://YOUR-URL.onrender.com/api/power/measure

# Run stress test
curl -X POST "https://YOUR-URL.onrender.com/api/power/stress-test?duration=10&intensity=light"
```

---

**Ready to deploy?** Follow Step 1 and create your GitHub repo! 🚀
