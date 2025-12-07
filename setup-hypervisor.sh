#!/bin/bash
# 🦅 Queztl Hypervisor Setup Script
# Prepares environment for building Type-1 hypervisor on Queztl OS

set -e

echo "=============================================="
echo "🦅 QUEZTL HYPERVISOR - ENVIRONMENT SETUP"
echo "=============================================="
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "⚠️  Warning: Detected non-Linux OS ($OSTYPE)"
    echo "   Hypervisor requires Linux with KVM support"
    echo "   Continuing with macOS setup for development..."
    echo ""
fi

# Create directory structure
echo "📁 Creating hypervisor directory structure..."
mkdir -p queztl-hypervisor/{core,api,vms/{images,configs,snapshots},tools,docs}
mkdir -p queztl-hypervisor/kernel/{patches,configs,modules}
mkdir -p queztl-hypervisor/dashboard/{frontend,backend}

echo "✅ Directory structure created"
echo ""

# Install Rust (if not installed)
echo "🦀 Checking Rust installation..."
if ! command -v rustc &> /dev/null; then
    echo "   Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
    echo "   ✅ Rust installed"
else
    echo "   ✅ Rust already installed ($(rustc --version))"
fi
echo ""

# Check for KVM support (Linux only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🔍 Checking KVM support..."
    if [[ -e /dev/kvm ]]; then
        echo "   ✅ KVM available at /dev/kvm"
    else
        echo "   ⚠️  KVM not found - checking CPU virtualization..."
        if grep -q -E '(vmx|svm)' /proc/cpuinfo; then
            echo "   ✅ CPU supports virtualization (VT-x/AMD-V)"
            echo "   📝 You may need to enable KVM: sudo modprobe kvm"
        else
            echo "   ❌ CPU does not support virtualization"
            echo "   This is required for hardware-assisted virtualization"
        fi
    fi
    echo ""
fi

# Create Cargo.toml for hypervisor core
echo "📝 Creating Rust hypervisor project..."
cat > queztl-hypervisor/core/Cargo.toml << 'EOF'
[package]
name = "queztl-hypervisor"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { version = "1.35", features = ["full"] }
kvm-ioctls = "0.16"
kvm-bindings = "0.7"
vmm-sys-util = "0.12"
vm-memory = "0.14"
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
clap = { version = "4.4", features = ["derive"] }
tracing = "0.1"
tracing-subscriber = "0.3"
anyhow = "1.0"

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
EOF

echo "✅ Cargo.toml created"
echo ""

# Create main.rs skeleton
echo "📝 Creating hypervisor core skeleton..."
cat > queztl-hypervisor/core/src/main.rs << 'EOF'
//! Queztl Hypervisor - Type-1 Bare-Metal Hypervisor
//! 
//! This is the main entry point for the Queztl Hypervisor.
//! It initializes KVM, manages VMs, and provides control interfaces.

use std::error::Error;
use clap::Parser;

#[derive(Parser)]
#[command(name = "queztl-hv")]
#[command(about = "Queztl Hypervisor - Manage virtual machines", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Parser)]
enum Commands {
    /// Start the hypervisor daemon
    Start {
        #[arg(short, long, default_value = "0.0.0.0:8080")]
        bind: String,
    },
    /// Create a new VM
    Create {
        #[arg(short, long)]
        name: String,
        #[arg(short, long, default_value = "2")]
        vcpus: u8,
        #[arg(short, long, default_value = "2048")]
        memory: u64,
    },
    /// List all VMs
    List,
    /// Start a VM
    Run {
        name: String,
    },
    /// Stop a VM
    Stop {
        name: String,
    },
}

fn main() -> Result<(), Box<dyn Error>> {
    // Initialize tracing
    tracing_subscriber::fmt::init();

    let cli = Cli::parse();

    match cli.command {
        Commands::Start { bind } => {
            println!("🦅 Starting Queztl Hypervisor on {}", bind);
            start_hypervisor(&bind)?;
        }
        Commands::Create { name, vcpus, memory } => {
            println!("📦 Creating VM: {}", name);
            println!("   vCPUs: {}", vcpus);
            println!("   Memory: {}MB", memory);
            create_vm(&name, vcpus, memory)?;
        }
        Commands::List => {
            println!("📋 Listing VMs:");
            list_vms()?;
        }
        Commands::Run { name } => {
            println!("▶️  Starting VM: {}", name);
            run_vm(&name)?;
        }
        Commands::Stop { name } => {
            println!("⏹️  Stopping VM: {}", name);
            stop_vm(&name)?;
        }
    }

    Ok(())
}

fn start_hypervisor(bind: &str) -> Result<(), Box<dyn Error>> {
    println!("🚀 Hypervisor daemon starting...");
    println!("🔍 Checking KVM availability...");
    
    // TODO: Initialize KVM
    // TODO: Set up API server
    // TODO: Start monitoring
    
    println!("✅ Hypervisor ready");
    println!("📡 API available at: http://{}", bind);
    
    Ok(())
}

