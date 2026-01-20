# Distributed Failover Architecture

## 🎯 Overview

The Queztl cluster operates **independently** - your Mac can disconnect anytime. Each node can take on multiple roles with automatic failover.

## 🏗️ Architecture

### Role-Based System

Every service is a **role** that can run on any capable node:

```
┌─────────────────────────────────────────────────────────┐
│  ROLES (services that can run anywhere)                 │
├─────────────────────────────────────────────────────────┤
│  • web_server        - Serve website                    │
│  • contact_api       - Handle forms, email, database    │
│  • image_generator   - Generate images (GPU preferred)  │
│  • content_runner    - Auto-generate content            │
│  • storage_server    - File storage, backups            │
│  • coordinator       - Health checks, failover          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  NODES (machines that can host roles)                   │
├─────────────────────────────────────────────────────────┤
│  • Beast   (192.168.1.105) - GPU, compute              │
│  • Sloth   (192.168.1.102) - Storage, database         │
│  • Mac     (Optional)      - Command center             │
│  • Optiplex 1-5 (Coming)   - Distributed compute       │
└─────────────────────────────────────────────────────────┘
```

### Priority-Based Assignment

Each role has a **priority list** of preferred nodes:

```python
"web_server": {
    "priority": ["sloth", "beast", "mac"],  # Try Sloth first
}

"image_generator": {
    "priority": ["beast", "sloth"],  # Beast has GPU, preferred
}

"storage_server": {
    "priority": ["sloth", "beast"],  # Sloth has most disk
}
```

## 🔄 Failover Scenarios

### Scenario 1: Mac Disconnects

**Before:**
```
Mac:   web_server, contact_api
Beast: image_generator
Sloth: storage_server
```

**After (automatic failover):**
```
Mac:   [OFFLINE]
Beast: image_generator
Sloth: web_server, contact_api, storage_server ← Took over Mac's roles
```

### Scenario 2: Beast Goes Down

**Before:**
```
Beast: image_generator, content_runner
Sloth: web_server, contact_api, storage_server
```

**After:**
```
Beast: [OFFLINE]
Sloth: web_server, contact_api, storage_server, image_generator, content_runner
       ← Took over all roles
```

### Scenario 3: Normal Operation (All Online)

**Optimal distribution:**
```
Beast: image_generator, content_runner  ← GPU tasks
Sloth: web_server, contact_api, storage_server ← Always-on services
Mac:   coordinator (optional)  ← Command center
```

## 🚀 Setup on Each Node

### On Beast (192.168.1.105)

```bash
# Clone repo
cd ~
git clone https://github.com/La-Potencia-Cananbis/queztl-core.git
cd queztl-core

# Install dependencies
pip3 install fastapi uvicorn aiohttp python-multipart

# Start coordinator
python3 backend/distributed_roles.py --coordinator beast

# The coordinator will:
# 1. Detect which roles are missing
# 2. Assign roles to this node based on priority
# 3. Start those roles automatically
# 4. Monitor health and handle failovers
```

### On Sloth (192.168.1.102)

```bash
# Same setup
cd ~
git clone https://github.com/La-Potencia-Cananbis/queztl-core.git
cd queztl-core

pip3 install fastapi uvicorn aiohttp python-multipart

# Start coordinator
python3 backend/distributed_roles.py --coordinator sloth
```

### On Mac (Optional)

```bash
# Already cloned
cd ~/queztl-core

# Start coordinator (optional - cluster works without Mac)
python3 backend/distributed_roles.py --coordinator mac

# Or just check status
python3 backend/distributed_roles.py --status
```

## 🔍 Monitoring

### Check Cluster Status

```bash
# From any node or Mac
python3 backend/distributed_roles.py --status
```

Output:
```
╔═══════════════════════════════════════════════════════╗
║  🦅 QUEZTL CLUSTER STATUS                            ║
╚═══════════════════════════════════════════════════════╝

🔌 NODES:
   beast      (192.168.1.105) - ✅ ONLINE
   sloth      (192.168.1.102) - ✅ ONLINE
   mac        (192.168.1.100) - ❌ OFFLINE

🎭 ROLES:
   ✅ web_server         → sloth
   ✅ contact_api        → sloth
   ✅ image_generator    → beast
   ✅ content_runner     → beast
   ✅ storage_server     → sloth
   ✅ coordinator        → sloth

📊 SUMMARY:
   Nodes:  2/3 online
   Roles:  6/6 active
```

### API Endpoints

Each coordinator provides a REST API:

```bash
# Health check
curl http://192.168.1.105:8005/health

# Full status
curl http://192.168.1.105:8005/status

# List all roles
curl http://192.168.1.105:8005/roles

# List all nodes
curl http://192.168.1.105:8005/nodes

# Request a role start
curl -X POST http://192.168.1.105:8005/start_role \
  -H "Content-Type: application/json" \
  -d '{"role": "image_generator"}'
```

## ⚙️ Configuration

### Update Node IPs

Edit `backend/distributed_roles.py`:

```python
NODES = {
    "beast": {
        "ip": "192.168.1.105",  # Update if changed
        "capabilities": ["gpu", "compute", "storage"]
    },
    "sloth": {
        "ip": "192.168.1.102",  # Update if changed
        "capabilities": ["storage", "database", "compute"]
    },
    # Add Optiplexes as they join
    "optiplex1": {
        "ip": "192.168.1.110",
        "capabilities": ["compute"]
    }
}
```

