# 🎯 CRITICAL HANDOFF - Cluster Setup Required

**Date:** January 20, 2026  
**Status:** Code ready, cluster not operational  
**Urgency:** HIGH - User frustrated with circular progress

## 🚨 THE ACTUAL PROBLEM

User has **working code** but the **cluster itself isn't running**. Stop reinventing wheels. Use standard Linux cluster tools.

## 💻 Hardware Available

### Local Network (DHCP 192.168.1.x)
- **Beast** - 192.168.1.105
  - RTX 4090 GPU (NO NVIDIA DRIVERS INSTALLED)
  - 32GB RAM
  - Ubuntu Server 24.04 LTS
  - SSH: `ssh xava@192.168.1.105` (working)
  - Docker containers: ray-worker, qhp-redis

- **Sloth** - 192.168.1.102  
  - Ray head node
  - Ubuntu Server 24.04 LTS
  - SSH: NOT WORKING (needs key install via console)
  - Docker containers: ray-head

### Remote Site (DNS)
- **3-5 Optiplex machines** - DNS configured at remote location
  - Accessible via hostnames (optiplex1, optiplex2, etc.)
  - Status: UNKNOWN, not tested yet

### Laptop (Command Center)
- MacBook (macOS)
- DO NOT run compute here - orchestrate only

## 📦 What's Already Built (DON'T REBUILD)

### Distributed Execution System
✅ `backend/queztl_exec.py` - Remote command executor (SSH/Docker modes)  
✅ `backend/queztl_config.py` - Cluster configuration  
✅ `backend/distributed_agent_wrapper.py` - High-level agent spawning  
✅ `backend/queztl_agents.py` - Agent system with DNA/RNA patterns  
✅ `backend/setup_cluster.py` - Network discovery helper  
✅ `backend/quick_status.py` - Fast health checks  

**All tested and working on Beast.**

### NM Socialists Website
✅ `frontend-new/` - Complete working site (19 memes, weekly rotation)  
✅ Committed to Git  
❌ NOT deployed (user wants own hardware + Dynamic DNS)

## 🎯 WHAT NEEDS TO HAPPEN

### Phase 1: Get Cluster Running (PRIORITY)
**Don't write new code. Use existing cluster tools.**

```bash
# Option A: Ray Cluster (already started)
ssh xava@192.168.1.105
docker ps  # Check ray-worker status

ssh xava@192.168.1.102  # NEEDS SSH KEY FIRST
docker ps  # Check ray-head status

# Connect workers to head
ray start --address='192.168.1.102:6379' --redis-password='...'

# Option B: Kubernetes (if Ray isn't working)
# Install k3s on all nodes
curl -sfL https://get.k3s.io | sh -

# Option C: Slurm (traditional HPC)
# Install slurm-wlm on all nodes
apt-get install slurm-wlm

# Option D: Plain SSH + GNU Parallel (simplest)
# Just use parallel-ssh and GNU parallel
apt-get install parallel pssh
```

**PICK ONE. Don't build from scratch.**

### Phase 2: Fix Sloth SSH Access
```bash
# Manual console access required (user has physical access)
# 1. Login to Sloth via monitor/keyboard
# 2. Run on Sloth:
mkdir -p ~/.ssh
cat >> ~/.ssh/authorized_keys
# 3. Paste laptop's public key (from ~/.ssh/id_rsa.pub)
# 4. Test: ssh xava@192.168.1.102
```

### Phase 3: Deploy Website to Own Hardware
```bash
# User wants Dynamic DNS, NOT Netlify/Render

# Install nginx on Beast or Sloth
ssh xava@192.168.1.105
sudo apt-get install nginx
sudo cp -r ~/queztl-core/frontend-new/* /var/www/html/

# Setup Dynamic DNS (user will configure router)
# Common options:
# - DuckDNS (free)
# - No-IP (free tier)
# - Dynu (free)
# - Direct with domain registrar

# Point domain to home IP
# Router port forward: 80/443 -> Beast or Sloth
```

## 🔥 Critical Files for Next Agent

### Cluster Configuration
- `backend/queztl_config.py` - Node IPs, SSH settings
- `backend/queztl_exec.py` - Remote execution engine
- `backend/distributed_agent_wrapper.py` - Agent spawning wrapper

### Testing & Verification
- `backend/test_integration.py` - Full integration test
- `backend/quick_status.py` - Fast cluster check (<10 sec)
- `backend/quickstart_distributed.sh` - Quick demo

### Frontend (Ready to Deploy)
- `frontend-new/` - Complete NM Socialists site
- `frontend-new/netlify.toml` - Can adapt for nginx
- `frontend-new/assets/js/meme-rotator.js` - Weekly rotation logic

## ❌ What NOT to Do

1. **Don't rebuild the executor system** - it works
2. **Don't create new cluster software** - use Ray/k3s/Slurm/SSH
3. **Don't deploy to Netlify** - user wants own hardware
4. **Don't run compute on laptop** - it's command center only
5. **Don't write new documentation** - focus on making it work

## ✅ What TO Do

