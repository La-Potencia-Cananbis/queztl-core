# 🏢 MULTI-SITE DEPLOYMENT ARCHITECTURE

**Goal:** Distributed agent cluster across two locations  
**Sites:** Current location + Lab  
**Timeline:** Immediate setup → Full lab deployment

---

## 🌍 NETWORK TOPOLOGY

```
┌─────────────────────────────────────────────────────────────────┐
│ SITE 1: CURRENT LOCATION (Temporary)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐                                              │
│  │   LAPTOP     │  ← Command Center (Your Mac)                 │
│  │ (Headnode)   │     - Issues commands                        │
│  └──────┬───────┘     - Monitors cluster                       │
│         │             - Git repo                               │
│         │                                                       │
│    ┌────┴────┐                                                 │
│    │         │                                                 │
│  ┌─▼───┐  ┌─▼───┐                                             │
│  │BEAST│  │SLOTH│  ← Worker nodes                             │
│  └─────┘  └─────┘                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ VPN / SSH Tunnel
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│ SITE 2: LAB (Future - Tuesday+)                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐                                              │
│  │  HEADNODE    │  ← Dedicated master controller               │
│  │ (Optiplex?)  │     - PostgreSQL database                    │
│  └──────┬───────┘     - Redis cache                            │
│         │             - API gateway                             │
│         │             - Dashboard server                        │
│         │                                                       │
│    ┌────┴─────┬──────┬──────┬──────┐                          │
│    │          │      │      │      │                           │
│  ┌─▼───┐  ┌──▼──┐ ┌─▼──┐ ┌─▼──┐ ┌─▼──┐                       │
│  │OPT-1│  │OPT-2│ │OPT-3│ │OPT-4│ │OPT-5│  ← Worker nodes     │
│  └─────┘  └─────┘ └────┘ └────┘ └────┘                        │
│                                                                 │
│  Total: 6 machines (1 headnode + 5 workers)                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 DEPLOYMENT PHASES

### Phase 1: Current Location (Now → Monday)
**Goal:** Test 2-node cluster before lab deployment

**Machines:**
- Laptop: Command center only (light control tasks)
- Beast: Worker node
- Sloth: Worker node

**Setup:**
```bash
# 1. Beast & Sloth
bash scripts/node-setup.sh

# 2. Laptop (SSH control)
bash scripts/setup-ssh.sh

# 3. Test
ssh beast "cd queztl-core && source venv/bin/activate && python backend/queztl_agents.py --spawn trainer"
```

---

### Phase 2: Lab Network Setup (Tuesday)
**Goal:** Dedicated headnode + 5 Optiplex workers

**Hardware:**
- 1 Optiplex → Headnode (or dedicated machine)
- 4-5 Optiplexes → Worker nodes
- Network switch
- (Optional) Beast & Sloth moved to lab

**Setup:**
```bash
# On headnode machine
bash scripts/headnode-setup.sh

# On each worker (Optiplex)
wget https://raw.githubusercontent.com/La-Potencia-Cananbis/queztl-core/main/scripts/node-setup.sh
bash node-setup.sh

# Register workers with headnode
bash scripts/add-worker.sh
# Enter each worker's IP
```

---

### Phase 3: Multi-Site Integration (Future)
**Goal:** Laptop at current location controls lab cluster

**Connection Options:**

#### Option A: VPN (Recommended)
```bash
# Install Tailscale (easiest)
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# All machines get virtual IPs
# Access lab headnode from anywhere
ssh headnode.tailscale
```

#### Option B: SSH Tunnel
```bash
# From laptop, tunnel to lab headnode
ssh -L 8000:localhost:8000 user@lab-headnode-public-ip

# Access dashboard
open http://localhost:8000
```

#### Option C: Public IP + Firewall
- Expose lab headnode with public IP
- Firewall rules for API access
- SSL/TLS for security

---

## 📋 MACHINE ROLES

### Headnode (Lab)
**Hardware:** Best Optiplex or dedicated machine  
**RAM:** 8GB+ recommended  
**Disk:** 100GB+ recommended

**Services:**
- PostgreSQL database (metrics, agent state)
- Redis cache (real-time data)
- FastAPI backend (REST API)
- Next.js dashboard (web UI)
- Nginx reverse proxy
- Job scheduler

**Setup:**
```bash
bash scripts/headnode-setup.sh
```

---

### Worker Nodes (All Optiplexes + Beast + Sloth)
**Hardware:** Any available machines  
**RAM:** 4GB+ minimum  
**Disk:** 50GB+ minimum

**Services:**
- Python agent runtime
- PyTorch (CPU-only for lightweight)
- Docker (optional, for containers)

**Setup:**
```bash
bash scripts/node-setup.sh
```

---

### Command Center (Your Laptop)
**Hardware:** Your Mac  
**Role:** Remote control and monitoring

**Services:**
- Git repository (code management)
- SSH client (remote access)
- Web browser (dashboard viewing)
- (Optional) Local dev environment

**Setup:**
```bash
bash scripts/setup-ssh.sh
```

---

## 🔧 CONFIGURATION FILES

### Headnode Config
`~/queztl-core/config/headnode.yaml`
```yaml
headnode:
  name: "lab-master"
  role: "master"
  ip: "192.168.1.100"
  
network:
  api_port: 8000
  dashboard_port: 3000
  websocket_port: 9999
  
database:
  host: "localhost"
  port: 5432
  name: "queztl_core"
  
