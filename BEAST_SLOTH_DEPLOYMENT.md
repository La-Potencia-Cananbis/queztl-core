# ⚡ BEAST & SLOTH - BARE METAL DEPLOYMENT GUIDE

**Goal:** Maximum speed, minimum bloat  
**Timeline:** Ready before Tuesday when Optiplexes arrive  
**Strategy:** Lightweight OS + Agent workers only

---

## 🎯 RECOMMENDED: Ubuntu Server 24.04 LTS

**Why:**
- No GUI = 90% less RAM usage
- Fast boot (~5-10 seconds)
- Easy package management (APT)
- LTS = Stable until 2029
- Great hardware support

**What You Get:**
- 512MB base RAM usage (vs 2-4GB with desktop)
- All CPU/GPU for agents
- SSH access from laptop
- Docker support

---

## 📥 QUICK DEPLOYMENT STEPS

### 1. Download ISO (5 minutes)

```bash
# On your laptop
cd ~/Downloads
wget https://releases.ubuntu.com/24.04/ubuntu-24.04-live-server-amd64.iso

# Or direct download:
# https://ubuntu.com/download/server
```

### 2. Create Bootable USB (3 minutes)

**macOS:**
```bash
# Find USB drive
diskutil list

# Unmount it (replace disk2 with your USB)
diskutil unmountDisk /dev/disk2

# Write ISO (takes 2-3 minutes)
sudo dd if=~/Downloads/ubuntu-24.04-live-server-amd64.iso of=/dev/rdisk2 bs=1m

# Eject
diskutil eject /dev/disk2
```

**Or use GUI:**
- Download balenaEtcher: https://etcher.balena.io/
- Select ISO, select USB, flash

### 3. Install on Beast (10 minutes)

1. **Boot from USB**
   - Insert USB → Restart → Press F12/F2/Del for boot menu
   - Select USB drive

2. **Installation (choose these options):**
   - Language: English
   - Keyboard: US
   - Installation type: **Ubuntu Server (minimized)**
   - Network: Auto-configure DHCP
   - Storage: **Use entire disk** (wipes everything)
   - Profile:
     - Name: beast
     - Server name: beast
     - Username: queztl
     - Password: (your choice)
   - SSH: **Enable OpenSSH server** ✓
   - Featured snaps: **SKIP ALL** (deselect everything)

3. **Reboot**
   - Remove USB when prompted

### 4. Repeat for Sloth

Same steps, but:
- Server name: sloth
- Username: queztl

---

## 🚀 POST-INSTALL SETUP (5 minutes per machine)

### SSH from Your Laptop

```bash
# Find the IP address (look at Beast's screen after boot)
# Or from Beast's terminal: ip a

# SSH from laptop
ssh queztl@<beast-ip>
```

### Run This Setup Script

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essentials ONLY
sudo apt install -y \
    python3.12 python3.12-venv python3-pip \
    git curl wget htop \
    build-essential

# Disable bloat
sudo systemctl disable snapd --now 2>/dev/null || true
sudo systemctl disable cups --now 2>/dev/null || true
sudo systemctl disable bluetooth --now 2>/dev/null || true

# Install Docker (lightweight)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
rm get-docker.sh

# Clone queztl-core
cd ~
git clone https://github.com/La-Potencia-Cananbis/queztl-core.git
cd queztl-core

# Setup Python environment
python3 -m venv venv
source venv/bin/activate

# Install CPU-only PyTorch (faster download, no CUDA bloat)
pip install torch torchvision pillow numpy pandas --index-url https://download.pytorch.org/whl/cpu

# Test agents
python backend/queztl_agents.py --help

# Get IP for laptop access
echo ""
echo "✅ Setup complete!"
echo "Machine: $(hostname)"
echo "IP: $(hostname -I | awk '{print $1}')"
echo ""
```

### Save IPs

```bash
# From laptop, add to ~/.ssh/config
cat >> ~/.ssh/config << EOF

Host beast
    HostName <beast-ip>
    User queztl

Host sloth
    HostName <sloth-ip>
    User queztl
EOF

# Now you can SSH easily:
ssh beast
ssh sloth
```

---

## ⚡ PERFORMANCE SPECS (After Setup)

### Before (with GUI):
- RAM usage: 2-4 GB idle
- Boot time: 30-60 seconds
- Background services: 100+

### After (Server):
- RAM usage: 512 MB idle
- Boot time: 5-10 seconds
- Background services: ~20

### Available for Agents:
- **Beast**: All CPU cores, ~15.5GB RAM free
- **Sloth**: All CPU cores, RAM freed up
- No GUI overhead
- No desktop processes

---

## 🎮 CONTROL FROM LAPTOP

### Spawn Agents on Beast

```bash
# From laptop
ssh beast "cd queztl-core && source venv/bin/activate && python backend/queztl_agents.py --spawn trainer"

