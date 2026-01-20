# 🔄 Distributed Failover - Quick Reference

## What Changed

**Before:** Mac runs everything  
**After:** Cluster runs independently with automatic failover

## 🎯 Key Concept

Every service is a **ROLE** that can run on any node. If a node goes down, roles automatically move to other nodes.

## 📋 Roles

| Role | Port | Priority | Purpose |
|------|------|----------|---------|
| web_server | 8080 | sloth → beast → mac | Serve website |
| contact_api | 8003 | sloth → beast → mac | Handle forms |
| image_generator | 8001 | beast → sloth | Generate images (GPU) |
| content_runner | 8004 | sloth → beast → mac | Auto-generate content |
| storage_server | 8000 | sloth → beast | File storage |
| coordinator | 8005 | sloth → beast → mac | Health checks, failover |

## 🚀 Quick Start

### 1. Deploy to Cluster

```bash
cd ~/queztl-core
./deploy-failover.sh
```

This will:
- ✅ SSH to Beast and Sloth
- ✅ Update repository
- ✅ Install dependencies
- ✅ Create systemd services
- ✅ Start coordinators
- ✅ Enable auto-start on boot

### 2. Check Status

```bash
python3 backend/distributed_roles.py --status
```

### 3. Unplug Your Mac

The cluster keeps running! 🎉

## 📊 Status Check Example

```
╔═══════════════════════════════════════════════════════╗
║  🦅 QUEZTL CLUSTER STATUS                            ║
╚═══════════════════════════════════════════════════════╝

🔌 NODES:
   beast      (192.168.1.105) - ✅ ONLINE
   sloth      (192.168.1.102) - ✅ ONLINE
   mac        (192.168.1.100) - ❌ OFFLINE  ← You unplugged

🎭 ROLES:
   ✅ web_server         → sloth     ← Still serving!
   ✅ contact_api        → sloth     ← Still working!
   ✅ image_generator    → beast     ← Still generating!
   ✅ content_runner     → beast     ← Still running!
   ✅ storage_server     → sloth     ← Still storing!
   ✅ coordinator        → sloth     ← Still monitoring!

📊 SUMMARY:
   Nodes:  2/3 online
   Roles:  6/6 active  ← Everything works!
```

## 🔄 Failover Examples

### Example 1: Beast Goes Down

**What happens:**
1. Coordinator on Sloth detects Beast is offline
2. Moves `image_generator` → Sloth
3. Moves `content_runner` → Sloth
4. All services still running!

**Website still accessible!**

### Example 2: Beast Comes Back

**What happens:**
1. Coordinator detects Beast is back online
2. Moves `image_generator` back → Beast (has GPU)
3. Moves `content_runner` back → Beast
4. Optimal distribution restored!

**Automatic optimization!**

### Example 3: Both Nodes Online, Mac Offline

**Normal operation:**
```
Beast: image_generator, content_runner
Sloth: web_server, contact_api, storage_server, coordinator
Mac:   [OFFLINE - on the go]
```

**Website fully functional from anywhere in the world!**

## 🔧 Management Commands

### Check Service Status

```bash
# On Beast
ssh xava@192.168.1.105 'sudo systemctl status queztl-coordinator'

# On Sloth
ssh xava@192.168.1.102 'sudo systemctl status queztl-coordinator'
```

### View Logs

```bash
# Live logs from Beast
ssh xava@192.168.1.105 'sudo journalctl -u queztl-coordinator -f'

# Live logs from Sloth
ssh xava@192.168.1.102 'sudo journalctl -u queztl-coordinator -f'
```

### Restart Services

```bash
# Restart Beast coordinator
ssh xava@192.168.1.105 'sudo systemctl restart queztl-coordinator'

# Restart Sloth coordinator
ssh xava@192.168.1.102 'sudo systemctl restart queztl-coordinator'
```

### Manual Failover Test

```bash
# Stop coordinator on Beast to trigger failover
ssh xava@192.168.1.105 'sudo systemctl stop queztl-coordinator'

# Watch roles move to Sloth
python3 backend/distributed_roles.py --status

# Start Beast back up
ssh xava@192.168.1.105 'sudo systemctl start queztl-coordinator'

# Watch roles return to optimal distribution
python3 backend/distributed_roles.py --status
```

