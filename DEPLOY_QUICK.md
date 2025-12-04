# Quick Deploy to Netlify

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/yourusername/hive)

## Automated Deployment Steps

### 1. Deploy Dashboard to Netlify (Frontend)

**Option A: Via Netlify UI (Easiest)**
1. Click the "Deploy to Netlify" button above
2. Connect your GitHub account
3. Configure these settings:
   - **Base directory**: `dashboard`
   - **Build command**: `npm run build`
   - **Publish directory**: `.next`
4. Add environment variable:
   - `NEXT_PUBLIC_API_URL` = (your backend URL - add after step 2)

**Option B: Via CLI**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
./deploy-netlify.sh
```

### 2. Deploy Backend to Railway (Backend API)

**Option A: Via Railway UI (Recommended)**
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add these services:
   - **Web Service**: Python app (auto-detected)
   - **PostgreSQL**: Click "New" → "Database" → "PostgreSQL"
   - **Redis**: Click "New" → "Database" → "Redis"
5. Set environment variables (automatically set by Railway):
   - `DATABASE_URL` (auto-populated)
   - `REDIS_URL` (auto-populated)
6. Railway will provide your backend URL (e.g., `https://hive-backend.up.railway.app`)

**Option B: Via CLI**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy backend
cd backend
railway init
railway up

# Get your URL
railway domain
```

### 3. Connect Frontend to Backend

1. Copy your Railway backend URL
2. In Netlify:
   - Go to Site settings → Environment variables
   - Update `NEXT_PUBLIC_API_URL` to your Railway URL
3. Redeploy Netlify site

### 4. Update CORS in Backend

Add your Netlify domain to CORS allowed origins:

```python
# In backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://senzeni.netlify.app",  # Your Netlify domain
        "http://localhost:3000",         # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Push changes and Railway will auto-deploy.

## Alternative Backend Hosting Options

### Render.com (Free Tier Available)
```bash
# 1. Create account at render.com
# 2. New Web Service → Connect Repository
# 3. Configure:
#    - Build Command: pip install -r requirements.txt
#    - Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
# 4. Add PostgreSQL and Redis from Render dashboard
```

### Fly.io (Good for Global Edge)
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy
cd backend
fly launch
fly deploy

# Get URL
fly info
```

### Heroku (Classic Option)
```bash
# Install Heroku CLI
brew tap heroku/brew && brew install heroku

# Login and create app
heroku login
heroku create hive-backend

# Add addons
heroku addons:create heroku-postgresql:essential-0
heroku addons:create heroku-redis:mini

# Deploy
git push heroku main

# Get URL
heroku info
```

## Post-Deployment Checklist

- [ ] ✅ Dashboard deployed to Netlify
- [ ] ✅ Backend deployed (Railway/Render/Fly/Heroku)
- [ ] ✅ Database provisioned and connected
- [ ] ✅ Redis provisioned (optional)
- [ ] ✅ Environment variables configured
- [ ] ✅ CORS updated with Netlify domain
- [ ] ✅ Test all API endpoints
- [ ] ✅ Test WebSocket connection
- [ ] ✅ Monitor logs for errors

## Testing Your Deployment

```bash
# Test backend health
curl https://your-backend.railway.app/api/health

# Test frontend
curl https://senzeni.netlify.app

# Monitor logs
# Railway: railway logs
# Netlify: netlify logs
```

## Monitoring & Debugging

**Backend Logs:**
- Railway: `railway logs --follow`
- Render: View in dashboard
- Fly.io: `fly logs`

**Frontend Logs:**
- Netlify: Site settings → Functions → View logs
- Browser console: Press F12

**Common Issues:**

1. **"Disconnected" status**
   - Check `NEXT_PUBLIC_API_URL` is correct
   - Verify CORS allows Netlify domain
   - Check backend is running

2. **Database connection errors**
   - Verify `DATABASE_URL` is set
   - Check database is provisioned
   - Review backend logs

3. **Build failures**
   - Check Node version (should be 20)
   - Verify all dependencies in package.json
   - Review build logs

## Cost Summary

**Free Tier (Total: $0/month)**
- Netlify: Free (100GB bandwidth)
- Railway: $5 credit/month (then pay-as-you-go ~$5-10/month)
- Or Render: Free tier (sleeps after inactivity)

**Production Tier (~$20-30/month)**
- Netlify: $19/month (Pro plan)
- Railway: ~$10-15/month
- Or managed services with better guarantees

## Your Live URLs

After deployment:
- **Dashboard**: https://senzeni.netlify.app
- **Backend**: https://your-backend.railway.app
- **API Docs**: https://your-backend.railway.app/docs

---

**Need Help?** Check logs and refer to [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.
