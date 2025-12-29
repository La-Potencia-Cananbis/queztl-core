# 🗺️ GIS Studio - Ubuntu VM Installation Guide

## Quick Start (5 Minutes)

### Prerequisites
- Ubuntu 20.04+ VM with SSH access
- At least 2GB RAM, 5GB disk space
- Internet connection
- Your Mac with GIS Studio files

---

## Option 1: Automated Deployment (Recommended) 🚀

### Step 1: Get Your VM IP Address
```bash
# On your Ubuntu VM, find the IP:
hostname -I
```

### Step 2: One-Command Deploy
From your Mac, run:
```bash
./deploy-to-ubuntu-vm.sh <your-vm-ip>
```

**Example:**
```bash
./deploy-to-ubuntu-vm.sh 192.168.1.100
```

That's it! The script will:
- ✅ Connect to your VM
- ✅ Upload all files
- ✅ Install all dependencies
- ✅ Configure systemd services
- ✅ Start the services
- ✅ Display access URLs

### Step 3: Access Your GIS Studio
After the script completes, open these URLs in your browser:

**Interactive API Tester:**
```
http://192.168.1.100:8080/gis-studio-dashboard.html
```

**Information Dashboard:**
```
http://192.168.1.100:8080/gis-studio.html
```

**API Documentation:**
```
http://192.168.1.100:8000/docs
```

---

## Option 2: Manual Step-by-Step Installation

### Step 1: SSH Into Your VM
```bash
ssh ubuntu@<your-vm-ip>
```

### Step 2: Create Project Directory
```bash
sudo mkdir -p /opt/gis-studio
sudo chown -R ubuntu:ubuntu /opt/gis-studio
cd /opt/gis-studio
```

### Step 3: Copy Files From Your Mac (In another terminal)
```bash
scp -r . ubuntu@<your-vm-ip>:/opt/gis-studio/
```

Or use rsync for faster transfer:
```bash
rsync -avz --delete . ubuntu@<your-vm-ip>:/opt/gis-studio/
```

### Step 4: Run Installation Script
Back in your VM SSH session:
```bash
cd /opt/gis-studio
chmod +x install-gis-studio-ubuntu.sh
./install-gis-studio-ubuntu.sh
```

### Step 5: Activate Virtual Environment
```bash
source /opt/gis-studio/venv/bin/activate
```

### Step 6: Start Services Manually
**Option A: Using systemd (Recommended)**
```bash
# Start services
sudo systemctl start gis-studio
sudo systemctl start gis-studio-frontend

# Enable at boot
sudo systemctl enable gis-studio
sudo systemctl enable gis-studio-frontend

# Check status
sudo systemctl status gis-studio
sudo systemctl status gis-studio-frontend
```

**Option B: Run directly**
```bash
# Terminal 1 - Backend
cd /opt/gis-studio
source venv/bin/activate
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd /opt/gis-studio/frontend
python3 -m http.server 8080
```

---

## Verification Checklist ✅

### Check Service Status
```bash
sudo systemctl status gis-studio
sudo systemctl status gis-studio-frontend
```

### Check Ports Are Open
```bash
sudo netstat -tlnp | grep -E '8000|8080'
# or
sudo ss -tlnp | grep -E '8000|8080'
```

### Test Backend Health
```bash
curl http://localhost:8000/api/health
# Should return: {"status":"ok"}
```

### Test GIS API
```bash
curl http://localhost:8000/api/gis/studio/status
# Should return JSON with system status
```

### View Logs
```bash
# Backend logs
sudo journalctl -u gis-studio -f

# Frontend logs
sudo journalctl -u gis-studio-frontend -f

# Or check log files directly
tail -f /tmp/gis-studio-logs/backend.log
tail -f /tmp/gis-studio-logs/frontend.log
```

---

## Troubleshooting

### Services Won't Start
```bash
# Check what's using the ports
sudo lsof -i :8000
sudo lsof -i :8080

# Kill any existing processes
sudo pkill -f uvicorn
sudo pkill -f "http.server"

# Restart services
sudo systemctl restart gis-studio gis-studio-frontend
```

### Import Errors
```bash
# Verify all Python packages are installed
source /opt/gis-studio/venv/bin/activate
pip list | grep -E "fastapi|uvicorn|numpy|scipy"

# Reinstall if needed
pip install fastapi uvicorn numpy scipy scikit-learn
```

### Cannot Connect to Backend
1. Check firewall allows port 8000:
   ```bash
   sudo ufw allow 8000/tcp
   sudo ufw allow 8080/tcp
   ```

2. Check if service is actually running:
   ```bash
   sudo systemctl status gis-studio
   ```

3. Test local connection:
   ```bash
   curl http://localhost:8000/api/health
   ```

### Frontend Not Serving Files
1. Check frontend directory exists:
   ```bash
   ls -la /opt/gis-studio/frontend/
   ```

2. Check HTTP server is running:
   ```bash
   ps aux | grep "http.server"
   ```

3. Restart frontend service:
   ```bash
   sudo systemctl restart gis-studio-frontend
   ```

---

## Common Commands

### Start Services
```bash
sudo systemctl start gis-studio gis-studio-frontend
```

### Stop Services
```bash
sudo systemctl stop gis-studio gis-studio-frontend
```