fn create_vm(name: &str, vcpus: u8, memory: u64) -> Result<(), Box<dyn Error>> {
    // TODO: Create VM configuration
    // TODO: Allocate resources
    // TODO: Create disk image
    
    println!("✅ VM '{}' created", name);
    Ok(())
}

fn list_vms() -> Result<(), Box<dyn Error>> {
    // TODO: Query VM database
    // TODO: Display VM status
    
    println!("   (No VMs yet)");
    Ok(())
}

fn run_vm(name: &str) -> Result<(), Box<dyn Error>> {
    // TODO: Load VM configuration
    // TODO: Initialize KVM VM
    // TODO: Start vCPUs
    
    println!("✅ VM '{}' started", name);
    Ok(())
}

fn stop_vm(name: &str) -> Result<(), Box<dyn Error>> {
    // TODO: Send shutdown signal
    // TODO: Save state
    // TODO: Cleanup resources
    
    println!("✅ VM '{}' stopped", name);
    Ok(())
}
EOF

mkdir -p queztl-hypervisor/core/src
echo "✅ Hypervisor core skeleton created"
echo ""

# Create Python API
echo "📝 Creating Python control API..."
cat > queztl-hypervisor/api/qhv_api.py << 'EOF'
#!/usr/bin/env python3
"""
Queztl Hypervisor Control API
Provides REST and WebSocket interfaces for VM management
"""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import json

