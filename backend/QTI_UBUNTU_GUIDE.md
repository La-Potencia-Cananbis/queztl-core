# 🗺️ Quetzal Terminal Interface (QTI) - Ubuntu Build System

## Overview

**QTI** is a complete system for building and managing Quetzal on multiple Linux distributions. It provides:

- **Terminal UI (TUI)** for interactive distro selection
- **Automated builders** for 6+ Linux distributions
- **One-command rebuild** capability for your BM (Build Manager)
- **Service management** with systemd
- **GIS Studio integration** on any distro

---

## What You Get

### 1. **QTI Terminal Application** (`qti_ubuntu_app.py`)

Interactive terminal UI that lets you:
- ✅ Select from 6 distro options
- ✅ View distro specs (package manager, kernel, size, etc.)
- ✅ Start automated builds
- ✅ Monitor build progress
- ✅ Save build configurations

**Supported Distros:**
- Ubuntu 24.04 LTS (2GB, apt, systemd)
- Debian 12 Bookworm (2GB, apt, systemd)
- Alpine Linux 3.19 (170MB, apk, openrc) ⚡ Ultra-minimal
- Arch Linux (1GB, pacman, systemd) 🔥 Cutting edge
- Fedora 40 (2GB, dnf, systemd) 🤖 ML/AI optimized
- NixOS 24.05 (3GB, nix, systemd) 📦 Declarative

### 2. **Distro Builder Script** (`quetzal_distro_builder.sh`)

Fully automated installer that:
- Detects your current distro
- Installs distro-specific dependencies
- Clones Quetzal Core repo
- Sets up Python venv
- Configures GIS Studio
- Creates systemd services
- Starts services automatically

---

## Installation

### Option 1: On Ubuntu (Recommended)

```bash
# Clone or download QTI
git clone https://github.com/SalChicanoLoco/queztl-core.git
cd queztl-core

# Run the installer
sudo bash quetzal_distro_builder.sh
```

### Option 2: Run QTI UI First

```bash
python3 qti_ubuntu_app.py
```

This opens an interactive menu where you can:
1. See all available distros
2. View specs and requirements
3. Start an automated build
4. Monitor build progress in real-time

---

## Supported Distros & Their Advantages

### 🐧 Ubuntu 24.04 LTS (Default)
**Best for:** General purpose, most packages available
- Package manager: apt
- Kernel: 6.8
- Base size: 2GB
- LTS support: 5 years

```bash
sudo bash quetzal_distro_builder.sh  # Detects Ubuntu automatically
```

### 🔴 Alpine Linux 3.19 (Fastest!)
**Best for:** Minimal systems, fast builds, IoT/embedded
- Package manager: apk
- Kernel: 6.6
- Base size: **170MB** (!)
- Init: openrc (super lightweight)

**Pros:**
- 10x smaller than Ubuntu
- Blazing fast boot
- Perfect for edge computing
- Minimal attack surface

**Install on Alpine:**
```bash
apk add curl git bash
curl -O https://raw.githubusercontent.com/.../quetzal_distro_builder.sh
bash quetzal_distro_builder.sh
```

### 🎯 Arch Linux (Cutting Edge)
**Best for:** Rolling release, latest packages, developers
- Package manager: pacman
- Kernel: latest
- Base size: 1GB
- Updates: rolling

```bash
pacman -S curl git
bash quetzal_distro_builder.sh
```

### 🎨 Fedora 40 (AI/ML Optimized)
**Best for:** Machine learning, cutting edge features
- Package manager: dnf
- Kernel: 6.8
- Base size: 2GB
- Great ML/AI tooling

```bash
sudo bash quetzal_distro_builder.sh
```

### 🔧 NixOS 24.05 (Reproducible)
**Best for:** Declarative config, reproducible builds
- Package manager: nix
- Kernel: 6.6
- Base size: 3GB
- Reproducible: 100%

**Install:** Requires manual configuration.nix edits

### 🎁 Debian 12 Bookworm (Stable)
**Best for:** Production, long-term stability
- Package manager: apt
- Kernel: 6.1
- Base size: 2GB
- Support: 3 years

```bash
sudo bash quetzal_distro_builder.sh
```

---

## Usage

### Interactive Mode (Recommended for First-Time)

```bash
python3 qti_ubuntu_app.py
```

You'll see:
```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🗺️  QUETZAL TERMINAL INTERFACE (QTI) - Ubuntu        ║
║              Distro Builder & Manager                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

→ 1. Build New System
  2. Select Distro
  3. View Current System
  4. System Status
  5. Settings
  Q. Quit
```

Navigate with arrow keys, press ENTER to select.

### Automated Mode (One-Command)

```bash
# Auto-detect and install on current distro
sudo bash quetzal_distro_builder.sh

# Custom build directory
BUILD_DIR=/custom/path sudo bash quetzal_distro_builder.sh

# Custom install directory
INSTALL_DIR=/usr/local/quetzal sudo bash quetzal_distro_builder.sh
```

---

## What Gets Installed

### System Packages (Distro-Specific)
```
✓ Python 3 + pip
✓ Git & build tools
✓ GCC/G++ compiler
✓ NumPy, SciPy (scientific computing)
✓ GDAL, GEOS, Proj (GIS libraries)
✓ PostgreSQL client + SQLite
✓ Systemd (on most distros)
```