workers:
  - name: "optiplex-1"
    ip: "192.168.1.101"
  - name: "optiplex-2"
    ip: "192.168.1.102"
  # ... etc
```

### Worker Config
`~/queztl-core/config/worker.yaml`
```yaml
worker:
  name: "optiplex-1"
  role: "worker"
  ip: "192.168.1.101"
  
headnode:
  host: "192.168.1.100"
  api_port: 8000
  
resources:
  cpu_cores: 4
  ram_gb: 8
  disk_gb: 500
```

---

## 🚀 DEPLOYMENT COMMANDS

### Deploy to All Workers
```bash
# From headnode
bash scripts/deploy-to-workers.sh
```

### Spawn Agents on Specific Worker
```bash
# From laptop or headnode
ssh optiplex-1 "cd queztl-core && source venv/bin/activate && python backend/queztl_agents.py --spawn trainer"
```

### Spawn Agents on All Workers
```bash
# From headnode
for worker in $(cat config/workers.txt); do
    ssh $worker "cd queztl-core && source venv/bin/activate && python backend/queztl_agents.py --spawn trainer" &
done
wait
```

### Monitor Cluster
```bash
# From headnode
bash scripts/headnode-status.sh

# From laptop (via SSH)
ssh headnode bash scripts/headnode-status.sh
```

---

## 🌐 NETWORK REQUIREMENTS

### Local Network (Lab)
- Switch/Router: All machines on same subnet
- DHCP: Or static IPs for each machine
- Suggested range: 192.168.1.100-120

### Remote Access (Laptop → Lab)
- Port forwarding: 8000 (API), 3000 (Dashboard)
- Or VPN: Tailscale, WireGuard, OpenVPN
- Or SSH tunnel: `ssh -L 8000:localhost:8000 headnode`

### Firewall Rules
```bash
# On headnode
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 8000/tcp  # API
sudo ufw allow 3000/tcp  # Dashboard
sudo ufw allow 9999/tcp  # WebSocket
sudo ufw enable
```

---

## 📊 HARDWARE PLANNING

### Current (Phase 1)
- 1 Laptop (command center)
- 2 Machines (Beast + Sloth workers)
- **Total: 3 machines**

### Lab (Phase 2)
- 1 Headnode
- 5 Optiplex workers
- **Total: 6 machines**

### Combined (Phase 3)
- 1 Laptop (remote control)
- 1 Headnode (lab master)
- 7 Workers (Beast + Sloth + 5 Optiplexes)
- **Total: 9 machines**

---

## ⚡ EXPECTED PERFORMANCE

### Phase 1 (2 workers)
- Concurrent agents: 4-8
- Training jobs: 2 parallel
- Good for: Testing, development

### Phase 2 (6 machines total)
- Concurrent agents: 20-30
- Training jobs: 10+ parallel
- Good for: Production workload

### Phase 3 (9 machines total)
- Concurrent agents: 40-50+
- Training jobs: 15+ parallel
- Good for: Heavy compute, distributed training

---

## 📝 CHECKLISTS

### Before Tuesday (Phase 1)
- [ ] Beast: Ubuntu Server installed
- [ ] Beast: Queztl setup complete
- [ ] Sloth: Ubuntu Server installed
- [ ] Sloth: Queztl setup complete
- [ ] Laptop: SSH keys configured
- [ ] Test: Agent spawning works
- [ ] Test: Remote control from laptop

### Tuesday Setup (Phase 2)
- [ ] Decide which Optiplex = Headnode
- [ ] Headnode: Ubuntu Server installed
- [ ] Headnode: Headnode setup script run
- [ ] Workers: Ubuntu Server installed (all)
- [ ] Workers: Node setup script run (all)
- [ ] Network: All machines on same subnet
- [ ] SSH: Headnode can access all workers
- [ ] Test: Spawn agents on all workers

### Lab Complete (Phase 3)
- [ ] VPN or SSH tunnel configured
- [ ] Laptop can access lab headnode
- [ ] Dashboard accessible remotely
- [ ] Agent deployment working
- [ ] Monitoring operational
- [ ] (Optional) Beast & Sloth moved to lab

---

## 🛠️ TROUBLESHOOTING

### Can't SSH to machines
```bash
# On target machine
sudo systemctl status ssh
sudo systemctl start ssh
sudo ufw allow 22/tcp
```

### Worker can't reach headnode
```bash
# Test connectivity
ping headnode-ip

# Check firewall
sudo ufw status

# Verify services
curl http://headnode-ip:8000/health
```

### Agent won't spawn
```bash
# Check Python environment
source venv/bin/activate
python backend/queztl_agents.py --help

# Check dependencies
pip list | grep torch

# Check logs
tail -f /tmp/queztl_agents/*/agent.log
```

---

## 📖 QUICK REFERENCE

### Setup Scripts
```bash
# Headnode
scripts/headnode-setup.sh

# Worker
scripts/node-setup.sh

# Laptop SSH
scripts/setup-ssh.sh

# Add worker to cluster
scripts/add-worker.sh

# Deploy code to workers
scripts/deploy-to-workers.sh

# Check status
scripts/headnode-status.sh
```

### Service Management
```bash
# Start headnode services
sudo systemctl start queztl-headnode

# Check status
sudo systemctl status queztl-headnode

# View logs
sudo journalctl -u queztl-headnode -f
```

---

**Ready to build your distributed agent cluster!** 🚀