# Or interactive
ssh beast
cd queztl-core
source venv/bin/activate
python backend/queztl_agents.py --demo
```

### Spawn Agents on Sloth

```bash
ssh sloth "cd queztl-core && source venv/bin/activate && python backend/queztl_agents.py --spawn trainer"
```

### Monitor Both

```bash
# Terminal 1: Beast logs
ssh beast tail -f /tmp/queztl_agents/*/agent.log

# Terminal 2: Sloth logs  
ssh sloth tail -f /tmp/queztl_agents/*/agent.log

# Terminal 3: Resource usage
ssh beast htop
```

---

## 📊 DISK USAGE

### Ubuntu Server Minimal:
- Base install: ~2.5 GB
- Python + PyTorch: ~3 GB
- Queztl code: ~500 MB
- **Total: ~6 GB** (leaves 90%+ free on typical drives)

### Space for:
- Training datasets
- Model checkpoints
- Agent workspaces
- Logs

---

## 🔥 OPTIPLEX PREPARATION (Tuesday)

When you bring 4-5 Optiplexes:

1. **Clone USB** - Use same bootable USB
2. **Mass install** - Same steps for each
3. **Name them:**
   - optiplex1, optiplex2, optiplex3, etc.
   - Or: node1, node2, node3, worker1, worker2

4. **Auto-config script:**

```bash
# Run on each Optiplex
curl -fsSL https://raw.githubusercontent.com/La-Potencia-Cananbis/queztl-core/main/scripts/node-setup.sh | bash
```

5. **From laptop:**

```bash
# Deploy to all nodes
for node in beast sloth optiplex1 optiplex2 optiplex3; do
    ssh $node "cd queztl-core && git pull && source venv/bin/activate && python backend/queztl_agents.py --spawn trainer" &
done
```

---

## 🛠️ ALTERNATIVE: Keep Current OS

If you don't want to reinstall:

```bash
# On Beast/Sloth
bash ~/queztl-core/backend/DEPLOY_BEAST_SLOTH.sh

# Choose option 4: Strip down current OS
```

This will:
- Remove GUI bloat
- Disable unnecessary services  
- Keep existing files
- Free up RAM/CPU

**Pros:** Faster than reinstall  
**Cons:** Not as clean as fresh install

---

## 📋 CHECKLIST

Before Tuesday:

- [ ] Beast: Ubuntu Server installed
- [ ] Beast: Queztl code deployed
- [ ] Beast: Agents tested working
- [ ] Beast: SSH access from laptop
- [ ] Sloth: Ubuntu Server installed
- [ ] Sloth: Queztl code deployed
- [ ] Sloth: Agents tested working
- [ ] Sloth: SSH access from laptop
- [ ] Laptop: Can control both machines
- [ ] Laptop: Monitoring setup working

When Optiplexes arrive:

- [ ] USB installer ready
- [ ] Auto-setup script tested
- [ ] Network plan ready
- [ ] Laptop control workflow tested

---

## 🚨 TROUBLESHOOTING

### Can't SSH into Beast/Sloth

```bash
# On Beast/Sloth terminal:
sudo systemctl status ssh
sudo systemctl start ssh

# Check firewall
sudo ufw allow ssh
```

### Python/PyTorch issues

```bash
# Reinstall in venv
cd ~/queztl-core
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install torch torchvision pillow numpy --index-url https://download.pytorch.org/whl/cpu
```

### Out of disk space

```bash
# Clean up
sudo apt autoremove -y
sudo apt clean
docker system prune -af
```

---

## 🎯 EXPECTED TIMELINE

- **Now → Monday:** Beast + Sloth bare metal
- **Monday:** Test multi-node agent spawning
- **Tuesday AM:** Optiplexes arrive
- **Tuesday PM:** 7-node cluster running
- **This Week:** Full distributed agent network

---

## 🏁 SUCCESS CRITERIA

You'll know it's working when:

1. ✅ SSH from laptop to Beast/Sloth (no password with SSH keys)
2. ✅ Agents spawn and run on remote machines
3. ✅ Laptop stays cool (no local processing)
4. ✅ Can monitor all nodes from laptop
5. ✅ Beast/Sloth boot in <10 seconds
6. ✅ RAM usage <1GB idle

---

**Let's go! Want me to help with any specific step?**
