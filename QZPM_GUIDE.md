# QZPM - Queztl Package Manager

## 🚩 Overview

QZPM is an APT-like package manager for the queztl-core distributed system. It manages dependencies, versions, and installations across Beast, Sloth, and your entire cluster.

## ✅ What's Installed

- ✓ QZPM on local machine: `./qzpm`
- ✓ QZPM on Beast: `~/bin/qzpm` (192.168.1.105)
- ✓ Package repository initialized
- ✓ 16 packages available

## 📦 Available Packages

### Core
- `python-core` (3.12) - Python runtime
- `docker` (latest) - Container runtime
- `redis` (7.0) - In-memory database
- `postgresql` (16) - SQL database

### Python Frameworks
- `fastapi` (0.128.0) - Web framework
- `uvicorn` (0.40.0) - ASGI server

### AI/ML
- `pytorch-cpu` (2.5.1) - PyTorch for CPU
- `pytorch-cuda` (2.5.1) - PyTorch with CUDA
- `stable-diffusion` (latest) - Image generation AI
- `numpy` (2.2.3) - Numerical computing

### Utilities
- `pillow` (12.1.0) - Image processing
- `beautifulsoup4` (4.12.3) - HTML parser
- `requests` (2.32.5) - HTTP library

### Queztl Packages
- `queztl-webhost` (1.0.0) - AI web trainer
- `queztl-meme-generator` (1.0.0) - Meme creation
- `queztl-image-gen` (1.0.0) - Beast image generation

## 🔧 Commands

### List & Search
```bash
# List all packages
./qzpm list

# List installed only
./qzpm list --installed

# Search for packages
./qzpm search diffusion
./qzpm search pytorch

# Show package details
./qzpm show stable-diffusion
```

### Install & Remove
```bash
# Install package (with dependency resolution)
./qzpm install stable-diffusion

# Install without prompts
./qzpm install fastapi -y

# Install with break-system-packages
./qzpm install pillow --break-system-packages

# Remove package
./qzpm remove <package>
./qzpm remove <package> -y
```

### Update & Upgrade
```bash
# Update package lists
./qzpm update

# Upgrade specific package
./qzpm upgrade pytorch-cpu

# Upgrade all packages
./qzpm upgrade
```

### Manifest Management
```bash
# Export installed packages
./qzpm export my-setup.json

# Import and install from manifest
./qzpm import my-setup.json
./qzpm import my-setup.json -y
```

## 🌐 Remote Installation

### Install on Beast
```bash
./scripts/install-qzpm-remote.sh 192.168.1.105
```

### Install on Sloth
```bash
./scripts/install-qzpm-remote.sh 192.168.1.106
```

### Install on any node
```bash
./scripts/install-qzpm-remote.sh <ip-address> [username]
```

## 🎯 Common Workflows

### Setup Beast for Image Generation
```bash
# On your laptop
./qzpm export beast-setup.json

# Transfer to Beast
scp beast-setup.json xava@192.168.1.105:~/

# On Beast
ssh xava@192.168.1.105
qzpm import ~/beast-setup.json -y
qzpm install queztl-image-gen -y
```

### Synchronize Cluster Nodes
```bash
# Create manifest
./qzpm export cluster-manifest.json

# Install on all nodes
for ip in 192.168.1.{105..110}; do
  scp cluster-manifest.json xava@$ip:~/
  ssh xava@$ip "qzpm import ~/cluster-manifest.json -y"
done
```

### Install Complete Stack
```bash
# Install everything for AI image generation
./qzpm install queztl-image-gen -y

# This automatically installs:
# - fastapi
# - uvicorn
# - stable-diffusion
#   - pytorch-cpu
#     - python-core
# - pillow
```

## 📋 Example: Beast Full Setup

```bash
# 1. Install QZPM on Beast
./scripts/install-qzpm-remote.sh 192.168.1.105

# 2. SSH to Beast
ssh xava@192.168.1.105

# 3. Install packages
qzpm install queztl-image-gen -y
qzpm install queztl-meme-generator -y
qzpm install queztl-webhost -y

# 4. Verify
qzpm list --installed
```

## 🔍 Package Details

### Show Dependencies
```bash
./qzpm show stable-diffusion
```
Output:
```
📦 Package: stable-diffusion
   Version: latest
   Type: python
   Status: Not installed
   Description: Stable Diffusion XL for image generation
   Dependencies: pytorch-cpu
```

### Check What's Installed
```bash
./qzpm list --installed
```

### Search by Keyword
```bash
./qzpm search image
./qzpm search pytorch
./qzpm search queztl
```

## 🚀 Advanced Usage

### Custom Package Repository
Packages are defined in `~/.qzpm/packages.json`. You can add custom packages:

```json
{
  "my-package": {
    "version": "1.0.0",
    "type": "python",
    "description": "My custom package",
    "dependencies": ["python-core"],
    "install_command": "pip install my-package"
  }
}
```

### Version Pinning
All packages use specific versions to ensure stability:
- PyTorch: 2.5.1
- FastAPI: 0.128.0
- Pillow: 12.1.0

### Dependency Graph
QZPM automatically resolves dependencies:
```
queztl-image-gen
  ├── fastapi (0.128.0)
  │   └── python-core (3.12)
  ├── uvicorn (0.40.0)
  │   └── python-core (3.12)
  ├── stable-diffusion (latest)
  │   └── pytorch-cpu (2.5.1)
  │       └── python-core (3.12)
  └── pillow (12.1.0)
      └── python-core (3.12)
```

## 📊 Status Files

QZPM stores data in `~/.qzpm/`:
- `packages.json` - Package repository
- `installed.json` - Installed packages
- `sources.list` - Package sources (future)

## 🔧 Troubleshooting

### Package Not Found
```bash
./qzpm update
./qzpm search <query>
```

### Dependency Conflicts
QZPM will show conflicts and ask for confirmation:
```bash
./qzpm install <package>
# Review dependencies and confirm
```

### Remote Installation Fails
Ensure SSH access and that ~/bin is in PATH:
```bash
ssh xava@192.168.1.105 "mkdir -p ~/bin && echo 'export PATH=\"\$HOME/bin:\$PATH\"' >> ~/.bashrc"
```

## 📝 Notes

- QZPM is distributed-system aware
- Handles Python's externally-managed-environment
- Supports both pip and system packages
- Version-locked for stability
- Manifest export/import for reproducibility

## 🎯 Next Steps

1. Install QZPM on all cluster nodes
2. Create cluster manifest
3. Deploy consistent environment everywhere
4. Use for software version management

## 🔗 Integration

QZPM integrates with:
- Beast image generation system
- Meme generator pipeline
- WebHost AI trainer
- Future cluster services

Ready to stabilize your distributed system! 🚀
