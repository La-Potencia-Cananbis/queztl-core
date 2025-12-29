#!/bin/bash

# 🗺️ GIS STUDIO - QUICK REFERENCE CARD
# Everything you need to launch and use your beautiful dashboards

echo "
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║            🗺️ GIS STUDIO - QUICK REFERENCE & LAUNCH GUIDE 🚀             ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 QUICK START (3 STEPS)
═════════════════════════════════════════════════════════════════════════════

1. START THE SERVERS
   $ ./start-gis-studio.sh

2. OPEN YOUR BROWSER
   Option A (Live Testing):  http://localhost:8080/gis-studio-dashboard.html
   Option B (Info):          http://localhost:8080/gis-studio.html

3. ENJOY! ✨
   • Test the API endpoints
   • View your beautiful dashboards
   • Explore the UI animations


📊 WHAT YOU GET
═════════════════════════════════════════════════════════════════════════════

DASHBOARD 1: Interactive API Tester
   URL: http://localhost:8080/gis-studio-dashboard.html
   
   Features:
   ✓ 9 API endpoints (clickable buttons)
   ✓ Live endpoint testing
   ✓ Real-time JSON responses
   ✓ Pre-loaded example payloads
   ✓ Error handling
   ✓ Status indicators
   ✓ Responsive 2-column layout

DASHBOARD 2: Beautiful Information
   URL: http://localhost:8080/gis-studio.html
   
   Features:
   ✓ System overview
   ✓ Feature showcase
   ✓ API documentation
   ✓ Quick start guide
   ✓ Technology stack
   ✓ Smooth animations
   ✓ Scroll navigation


🔌 API ENDPOINTS
═════════════════════════════════════════════════════════════════════════════

Base URL: http://localhost:8000/api/gis/studio/

VALIDATION
   POST /validate/lidar      - Validate LiDAR point clouds
   POST /validate/dem        - Validate Digital Elevation Models

INTEGRATION
   POST /integrate/terrain   - Analyze terrain characteristics
   POST /integrate/magnetic  - Correlate magnetic anomalies

TRAINING
   POST /train/terrain       - Train terrain classifier
   POST /train/depth         - Train depth predictor
   POST /predict             - Make predictions

IMPROVEMENT
   POST /improve/feedback    - Submit feedback
   GET  /status              - Get system status


📁 IMPORTANT FILES
═════════════════════════════════════════════════════════════════════════════

DASHBOARDS
   frontend/gis-studio-dashboard.html  (27KB) - API tester
   frontend/gis-studio.html            (24KB) - Info page
   frontend/gis-studio.css             (1.6K) - Styles

SCRIPTS
   start-gis-studio.sh        (7.5KB) - Full server launcher
   launch-gis-studio.sh       (2.5KB) - Dashboard launcher

DOCUMENTATION
   GIS_STUDIO_DASHBOARD_GUIDE.md     - Design guide
   GIS_STUDIO_BEAUTY_EDITION.txt     - Feature showcase
   GIS_STUDIO_COMPLETE.md            - System docs


⚡ USEFUL COMMANDS
═════════════════════════════════════════════════════════════════════════════

START EVERYTHING
   ./start-gis-studio.sh

START JUST BACKEND
   python3 -m uvicorn backend.main:app --reload --port 8000

START JUST FRONTEND (if backend is already running)
   cd frontend && python3 -m http.server 8080

CHECK BACKEND HEALTH
   curl http://localhost:8000/api/health

GET SYSTEM STATUS
   curl http://localhost:8000/api/gis/studio/status

VIEW BACKEND LOGS
   tail -f /tmp/gis-studio-logs/backend.log

VIEW FRONTEND LOGS
   tail -f /tmp/gis-studio-logs/frontend.log

STOP SERVERS
   pkill -f uvicorn
   pkill -f 'http.server'
   
   OR (in the start-gis-studio.sh terminal):
   Ctrl+C


🎨 DESIGN HIGHLIGHTS
═════════════════════════════════════════════════════════════════════════════