1. **Get Ray cluster operational** (it's already installed via Docker)
2. **Fix Sloth SSH** (manual key install via console)
3. **Test distributed execution** (use existing test_integration.py)
4. **Deploy website to nginx** on Beast or Sloth
5. **Help user configure Dynamic DNS** (DuckDNS, No-IP, etc.)

## 🔧 Quick Commands for Next Agent

### Check Current Cluster Status
```bash
# From laptop
cd ~/queztl-core
python3 backend/quick_status.py

# Expected output:
# Beast SSH: ✅
# Beast Docker: ✅  
# Sloth SSH: ❌ (known issue)
```

### Test Distributed Execution (Beast only for now)
```bash
cd ~/queztl-core
python3 backend/test_integration.py

# Should show:
# ✅ SSH execution working
# ✅ Docker execution working
# ✅ Agent spawning working
```

### Get Beast Ready for Web Hosting
```bash
ssh xava@192.168.1.105
sudo apt-get update
sudo apt-get install nginx
sudo systemctl status nginx

# Copy site
sudo rm -rf /var/www/html/*
sudo cp -r ~/queztl-core/frontend-new/* /var/www/html/
sudo chown -R www-data:www-data /var/www/html/

# Test locally
curl http://localhost/
```

### Fix Sloth SSH (Manual - User Present)
```bash
# On Sloth console (physical access):
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
# Paste: (get from laptop: cat ~/.ssh/id_rsa.pub)
chmod 600 ~/.ssh/authorized_keys

# From laptop:
ssh xava@192.168.1.102  # Should work now
```

### Check Ray Cluster
```bash
# Beast
ssh xava@192.168.1.105
docker exec ray-worker ray status

# Sloth (after SSH fixed)
ssh xava@192.168.1.102
docker exec ray-head ray status

# Access Ray dashboard
# http://192.168.1.102:8265
```

## 📋 Current Cluster State

### Working
- ✅ Beast SSH connection
- ✅ Beast Docker execution (ray-worker)
- ✅ Command executor (queztl_exec.py)
- ✅ Agent system (queztl_agents.py)
- ✅ Configuration system (queztl_config.py)
- ✅ NM Socialists site in Git

### Not Working / Unknown
- ❌ Sloth SSH access (needs manual key install)
- ❓ Ray cluster coordination (head<->worker)
- ❓ Optiplex remote nodes (not tested)
- ❓ NVIDIA drivers on Beast (needed for Stable Diffusion)
- ❌ Website deployment (user wants Dynamic DNS)

## 💡 Recommended Approach for Next Agent

### Hour 1: Get Cluster Running
1. Fix Sloth SSH (5 min - manual console)
2. Verify Ray cluster (10 min - check docker logs)
3. Test distributed execution (10 min - run test_integration.py)
4. If Ray broken, switch to simpler setup (20 min - GNU parallel + SSH)

### Hour 2: Deploy Website
1. Install nginx on Beast (5 min)
2. Copy frontend-new to /var/www/html (2 min)
3. Test locally (3 min)
4. Help user configure Dynamic DNS (20 min - DuckDNS setup)
5. Router port forwarding (10 min - user configures)
6. Test from external network (5 min)

### Hour 3: Integrate & Test
1. Run agents on cluster (15 min)
2. Verify distributed execution (15 min)
3. Test website serving (10 min)
4. Document current state (20 min)

**Total: 3 hours to working system**

## 🗣️ User Context

- **Frustrated** with circular progress - "spinning in circles"
- **Wants practical results** - "get it together"
- **Has budget** - "I will pay extra"
- **Knows networking** - "I will explain Dynamic DNS later"
- **Hardware ready** - All machines available
- **Clear goal** - Cluster working + website on own hardware

## 📞 Critical Questions for User

Before starting work, confirm:

1. **Cluster preference?** Ray (already installed) vs k3s vs Slurm vs plain SSH?
2. **Website host?** Beast (GPU machine) or Sloth (coordinator)?
3. **Dynamic DNS provider?** DuckDNS, No-IP, Dynu, or domain registrar?
4. **Port forwarding?** Can user access router to forward 80/443?
5. **Sloth console access?** Can user physically access to add SSH key?

## 🎯 Success Criteria

At end of next session, user should have:

1. ✅ **Cluster running** - All nodes communicating
2. ✅ **Distributed execution working** - Can spawn agents on remote nodes
3. ✅ **Website live** - Accessible from internet via Dynamic DNS
4. ✅ **No more wheel reinventing** - Using standard tools

## 📦 Files to Focus On

**Use these, don't rewrite:**
- `backend/queztl_exec.py` (340 lines) - Core executor
- `backend/distributed_agent_wrapper.py` (280 lines) - Agent wrapper
- `backend/queztl_config.py` (170 lines) - Configuration
- `frontend-new/` (complete site)

**Ignore these (nice-to-have, not critical):**
- Most markdown docs
- Old frontend files
- Monitoring scripts (cron already running)
- Test files (except test_integration.py)

## 🚀 Starting Command

```bash
# Next agent starts here:
cd ~/queztl-core
git pull origin main
python3 backend/quick_status.py

# Then fix whatever's broken (probably Sloth SSH)
# Then deploy website to nginx
# Then verify distributed execution works
# Done.
```

---

**TL;DR:** Stop writing new code. Fix Sloth SSH, get Ray cluster working (or use simpler setup), deploy website to nginx on Beast/Sloth, configure Dynamic DNS. That's it. 3 hours max.