### Restart Services
```bash
sudo systemctl restart gis-studio gis-studio-frontend
```

### View Real-Time Logs
```bash
# Backend
sudo journalctl -u gis-studio -f

# Frontend
sudo journalctl -u gis-studio-frontend -f

# Both
sudo journalctl -u gis-studio -u gis-studio-frontend -f
```

### Check Service Status
```bash
sudo systemctl status gis-studio gis-studio-frontend
```

### Enable at Boot
```bash
sudo systemctl enable gis-studio gis-studio-frontend
```

### Disable at Boot
```bash
sudo systemctl disable gis-studio gis-studio-frontend
```

---

## Performance Optimization

### Increase Python Workers
If you have multiple cores, increase uvicorn workers:

Edit `/etc/systemd/system/gis-studio.service`:
```ini
ExecStart=/opt/gis-studio/venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Reload and restart:
```bash
sudo systemctl daemon-reload
sudo systemctl restart gis-studio
```

### Monitor Resource Usage
```bash
# Real-time monitoring
top

# Or use htop (if installed)
htop

# Check specific process
ps aux | grep uvicorn
```

---

## Deployment with Docker (Optional)

If you prefer containerized deployment:

```bash
# Check if Docker is available
docker --version

# Build image
docker build -t gis-studio:latest .

# Run container
docker run -d \
  --name gis-studio \
  -p 8000:8000 \
  -p 8080:8080 \
  gis-studio:latest
```

---

## Network Configuration

### Access from Other Machines
If accessing from a different machine on your network:

Replace `localhost` with your VM's IP address:
```
http://<vm-ip>:8080/gis-studio-dashboard.html
```

### Firewall Rules
```bash
# Allow ports
sudo ufw allow 8000/tcp
sudo ufw allow 8080/tcp

# Check firewall status
sudo ufw status
```

### Port Forwarding (if behind NAT)
If your VM is behind a router, configure port forwarding:
- External Port 8000 → VM IP:8000
- External Port 8080 → VM IP:8080

---

## Backup and Recovery

### Backup Your Installation
```bash
# Create backup
cd /opt
sudo tar -czf gis-studio-backup-$(date +%Y%m%d).tar.gz gis-studio/

# Move to safe location
sudo mv gis-studio-backup-*.tar.gz ~/backups/
```

### Restore from Backup
```bash
# Stop services
sudo systemctl stop gis-studio gis-studio-frontend

# Restore
cd /opt
sudo tar -xzf ~/backups/gis-studio-backup-20251208.tar.gz

# Restart services
sudo systemctl start gis-studio gis-studio-frontend
```

---

## Success Indicators ✅

Your installation is successful when:

1. ✅ Both services show "active (running)"
   ```bash
   sudo systemctl status gis-studio
   sudo systemctl status gis-studio-frontend
   ```

2. ✅ Backend responds to health check
   ```bash
   curl http://localhost:8000/api/health
   # Returns: {"status":"ok"}
   ```

3. ✅ Dashboards load in browser
   ```
   http://<vm-ip>:8080/gis-studio-dashboard.html
   ```

4. ✅ API endpoints return data
   ```bash
   curl http://localhost:8000/api/gis/studio/status
   ```

---

## Next Steps

### Test the API
1. Open the Interactive API Tester dashboard
2. Click any endpoint
3. Click "Send Request"
4. Verify you see JSON responses

### Monitor Performance
```bash
# Watch resource usage while testing
watch -n 1 'ps aux | grep -E "python|http"'
```

### Setup Auto-Restart
Services are already configured to auto-restart on failure. To verify:
```bash
# Kill backend process
sudo kill $(pgrep -f uvicorn)

# Service should restart automatically
sleep 3
sudo systemctl status gis-studio
```

---

## Support & Debugging

### Get Full System Info
```bash
./debug-gis-studio.sh  # if available on your system
```

### Collect Diagnostics
```bash
# System info
uname -a
python3 --version
pip --version

# Service info
sudo systemctl status gis-studio -l
systemctl show gis-studio

# Network info
sudo netstat -tlnp | grep -E '8000|8080'
```

### Common Errors & Solutions

**Error: "Module not found: backend"**
- Solution: Make sure backend directory is in `/opt/gis-studio/`
- Run: `ls -la /opt/gis-studio/backend/`

**Error: "Address already in use"**
- Solution: Kill the existing process
- Run: `sudo pkill -f uvicorn`

**Error: "Permission denied"**
- Solution: Fix permissions
- Run: `sudo chown -R ubuntu:ubuntu /opt/gis-studio`

---

## Version Information
- **GIS Studio:** 1.0.0 - Beauty Edition
- **Date:** December 8, 2025
- **Status:** ✅ Production Ready
- **OS:** Ubuntu 20.04+
- **Python:** 3.9+

---

## 🎉 You're Ready!

Your GIS Studio is now running on your Ubuntu VM. 

**Access it now:**
```
http://<your-vm-ip>:8080/gis-studio-dashboard.html
```

¡Todo está jodido! 🔥✨

---

**Questions?** Check the logs:
```bash
sudo journalctl -u gis-studio -f
```

**Everything working?** 🎯 Start testing your APIs!