### Quetzal Core
```
✓ Backend API (FastAPI)
✓ GIS modules (terrain, validation, analysis)
✓ QP Protocol handler (binary WebSocket)
✓ Auto-scaling infrastructure
✓ Memory optimizer
✓ Security monitoring
```

### GIS Studio
```
✓ Frontend dashboards (HTML5)
✓ API tester interface
✓ System status monitor
✓ Real-time WebSocket updates
```

---

## After Installation

### Start Services

```bash
# Start both services
sudo systemctl start gis-studio gis-studio-frontend

# Enable auto-start on boot
sudo systemctl enable gis-studio gis-studio-frontend

# Check status
sudo systemctl status gis-studio gis-studio-frontend
```

### Access Your System

```
🚀 Frontend Dashboard: http://localhost:8080/gis-studio-dashboard.html
🎨 Info Page: http://localhost:8080/gis-studio.html
📚 API Docs: http://localhost:8000/docs
⚙️  Backend API: http://localhost:8000/api/gis/studio/status
```

### View Logs

```bash
# Backend logs
sudo journalctl -u gis-studio -f

# Frontend logs
sudo journalctl -u gis-studio-frontend -f

# All Quetzal logs
sudo journalctl -u gis-studio* -f
```

### Rebuild on Different Distro

1. **Save current config** (via QTI menu)
2. **Boot new distro** or use VM/container
3. **Run builder script** on new distro
4. **Restore config** (optional)

---

## Performance Comparison

| Distro | Boot Time | Size | Packages | Updates | Best For |
|--------|-----------|------|----------|---------|----------|
| Alpine | ⚡⚡⚡ 2s | 170MB | Limited | Manual | Edge/IoT |
| Arch | ⚡⚡ 5s | 1GB | Extensive | Rolling | Dev |
| Debian | ⚡ 10s | 2GB | Stable | ~3y | Prod |
| Fedora | ⚡ 8s | 2GB | Cutting edge | ~13mo | ML/AI |
| NixOS | ⚡ 7s | 3GB | Functional | Rolling | Reproducible |
| Ubuntu | ⚡ 10s | 2GB | Extensive | 5y LTS | General |

---

## System Requirements

### Minimum
- CPU: 2+ cores
- RAM: 1GB (Alpine), 2GB+ (others)
- Disk: 5GB free
- Network: Internet for package download

### Recommended
- CPU: 4+ cores
- RAM: 4GB+
- Disk: 20GB+ free
- SSD for faster builds

---

## Troubleshooting

### Build Fails on Dependencies
```bash
# Clean build directory
rm -rf /tmp/quetzal-build

# Retry
sudo bash quetzal_distro_builder.sh
```

### Services Won't Start
```bash
# Check error
sudo journalctl -u gis-studio -n 50

# Reinstall systemd units
sudo systemctl daemon-reload
sudo systemctl start gis-studio
```

### QTI Won't Run
```bash
# Install Python curses support
pip3 install windows-curses  # Windows only

# On Linux, curses is built-in
python3 qti_ubuntu_app.py
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Try again
sudo systemctl restart gis-studio
```

---

## Advanced Options

### Custom Installation Paths

```bash
export QUETZAL_REPO="https://your.repo/quetzal-core.git"
export BUILD_DIR="/custom/build"
export INSTALL_DIR="/custom/install"
sudo bash quetzal_distro_builder.sh
```

### Build in Container

```bash
# Alpine container
docker run -it alpine:latest bash quetzal_distro_builder.sh

# Ubuntu container
docker run -it ubuntu:24.04 bash quetzal_distro_builder.sh
```

### Automated Rebuilds

Create a cron job:
```bash
0 2 * * 0 cd /opt/quetzal && sudo -u quetzal git pull && sudo systemctl restart gis-studio
```

---

## Why Rebuild Your BM?

### Benefits of Different Distros

**Alpine Linux:**
- 🚀 10x faster boot
- 💾 10x less disk
- 🔒 Smaller attack surface
- Perfect for: Edge servers, containers, IoT

**Arch Linux:**
- 🔥 Bleeding edge packages
- 📦 Full control (AUR)
- 💯 Latest everything
- Perfect for: Development, testing, cutting edge

**Debian/Ubuntu:**
- 📚 Huge package ecosystem
- 🔄 Stable updates
- 💼 Enterprise support
- Perfect for: Production, stability

**NixOS:**
- 📋 Declarative config
- 🔁 Reproducible builds
- 🎯 Perfect rollback
- Perfect for: Infrastructure-as-code, DevOps

---

## Next Steps

1. **Try QTI UI:** `python3 qti_ubuntu_app.py`
2. **Choose your distro** based on your needs
3. **Run automated build:** `sudo bash quetzal_distro_builder.sh`
4. **Access your system:** Open browser to `http://localhost:8080`
5. **Scale it up:** Deploy to multiple distros/servers

---

## Support

For issues or questions:
- Check logs: `sudo journalctl -u gis-studio -n 100`
- Review this guide's Troubleshooting section
- Check Quetzal documentation

---

**🎉 Your BM is now multi-distro capable! 🎉**