### Customize Role Priorities

```python
ROLES = {
    "web_server": {
        "port": 8080,
        # Prefer Sloth (always on), then Beast, then Mac
        "priority": ["sloth", "beast", "mac"]
    }
}
```

## 🔧 Systemd Integration (Permanent Services)

### Create Service File

On each node, create `/etc/systemd/system/queztl-coordinator.service`:

```ini
[Unit]
Description=Queztl Distributed Coordinator
After=network.target

[Service]
Type=simple
User=xava
WorkingDirectory=/home/xava/queztl-core
ExecStart=/usr/bin/python3 backend/distributed_roles.py --coordinator $(hostname)
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Enable and Start

```bash
sudo systemctl daemon-reload
sudo systemctl enable queztl-coordinator
sudo systemctl start queztl-coordinator

# Check status
sudo systemctl status queztl-coordinator

# View logs
sudo journalctl -u queztl-coordinator -f
```

## 🎯 How Failover Works

### Health Monitoring

Every 30 seconds, each coordinator:
1. **Checks all nodes** - Are they responding?
2. **Checks all roles** - Is each service healthy?
3. **Detects failures** - Service down or node offline?
4. **Triggers failover** - Reassigns roles to healthy nodes

### Failover Process

```
1. Coordinator detects: image_generator down on Beast
   ↓
2. Checks priority list: ["beast", "sloth"]
   ↓
3. Beast offline, try Sloth
   ↓
4. Sloth online? ✅
   ↓
5. Request Sloth to start image_generator
   ↓
6. Wait 5 seconds, verify health
   ↓
7. ✅ Failover complete
```

### Recovery

When a node comes back online:
```
1. Coordinator detects: Beast is back online
   ↓
2. Check current assignments
   ↓
3. image_generator on Sloth (priority says Beast)
   ↓
4. Request Beast to start image_generator
   ↓
5. Once healthy, stop on Sloth
   ↓
6. ✅ Returned to optimal state
```

## 📊 Example Scenarios

### Normal Day - All Running

```
8:00 AM - All nodes online
Beast: image_generator, content_runner
Sloth: web_server, contact_api, storage_server
Mac:   coordinator (monitoring)
```

### You Leave with Mac

```
9:00 AM - Mac unplugs and leaves
Beast: image_generator, content_runner
Sloth: web_server, contact_api, storage_server, coordinator ← Takes over
```

**Website still accessible!** Sloth serves everything.

### Beast Power Outage

```
2:00 PM - Beast loses power
Sloth: web_server, contact_api, storage_server, coordinator, 
       image_generator ← Failover, content_runner ← Failover
```

**Everything still works!** Image generation slower (no GPU) but functional.

### Beast Returns

```
2:30 PM - Beast powers back on
Beast: image_generator ← Moved back, content_runner ← Moved back
Sloth: web_server, contact_api, storage_server, coordinator
```

**Automatic optimization!** GPU tasks return to Beast.

## 🔐 Production Best Practices

### 1. Persistent Configuration

Store config in `/etc/queztl/config.json`:

```json
{
  "nodes": {
    "beast": {"ip": "192.168.1.105", "priority": 1},
    "sloth": {"ip": "192.168.1.102", "priority": 2}
  },
  "health_check_interval": 30,
  "failover_timeout": 5
}
```

### 2. Logging

Centralize logs to Sloth:

```bash
# On each node
sudo rsyslog-config to send to Sloth
# Sloth stores all logs
```

### 3. Database Replication

```bash
# Sloth: Primary database
# Beast: Replicated copy (read-only)
# Automatic sync every minute
```

### 4. Static IP or DNS

```bash
# Add to /etc/hosts on each node
192.168.1.105  beast beast.local
192.168.1.102  sloth sloth.local

# Or use your router's DNS
```

## 🚀 Future: 7+ Node Cluster

When Optiplexes join:

```python
# Add to NODES
"optiplex1": {"ip": "192.168.1.110", "capabilities": ["compute"]},
"optiplex2": {"ip": "192.168.1.111", "capabilities": ["compute"]},
"optiplex3": {"ip": "192.168.1.112", "capabilities": ["compute"]},
"optiplex4": {"ip": "192.168.1.113", "capabilities": ["compute"]},
"optiplex5": {"ip": "192.168.1.114", "capabilities": ["compute"]},
```

Roles automatically distribute across all nodes!

## 📝 Commands Cheat Sheet

```bash
# Check cluster status
python3 backend/distributed_roles.py --status

# Start coordinator on this node
python3 backend/distributed_roles.py --coordinator $(hostname)

# Check specific role
curl http://192.168.1.105:8001/health  # image_generator
curl http://192.168.1.102:8080/        # web_server
curl http://192.168.1.102:8003/health  # contact_api

# View coordinator status
curl http://192.168.1.105:8005/status | jq

# Request manual failover
curl -X POST http://192.168.1.105:8005/start_role \
  -d '{"role": "web_server"}'
```

---

**Result:** Your cluster runs 24/7 without your Mac. Unplug and go, everything keeps working! 🚀
