# Queztl Email Backend - Cloud Deployment

## Quick Deploy Options

### Option 1: Railway (Easiest, Free Tier)
- **Cost**: Free tier (500 hours/month, restarts after sleep)
- **Time**: 5 minutes
- **Perfect for**: Demo & investor pitches

**Steps:**
1. Go to: https://railway.app/
2. Sign up with GitHub
3. New Project → Deploy from GitHub → Select `queztl-core`
4. Add environment variables:
   - `SENDGRID_API_KEY`: Your SendGrid key
   - `FROM_EMAIL`: salvador@senasaitech.com
   - `FROM_NAME`: Salvador Sena - Queztl
5. Railway auto-deploys!
6. Get URL: `https://your-app.railway.app`

### Option 2: Render (Reliable, Free)
- **Cost**: Free tier (spins down after 15 min idle)
- **Time**: 5 minutes
- **Perfect for**: Production-ready demo

**Steps:**
1. Go to: https://render.com/
2. New → Web Service → Connect GitHub → queztl-core
3. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn email_service:app --host 0.0.0.0 --port $PORT`
4. Add environment variables (same as above)
5. Deploy!
6. Get URL: `https://queztl-email.onrender.com`

### Option 3: Fly.io (Best Performance, Free)
- **Cost**: Free tier (3 VMs, 256MB RAM each)
- **Time**: 10 minutes
- **Perfect for**: Production

**Steps:**
1. Install: `brew install flyctl`
2. Sign up: `fly auth signup`
3. Deploy: `fly launch` (in backend folder)
4. Set secrets: `fly secrets set SENDGRID_API_KEY=...`
5. URL: `https://queztl-email.fly.dev`

## Recommended: Railway (Fastest Setup)

Railway is perfect because:
- ✅ No configuration needed
- ✅ Auto-detects Python
- ✅ Free tier sufficient for demos
- ✅ Easy to share URL with investors
- ✅ GitHub auto-deploy on push

After deploying, I'll update your email UI to use the live backend URL.
