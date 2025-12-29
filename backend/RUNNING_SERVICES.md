# QuetzalCore Running Services Map
**Last Updated**: December 9, 2025 - 1:40 PM

## Active Services

### 1. Backend API (Port 8000) **MAIN API**
- **PID**: 3086
- **Command**: `uvicorn backend.main:app --port 8000`
- **Directory**: `/Users/xavasena/hive`
- **Access**: http://localhost:8000
- **Status**: ✅ RUNNING
- **Endpoints**:
  - `/api/workload/3d` - 3DMark benchmarks (10.7 GFLOPS) ✅ WORKING
  - `/api/gis/studio/*` - GIS Studio (has 500 error) ❌
  - `/health` - Health check ✅

### 1b. Email Service (Port 8001)
- **PID**: 19958
- **Command**: `python backend/email_service.py`
- **Directory**: `/Users/xavasena/hive`
- **Access**: http://localhost:8001
- **Status**: ✅ RUNNING (separate email microservice)

### 2. Dashboard (Port 3000)
- **PID**: 883 (node)
- **Command**: `npm run dev` (Next.js)
- **Directory**: `/Users/xavasena/hive/dashboard`
- **Access**: http://localhost:3000
- **Status**: ✅ RUNNING
- **Features**:
  - Metrics visualization
  - Training controls
  - 3D workload interface
  - GIS Studio UI
  - Power meter

### 3. VM Console (Port 9090)
- **PID**: 2423
- **Command**: `python3 console-server.py`
- **Directory**: `/Users/xavasena/hive/vms/test-vm`
- **Access**: http://localhost:9090
- **Status**: ✅ RUNNING
- **Purpose**: Web-based VM console with terminal, VNC, logs

### 4. QuetzalBrowser Frontend (Port 8080)
- **PID**: 2795
- **Command**: `python -m http.server 8080`
- **Directory**: `/Users/xavasena/hive`
- **Access**: http://localhost:8080
- **Status**: ✅ RUNNING
- **Serves**: `quetzal-browser.html` and assets

### 5. Mobile Dashboard (Port 9999)
- **PID**: 33942
- **Command**: `python mobile_dashboard.py`
- **Directory**: `/Users/xavasena/hive`
- **Access**: http://localhost:9999
- **Status**: ✅ RUNNING

### 6. Scrum Monitor (Port 9998)
- **PID**: 52092
- **Command**: `python autonomous_scrum_monitor.py`
- **Directory**: `/Users/xavasena/hive`
- **Access**: http://localhost:9998
- **Status**: ✅ RUNNING

### 7. Agent Runner (No Network Port)
- **PID**: 9079
- **Command**: `python agent_runner.py`
- **Directory**: `/Users/xavasena/hive`
- **Status**: ✅ RUNNING

## File Locations

### VM Console Files
```
/Users/xavasena/hive/vms/test-vm/
├── console-server.py         # Python HTTP server (port 9090)
├── console.html              # Web console interface
├── console.html.backup       # Backup before modifications
├── config.json               # VM configuration
├── STATUS                    # VM status file
├── ARCHITECTURE.md           # System architecture docs
├── SETUP_COMPLETE.md         # Setup documentation
└── VNC_GUIDE.md              # VNC setup guide
```

### Backend Files
```
/Users/xavasena/hive/backend/
├── main.py                   # FastAPI application
└── (other backend modules)
```

### Dashboard Files
```
/Users/xavasena/hive/dashboard/
├── src/app/page.tsx          # Main dashboard page
├── package.json
└── node_modules/
```

## Known Issues

### ❌ GIS Studio Status Endpoint (500 Error)
- **Endpoint**: `GET /api/gis/studio/status`
- **Error**: Internal Server Error
- **Cause**: `gis_trainer.models.keys()` failing
- **Location**: `/Users/xavasena/hive/backend/main.py`
- **Fix Needed**: Add try-except wrapper or check gis_trainer initialization

### ⚠️ VM Console Display
- Console HTML loads but may have display issues
- xterm.js integration attempted multiple times
- VNC connection attempts failing
- **Working backup**: `console.html.backup`

## DO NOT TOUCH (Working Components)

1. ✅ Dashboard (http://localhost:3000) - **LEAVE ALONE**
2. ✅ 3D Workload API - **WORKING PERFECTLY** (10.4 GFLOPS)
3. ✅ QuetzalBrowser frontend (http://localhost:8080)
4. ✅ Mobile Dashboard (http://localhost:9999)
5. ✅ Scrum Monitor (http://localhost:9998)
6. ✅ Agent Runner

## Restart Commands (If Needed)

### Backend (Port 8000)
```bash
pkill -f "uvicorn.*main:app"
cd /Users/xavasena/hive
source .venv/bin/activate
uvicorn backend.main:app --reload --port 8000 > backend.log 2>&1 &
```

### Email Service (Port 8001)
```bash
pkill -f "email_service"
cd /Users/xavasena/hive
python3 backend/email_service.py > email.log 2>&1 &
```

### Dashboard
```bash
cd /Users/xavasena/hive/dashboard
pkill -f "next dev"
npm run dev > /tmp/dashboard.log 2>&1 &
```

### VM Console
```bash
pkill -f "console-server"
cd /Users/xavasena/hive/vms/test-vm
python3 console-server.py > /tmp/console-server.log 2>&1 &
```

### QuetzalBrowser Frontend
```bash
pkill -f "http.server 8080"
cd /Users/xavasena/hive
python3 -m http.server 8080 > /tmp/http-8080.log 2>&1 &
```

## Testing Commands

### Test 3DMark
```bash
curl -X POST http://localhost:8001/api/workload/3d \
  -H "Content-Type: application/json" \
  -d '{"scene":"benchmark"}'
```

### Test Dashboard
```bash
curl -I http://localhost:3000
```

### Test VM Console
```bash
curl -I http://localhost:9090
```

### Test Backend Health
```bash
curl http://localhost:8001/health
```

## Architecture

```
User Browser
    │
    ├─→ http://localhost:3000 ──→ Next.js Dashboard
    │                              │
    │                              └─→ WebSocket ws://localhost:8001/ws/metrics
    │
    ├─→ http://localhost:8080 ──→ QuetzalBrowser Frontend
    │
    ├─→ http://localhost:9090 ──→ VM Console (test-vm-001)
    │
    ├─→ http://localhost:9999 ──→ Mobile Dashboard
    │
    └─→ http://localhost:9998 ──→ Scrum Monitor

Backend Services (Port 8001)
    ├─→ /api/workload/3d     (✅ Working)
    ├─→ /api/gis/studio/*    (❌ 500 Error)
    └─→ /api/email/*         (? Untested)

QuetzalCore Hypervisor
    └─→ VMs in /Users/xavasena/hive/vms/
        └─→ test-vm-001 (2048MB RAM, 2 vCPUs, 20GB disk)
```

## Notes for AI Assistant

**BEFORE MAKING ANY CHANGES:**
1. Read this document first
2. Check process list: `ps aux | grep -E "(python|node)"`
3. Check ports: `lsof -i -P | grep LISTEN`
4. Test endpoints with curl
5. Don't kill processes unless necessary
6. Don't modify working files without backup

**WHEN FIXING ISSUES:**
1. Create backup first: `cp file.ext file.ext.backup.$(date +%s)`
2. Test in isolation
3. Document changes in this file
4. Don't break working services

**PRIORITY:**
- Backend port is **8001** not 8000
- Dashboard on port **3000**
- VM Console on port **9090**
- QuetzalBrowser on port **8080**
- Everything else is working - don't touch!