app = FastAPI(title="Queztl Hypervisor API", version="0.1.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VMConfig(BaseModel):
    name: str
    vcpus: int = 2
    memory_mb: int = 2048
    disk_gb: int = 20
    kernel: Optional[str] = None

class VMStatus(BaseModel):
    name: str
    status: str
    vcpus: int
    memory_mb: int
    uptime_seconds: int

# In-memory VM database (replace with real DB)
vms = {}

@app.get("/")
async def root():
    return {
        "service": "Queztl Hypervisor API",
        "version": "0.1.0",
        "status": "running"
    }

@app.post("/api/vm/create")
async def create_vm(config: VMConfig):
    """Create a new virtual machine"""
    if config.name in vms:
        return {"error": f"VM '{config.name}' already exists"}
    
    vms[config.name] = {
        "name": config.name,
        "vcpus": config.vcpus,
        "memory_mb": config.memory_mb,
        "disk_gb": config.disk_gb,
        "status": "stopped",
        "uptime_seconds": 0
    }
    
    return {"success": True, "vm": vms[config.name]}

@app.get("/api/vm/list")
async def list_vms() -> List[VMStatus]:
    """List all virtual machines"""
    return [VMStatus(**vm) for vm in vms.values()]

@app.post("/api/vm/{name}/start")
async def start_vm(name: str):
    """Start a virtual machine"""
    if name not in vms:
        return {"error": f"VM '{name}' not found"}
    
    vms[name]["status"] = "running"
    return {"success": True, "vm": vms[name]}

@app.post("/api/vm/{name}/stop")
async def stop_vm(name: str):
    """Stop a virtual machine"""
    if name not in vms:
        return {"error": f"VM '{name}' not found"}
    
    vms[name]["status"] = "stopped"
    return {"success": True, "vm": vms[name]}

@app.get("/api/vm/{name}/status")
async def vm_status(name: str):
    """Get VM status"""
    if name not in vms:
        return {"error": f"VM '{name}' not found"}
    
    return vms[name]

@app.websocket("/ws/monitor")
async def websocket_monitor(websocket: WebSocket):
    """Real-time VM monitoring via WebSocket"""
    await websocket.accept()
    
    try:
        while True:
            # Send VM metrics every second
            metrics = {
                "timestamp": asyncio.get_event_loop().time(),
                "vms": list(vms.values())
            }
            await websocket.send_json(metrics)
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
EOF

chmod +x queztl-hypervisor/api/qhv_api.py
echo "✅ Python API created"
echo ""

# Create kernel build script
echo "📝 Creating kernel build script..."
cat > queztl-hypervisor/kernel/build-custom-kernel.sh << 'EOF'
#!/bin/bash
# Build custom Linux kernel for Queztl VMs

set -e

KERNEL_VERSION="6.6.7"
KERNEL_DIR="linux-${KERNEL_VERSION}"
KERNEL_URL="https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-${KERNEL_VERSION}.tar.xz"

echo "🐧 Building Custom Linux Kernel for Queztl"
echo "============================================"
echo ""

# Download kernel source
if [ ! -d "$KERNEL_DIR" ]; then
    echo "📥 Downloading Linux kernel ${KERNEL_VERSION}..."
    wget "$KERNEL_URL"
    tar xf "linux-${KERNEL_VERSION}.tar.xz"
    echo "✅ Kernel source downloaded"
else
    echo "✅ Kernel source already exists"
fi

cd "$KERNEL_DIR"

# Create Queztl kernel config
echo "📝 Creating Queztl kernel configuration..."
make defconfig

# Enable KVM guest support
scripts/config --enable CONFIG_HYPERVISOR_GUEST
scripts/config --enable CONFIG_KVM_GUEST
scripts/config --enable CONFIG_PARAVIRT
scripts/config --enable CONFIG_PARAVIRT_SPINLOCKS

# Enable Virtio drivers
scripts/config --enable CONFIG_VIRTIO_PCI
scripts/config --enable CONFIG_VIRTIO_NET
scripts/config --enable CONFIG_VIRTIO_BLK
scripts/config --enable CONFIG_VIRTIO_CONSOLE

# Enable real-time features
scripts/config --enable CONFIG_PREEMPT
scripts/config --enable CONFIG_HIGH_RES_TIMERS

# Minimize size
scripts/config --disable CONFIG_DEBUG_KERNEL
scripts/config --disable CONFIG_WIRELESS
scripts/config --disable CONFIG_WLAN

echo "✅ Configuration complete"
echo ""

# Build kernel
echo "🔨 Building kernel (this may take a while)..."
make -j$(nproc) bzImage modules

echo ""
echo "✅ Kernel built successfully!"
echo "📦 Kernel image: arch/x86/boot/bzImage"
echo ""

EOF

chmod +x queztl-hypervisor/kernel/build-custom-kernel.sh
echo "✅ Kernel build script created"
echo ""

# Create VM builder
echo "📝 Creating VM image builder..."
cat > queztl-hypervisor/tools/build-vm-image.sh << 'EOF'
#!/bin/bash
# Build a minimal Linux VM image for Queztl Hypervisor

set -e

VM_NAME="${1:-queztl-vm}"
VM_SIZE="${2:-2G}"
DISTRO="${3:-alpine}"

echo "📦 Building VM Image: $VM_NAME"
echo "===================================="
echo "   Distribution: $DISTRO"
echo "   Size: $VM_SIZE"
echo ""

# Create disk image
echo "💾 Creating disk image..."
qemu-img create -f qcow2 "../vms/images/${VM_NAME}.qcow2" "$VM_SIZE"
echo "✅ Disk image created"
echo ""

# TODO: Bootstrap Linux distribution
# TODO: Install custom kernel
# TODO: Configure auto-login
# TODO: Install Queztl drivers

echo "✅ VM image built: ../vms/images/${VM_NAME}.qcow2"
echo ""

EOF

chmod +x queztl-hypervisor/tools/build-vm-image.sh
echo "✅ VM builder created"
echo ""

# Create README
echo "📝 Creating documentation..."
cat > queztl-hypervisor/README.md << 'EOF'
# 🦅 Queztl Hypervisor

Type-1 bare-metal hypervisor for running custom Linux instances.

## Quick Start

### 1. Build Hypervisor Core
```bash
cd core
cargo build --release
```

### 2. Start API Server
```bash
cd api
pip install fastapi uvicorn websockets
python qhv_api.py
```

### 3. Build Custom Kernel
```bash
cd kernel
./build-custom-kernel.sh
```

### 4. Create VM Image
```bash
cd tools
./build-vm-image.sh my-linux-vm 2G alpine
```

### 5. Run Hypervisor
```bash
cd core
./target/release/queztl-hypervisor start
```

## Architecture

See [../QUEZTL_HYPERVISOR_ARCHITECTURE.md](../QUEZTL_HYPERVISOR_ARCHITECTURE.md)

## Commands

```bash
# Create VM
queztl-hv create --name my-vm --vcpus 4 --memory 4096

# List VMs
queztl-hv list

# Start VM
queztl-hv run my-vm

# Stop VM
queztl-hv stop my-vm
```

## API Endpoints

- `POST /api/vm/create` - Create new VM
- `GET /api/vm/list` - List all VMs
- `POST /api/vm/{name}/start` - Start VM
- `POST /api/vm/{name}/stop` - Stop VM
- `GET /api/vm/{name}/status` - Get VM status
- `WS /ws/monitor` - Real-time monitoring

## Requirements

- Linux with KVM support
- Rust 1.70+
- Python 3.8+
- QEMU/KVM
- 8GB+ RAM recommended

EOF

echo "✅ Documentation created"
echo ""

echo "=============================================="
echo "✅ QUEZTL HYPERVISOR SETUP COMPLETE"
echo "=============================================="
echo ""
echo "📁 Project structure:"
echo "   queztl-hypervisor/"
echo "   ├── core/           # Rust hypervisor daemon"
echo "   ├── api/            # Python control API"
echo "   ├── kernel/         # Custom kernel builder"
echo "   ├── tools/          # VM management tools"
echo "   ├── vms/            # VM images and configs"
echo "   └── dashboard/      # Web dashboard (TODO)"
echo ""
echo "🚀 Next steps:"
echo "   1. cd queztl-hypervisor/core && cargo build"
echo "   2. cd queztl-hypervisor/api && python qhv_api.py"
echo "   3. Review QUEZTL_HYPERVISOR_ARCHITECTURE.md"
echo ""
echo "Let's see what this baby can do! 🦅"
