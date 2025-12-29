# 🦅 QuetzalCore Portal Deployment Guide

## What We Created

### 1. **QuetzalCore Portal** (Testing Dashboard)
   - **Location**: `/quetzalcore-portal/`
   - **Purpose**: Internal testing dashboard with ALL services integrated
   - **Features**:
     - Dashboard with real-time status
     - 5K Renderer (all resolutions, all scenes)
     - 3D Workload benchmark
     - GIS Studio status
     - Mining dashboard (placeholder)
     - VM Console (placeholder)
   - **Status**: ✅ Ready to deploy

### 2. **Public Landing Page**
   - **Location**: `/dashboard/public/index.html`
   - **Purpose**: Public-facing marketing site
   - **Status**: ✅ Already deployed to lapotenciacann.com

## 🚀 Deploy QuetzalCore Portal to Netlify

### Option A: New Netlify Site (Recommended)

1. **Go to Netlify**: https://app.netlify.com
2. **Add new site** → Import from Git
3. **Connect GitHub**: Select La-Potencia-Cananbis/queztl-core
4. **Configure build**:
   - Base directory: `quetzalcore-portal`
   - Build command: (leave empty or "echo 'no build needed'")
   - Publish directory: `.` (or leave empty)
5. **Deploy**
6. **Set custom domain**:
   - Go to Domain settings
   - Add custom domain: `portal.lapotenciacann.com`
   - Follow DNS instructions

### Option B: Quick Deploy Button

Netlify auto-detects `netlify.toml` in `/quetzalcore-portal/`

Just push to main (already done ✅) and Netlify will deploy if connected.

## 📋 Multi-Site URLs Architecture

Once deployed, your URLs will be:

- **Public Landing**: https://lapotenciacann.com
- **Testing Portal**: https://portal.lapotenciacann.com (or new Netlify URL)
- **Corporate**: https://senasaitech.com

## Future Individual Service Sites

When you're ready, create separate sites for:
- `render.lapotenciacann.com` - 5K Renderer only
- `gis.lapotenciacann.com` - GIS Studio only
- `3dmark.lapotenciacann.com` - 3D Benchmark only
- `mining.lapotenciacann.com` - Mining Dashboard only
- `vms.lapotenciacann.com` - VM Console only

## 🧪 Test Portal Locally

```bash
cd /Users/xavasena/hive/quetzalcore-portal
python3 -m http.server 8080
# Open http://localhost:8080
```

## ✅ What Works Right Now

The portal connects to your live backend at:
- https://queztl-core-backend.onrender.com

Features ready to test:
1. ✅ Dashboard with real-time backend status
2. ✅ 5K Renderer (all resolutions: 512x512 to 5120x2880)
3. ✅ 3D Workload benchmark
4. ✅ GIS Studio status check
5. ✅ "Test All Services" button

## 🎯 Next Steps

1. Deploy quetzalcore-portal to new Netlify site
2. Configure portal.lapotenciacann.com subdomain
3. Test all features on live portal
4. Keep public landing page separate on lapotenciacann.com
5. Later: Create individual service sites as needed

**Each service gets its own URL - no más throwing everything on one site! 🔥**