Color Palette
   Primary Cyan (#00d4ff)      - Main interactions
   Secondary Magenta (#ff006e) - Accents
   Accent Purple (#8338ec)     - Highlights
   Success Green (#00d98e)     - Confirmations

Animations
   ✓ Fade-in on entrance
   ✓ Hover lift effects
   ✓ Pulsing status dots
   ✓ Background gradient shifts
   ✓ Smooth transitions (0.3s)

Typography
   ✓ Segoe UI Bold headers
   ✓ Gradient text fills
   ✓ Monospace code blocks
   ✓ High contrast text


📱 RESPONSIVE DESIGN
═════════════════════════════════════════════════════════════════════════════

Desktop (1400px+)
   • 2-column layouts
   • Full hover effects
   • Side-by-side content

Tablet (768px-1200px)
   • Adapted grid
   • Readable text
   • Touch-friendly buttons

Mobile (<768px)
   • Single column
   • Full-width content
   • Vertical scrolling
   • Touch optimized


🧪 TESTING THE API
═════════════════════════════════════════════════════════════════════════════

Method 1: Using Interactive Tester Dashboard
   1. Open http://localhost:8080/gis-studio-dashboard.html
   2. Click an endpoint in the left panel
   3. Edit payload (optional)
   4. Click 'Send Request'
   5. View JSON response

Method 2: Using curl Command
   # Validate LiDAR data
   curl -X POST http://localhost:8000/api/gis/studio/validate/lidar \\
     -H 'Content-Type: application/json' \\
     -d '{
       \"points\": [[0,0,100], [1,1,101], [2,2,102]],
       \"classification\": [2,2,2],
       \"intensity\": [128,129,127]
     }'

   # Check system status
   curl http://localhost:8000/api/gis/studio/status

Method 3: Using Swagger UI
   1. Visit http://localhost:8000/docs
   2. Find your endpoint
   3. Click 'Try it out'
   4. Enter parameters
   5. Click 'Execute'


🔐 TROUBLESHOOTING
═════════════════════════════════════════════════════════════════════════════

Problem: \"Port 8000 already in use\"
Solution: pkill -f uvicorn

Problem: \"Port 8080 already in use\"
Solution: pkill -f 'http.server'

Problem: \"Backend not responding\"
Solution: Check logs at /tmp/gis-studio-logs/backend.log

Problem: \"Module not found errors\"
Solution: Ensure all GIS modules are in backend/ directory

Problem: \"Dashboard shows 'Cannot connect'\"
Solution: Make sure backend is running (./start-gis-studio.sh)


✅ VERIFICATION CHECKLIST
═════════════════════════════════════════════════════════════════════════════

Before Launch
 □ Start script is executable (chmod +x start-gis-studio.sh)
 □ Backend files are present (backend/main.py, etc.)
 □ Frontend files are present (frontend/*.html)
 □ Ports 8000 and 8080 are available

After Launch
 □ Backend starts (look for \"Uvicorn running on...\")
 □ Frontend starts (look for \"Serving HTTP...\")
 □ Dashboard loads (no 404 errors)
 □ API endpoints are clickable
 □ Animations are smooth (no lag)
 □ Responsive design works (try F12 mobile view)
 □ Errors are handled gracefully


📚 ADDITIONAL RESOURCES
═════════════════════════════════════════════════════════════════════════════

GIS_STUDIO_DASHBOARD_GUIDE.md
   • Color palette documentation
   • Typography system guide
   • Component descriptions
   • Responsive design details

GIS_STUDIO_BEAUTY_EDITION.txt
   • Complete feature showcase
   • Design system details
   • Architecture overview
   • Success criteria

GIS_STUDIO_COMPLETE.md
   • Original system documentation
   • Setup instructions
   • Usage examples
   • API reference


🚀 DEPLOYMENT OPTIONS
═════════════════════════════════════════════════════════════════════════════

DEVELOPMENT (Recommended for first time)
   ./start-gis-studio.sh
   • Full server with logging
   • Beautiful status output
   • Auto-cleanup on start

PRODUCTION
   python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4

DOCKER (If available)
   docker-compose up -d

CLOUD DEPLOYMENT (AWS, GCP, Azure)
   • Use start-gis-studio.sh as base
   • Point frontend to cloud backend
   • Update API endpoint URLs


💡 TIPS & TRICKS
═════════════════════════════════════════════════════════════════════════════

1. Use the API Tester for quick testing
   • No setup required
   • All endpoints in one place
   • Instant feedback

2. Check the backend logs while testing
   • See what's happening
   • Debug issues quickly
   • Understand the flow

3. Use responsive design testing (F12)
   • Toggle device toolbar
   • Test on multiple screen sizes
   • Verify touch interactions

4. Bookmark both dashboard URLs
   • Tester: .../gis-studio-dashboard.html
   • Info: .../gis-studio.html

5. Keep terminal window visible
   • See real-time status
   • Monitor server health
   • Catch errors immediately


═════════════════════════════════════════════════════════════════════════════

🎉 YOU'RE ALL SET!
═════════════════════════════════════════════════════════════════════════════

Your GIS Studio is:
   ✅ Beautiful (professional design)
   ✅ Functional (all features work)
   ✅ Responsive (mobile-friendly)
   ✅ Well-documented (complete guides)
   ✅ Production-ready (tested & verified)

Just run:
   $ ./start-gis-studio.sh

And you're ready to go! 🚀✨

═════════════════════════════════════════════════════════════════════════════
¡Todo está jodido! (Everything is amazing!) 🔥
═════════════════════════════════════════════════════════════════════════════
"
