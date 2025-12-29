# Deployment Guide - Netlify

## Deploy Dashboard to Netlify

### Option 1: Deploy via Netlify CLI

1. **Install Netlify CLI**
   ```bash
   npm install -g netlify-cli
   ```

2. **Login to Netlify**
   ```bash
   netlify login
   ```

3. **Initialize and Deploy**
   ```bash
   cd dashboard
   netlify init
   netlify deploy --prod
   ```

### Option 2: Deploy via Git (Recommended)

1. **Push to GitHub/GitLab**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Hive Testing System"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Connect to Netlify**
   - Go to https://app.netlify.com/
   - Click "Add new site" → "Import an existing project"
   - Connect your Git repository
   - Configure build settings:
     - **Base directory**: `dashboard`
     - **Build command**: `npm run build`
     - **Publish directory**: `.next`

3. **Set Environment Variables**
   In Netlify Dashboard → Site settings → Environment variables:
   ```
   NEXT_PUBLIC_API_URL = https://your-backend-api.com
   NODE_VERSION = 20
   ```

### Option 3: Deploy with Drag & Drop

1. **Build locally**
   ```bash
   cd dashboard
   npm run build
   ```

2. **Deploy to Netlify**
   - Go to https://app.netlify.com/drop
   - Drag and drop the `.next` folder

## Deploy Backend API

The backend needs a different hosting solution since Netlify is for static sites. Options:

### Option 1: Railway.app (Recommended)
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
cd backend
railway init
railway up
```

### Option 2: Render.com
1. Go to https://render.com
2. Create new "Web Service"
3. Connect your repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables for DATABASE_URL and REDIS_URL

### Option 3: Fly.io
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy
cd backend
fly launch
fly deploy
```

### Option 4: Heroku
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create hive-backend

# Add PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# Add Redis
heroku addons:create heroku-redis:mini

# Deploy
git push heroku main
```

## Update Frontend to Use Deployed Backend

Once backend is deployed, update the environment variable:

**In Netlify:**
- Go to Site settings → Environment variables
- Update `NEXT_PUBLIC_API_URL` to your backend URL

**Or update directly in code:**
```bash
# In dashboard/.env.production
NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

## Database Setup for Production

### Option 1: Use Managed PostgreSQL
- **Railway**: Includes PostgreSQL addon
- **Render**: Offers managed PostgreSQL
- **Supabase**: Free PostgreSQL hosting
- **Neon**: Serverless PostgreSQL

### Option 2: Use Existing Services
Update `DATABASE_URL` environment variable:
```
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
```

## Final Checklist

- [ ] Backend deployed and running
- [ ] Database provisioned and accessible
- [ ] Redis provisioned (optional for MVP)
- [ ] Environment variables set in Netlify
- [ ] NEXT_PUBLIC_API_URL points to backend
- [ ] CORS configured in backend for Netlify domain
- [ ] Test all API endpoints from deployed frontend
- [ ] Monitor logs for any errors

## Quick Deploy Commands

```bash
# Build and test locally first
cd dashboard
npm run build
npm start

# Deploy to Netlify
netlify deploy --prod

# Check deployment
curl https://senzeni.netlify.app
```

## Troubleshooting

**Dashboard shows "Disconnected"?**
- Check NEXT_PUBLIC_API_URL is correct
- Verify backend CORS allows your Netlify domain
- Check browser console for errors

**API calls failing?**
- Ensure backend is deployed and running
- Check environment variables are set
- Verify database connection strings

**Build failing?**
- Check Node version (should be 20)
- Verify all dependencies are in package.json
- Check build logs in Netlify dashboard

## Cost Considerations

**Free Tier Options:**
- Netlify: 100GB bandwidth, 300 build minutes/month
- Railway: $5 credit/month, then pay-as-you-go
- Render: Free tier available (spins down after inactivity)
- Supabase: 500MB database free tier

---

Your site will be live at: **https://senzeni.netlify.app**