## 🌐 API Access

### Coordinator API

```bash
# Get cluster status
curl http://192.168.1.105:8005/status | jq
curl http://192.168.1.102:8005/status | jq

# Check health
curl http://192.168.1.105:8005/health
curl http://192.168.1.102:8005/health

# List all roles
curl http://192.168.1.105:8005/roles | jq

# List all nodes
curl http://192.168.1.105:8005/nodes | jq

# Manually request role start
curl -X POST http://192.168.1.105:8005/start_role \
  -H "Content-Type: application/json" \
  -d '{"role": "image_generator"}'
```

### Service Endpoints

```bash
# Website
curl http://192.168.1.102:8080

# Contact API
curl http://192.168.1.102:8003/health

# Image Generator
curl http://192.168.1.105:8001/health

# Storage Server
curl http://192.168.1.102:8000/health
```

## 🔐 Auto-Start on Boot

Services automatically start when nodes boot up:

```bash
# Enabled by systemd
sudo systemctl enable queztl-coordinator

# Check if enabled
systemctl is-enabled queztl-coordinator
```

**Result:** Power cycle any node, it rejoins the cluster automatically!

## 📱 Mobile Monitoring

Access from your phone while Mac is away:

```bash
# If you have DynDNS set up:
https://your-domain.duckdns.org:8005/status

# Or via local IP if on same network:
http://192.168.1.102:8005/status
```

## 🎯 Testing Checklist

```bash
# 1. Deploy
./deploy-failover.sh

# 2. Check status
python3 backend/distributed_roles.py --status

# 3. Unplug Mac
# (physically disconnect or turn off WiFi)

# 4. Check website still works
curl http://192.168.1.102:8080  # Should work!

# 5. Plug Mac back in

# 6. Check status again
python3 backend/distributed_roles.py --status

# ✅ Everything still running!
```

## 🚨 Troubleshooting

### "Cannot SSH to node"

```bash
# Set up SSH key
ssh-copy-id xava@192.168.1.105
ssh-copy-id xava@192.168.1.102

# Test connection
ssh xava@192.168.1.105 "echo 'SSH OK'"
```

### "Service not starting"

```bash
# Check logs
ssh xava@192.168.1.105 'sudo journalctl -u queztl-coordinator -n 50'

# Check if port is already in use
ssh xava@192.168.1.105 'sudo lsof -i :8005'

# Restart service
ssh xava@192.168.1.105 'sudo systemctl restart queztl-coordinator'
```

### "Role not failing over"

```bash
# Check if both coordinators are running
curl http://192.168.1.105:8005/health
curl http://192.168.1.102:8005/health

# Check coordinator logs
ssh xava@192.168.1.105 'sudo journalctl -u queztl-coordinator -f'
```

### "Dependencies missing"

```bash
# Reinstall on node
ssh xava@192.168.1.105
cd ~/queztl-core
pip3 install fastapi uvicorn aiohttp python-multipart
```

## 📈 Future: Add More Nodes

When Optiplexes join:

```bash
# Edit backend/distributed_roles.py
# Add to NODES dictionary:
"optiplex1": {
    "ip": "192.168.1.110",
    "capabilities": ["compute"]
},
"optiplex2": {
    "ip": "192.168.1.111",
    "capabilities": ["compute"]
}

# Deploy to new nodes
./deploy-failover.sh  # Will need updating for new IPs

# Roles automatically distribute!
```

## 💡 Benefits

✅ **Independence** - Cluster runs without Mac  
✅ **Resilience** - Automatic failover  
✅ **Optimization** - Roles return to best nodes  
✅ **Scalability** - Easy to add more nodes  
✅ **Monitoring** - Real-time status checks  
✅ **Zero Downtime** - Services keep running  

## 📚 Documentation

- **Full Guide:** `DISTRIBUTED_FAILOVER.md`
- **Code:** `backend/distributed_roles.py`
- **Deploy Script:** `deploy-failover.sh`

---

**Your cluster is now autonomous! 🚀**

Unplug your Mac, go anywhere, cluster keeps running 24/7.
