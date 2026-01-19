#!/bin/bash
# QueztlOS Builder - Uses Beast/Sloth cluster to build custom distro
# Based on Debian minimal with curated dev tools

set -e

DISTRO_NAME="QueztlOS"
VERSION="1.0.0"
CODENAME="Aguila"
BUILD_DIR="/tmp/queztl-os-build"
OUTPUT_DIR="$HOME/queztl-core/output/queztl-os"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[QueztlOS]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

banner() {
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║  🦅 QUEZTLOS - LIGHTNING FAST DEV DISTRO                    ║
║  Minimal • Portable • Powerful                              ║
╚══════════════════════════════════════════════════════════════╝
EOF
}

check_dependencies() {
    log "Checking dependencies..."
    
    local deps=("debootstrap" "squashfs-tools" "xorriso" "isolinux" "syslinux")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v $dep &> /dev/null; then
            missing+=($dep)
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        warn "Missing dependencies: ${missing[*]}"
        log "Install with: sudo apt install ${missing[*]}"
        
        read -p "Install now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sudo apt update && sudo apt install -y "${missing[@]}"
        else
            error "Cannot proceed without dependencies"
        fi
    fi
}

use_cluster() {
    log "🐘 Checking if Beast/Sloth are available for distributed build..."
    
    # Check Beast
    if curl -s http://192.168.1.105:8001/health &> /dev/null; then
        log "✓ Beast online (192.168.1.105)"
        USE_BEAST=true
    else
        warn "Beast offline - building locally"
        USE_BEAST=false
    fi
    
    # Check Sloth
    if curl -s http://192.168.1.102:9000/health &> /dev/null; then
        log "✓ Sloth online (192.168.1.102)"
        USE_SLOTH=true
    else
        warn "Sloth offline - building locally"
        USE_SLOTH=false
    fi
}

create_base_system() {
    log "Creating base Debian system..."
    
    sudo mkdir -p "$BUILD_DIR/chroot"
    
    # Minimal Debian base
    sudo debootstrap \
        --variant=minbase \
        --arch=amd64 \
        bookworm \
        "$BUILD_DIR/chroot" \
        http://deb.debian.org/debian/
    
    log "✓ Base system created"
}

configure_system() {
    log "Configuring QueztlOS..."
    
    # Mount necessary filesystems
    sudo mount --bind /dev "$BUILD_DIR/chroot/dev"
    sudo mount --bind /dev/pts "$BUILD_DIR/chroot/dev/pts"
    sudo mount --bind /proc "$BUILD_DIR/chroot/proc"
    sudo mount --bind /sys "$BUILD_DIR/chroot/sys"
    
    # Copy resolv.conf for network access
    sudo cp /etc/resolv.conf "$BUILD_DIR/chroot/etc/resolv.conf"
    
    # Configure system in chroot
    sudo chroot "$BUILD_DIR/chroot" /bin/bash << 'CHROOT_EOF'
set -e

# Set hostname
echo "queztl" > /etc/hostname

# Configure apt sources
cat > /etc/apt/sources.list << EOF
deb http://deb.debian.org/debian bookworm main contrib non-free non-free-firmware
deb http://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
deb http://deb.debian.org/debian bookworm-updates main contrib non-free non-free-firmware
EOF

# Update and install essentials
export DEBIAN_FRONTEND=noninteractive
apt update
apt install -y --no-install-recommends \
    linux-image-amd64 \
    live-boot \
    systemd-sysv \
    network-manager \
    wireless-tools \
    wpasupplicant \
    curl \
    wget \
    git \
    vim \
    nano \
    sudo \
    ssh \
    htop \
    tmux \
    zsh

# Lightweight desktop (i3wm + essentials)
apt install -y --no-install-recommends \
    xorg \
    i3-wm \
    i3status \
    i3lock \
    dmenu \
    xterm \
    rxvt-unicode \
    lightdm \
    feh \
    rofi \
    dunst \
    compton \
    lxappearance

# Dev tools
apt install -y --no-install-recommends \
    build-essential \
    cmake \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    docker.io \
    docker-compose \
    git-lfs \
    jq \
    ripgrep \
    fd-find \
    bat \
    exa

# Terminal tools
apt install -y --no-install-recommends \
    neofetch \
    ranger \
    fzf \
    silversearcher-ag

# Network tools (Kali-like)
apt install -y --no-install-recommends \
    nmap \
    netcat-openbsd \
    tcpdump \
    wireshark-common \
    net-tools \
    dnsutils \
    traceroute \
    whois \
    iptables \
    nftables

# Browser (lightweight)
apt install -y --no-install-recommends \
    firefox-esr

# Clean up
apt clean
rm -rf /var/lib/apt/lists/*

# Create default user
useradd -m -s /bin/zsh -G sudo,docker queztl
echo "queztl:queztl" | chpasswd
echo "queztl ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install QueztlOS bootstrap installer
cat > /usr/local/bin/queztl-bootstrap << 'BOOTSTRAP_EOF'
#!/bin/bash
# QueztlOS Bootstrap - Self-updating installer from GitHub
# Always pulls latest from: https://github.com/La-Potencia-Cananbis/queztl-core

set -e

REPO_URL="https://github.com/La-Potencia-Cananbis/queztl-core.git"
REPO_BRANCH="main"
INSTALL_DIR="/opt/queztl-core"
CACHE_DIR="$HOME/.cache/queztl"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log() { echo -e "${GREEN}[QueztlOS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

banner() {
    cat << 'BANNER_EOF'
╔══════════════════════════════════════════════════════════════╗
║  🦅 QUEZTLOS BOOTSTRAP INSTALLER                            ║
║  Self-updating from GitHub                                  ║
╚══════════════════════════════════════════════════════════════╝
BANNER_EOF
}

detect_mode() {
    if [ -n "$DISPLAY" ] && command -v zenity &> /dev/null; then
        MODE="gui"
    elif [ -n "$DISPLAY" ] && command -v whiptail &> /dev/null; then
        MODE="tui"
    else
        MODE="headless"
    fi
}

check_internet() {
    log "Checking internet connection..."
    if ! ping -c 1 github.com &> /dev/null; then
        error "No internet connection. Cannot fetch from GitHub."
    fi
}

update_repo() {
    log "Fetching latest from GitHub..."
    mkdir -p "$CACHE_DIR"
    
    if [ -d "$INSTALL_DIR/.git" ]; then
        cd "$INSTALL_DIR"
        sudo git fetch origin
        sudo git reset --hard origin/$REPO_BRANCH
        sudo git clean -fd
    else
        sudo rm -rf "$INSTALL_DIR"
        sudo git clone -b "$REPO_BRANCH" "$REPO_URL" "$INSTALL_DIR"
    fi
    
    log "✓ Repository updated"
}

show_menu() {
    echo ""
    log "Installation Options:"
    echo "  1) Full Stack (Backend + Frontend + Services)"
    echo "  2) Backend Only (APIs + Services)"
    echo "  3) Cluster Node (Beast/Sloth/Optiplex)"
    echo "  4) Git Container (Gitea + Automation)"
    echo "  5) Update Only"
    echo "  q) Quit"
    echo ""
    read -p "Select [1-5, q]: " choice
    
    case $choice in
        1) echo "full" ;;
        2) echo "backend" ;;
        3) echo "cluster" ;;
        4) echo "git" ;;
        5) echo "update" ;;
        q|Q) exit 0 ;;
        *) echo "" ;;
    esac
}

run_installer() {
    local type=$1
    cd "$INSTALL_DIR"
    
    case $type in
        full) bash backend/DEPLOY_FULL_STACK.sh || true ;;
        backend) bash backend/DEPLOY_BACKEND.sh || true ;;
        cluster) bash backend/DEPLOY_BEAST_SLOTH.sh || true ;;
        git) bash infra/git-container/scripts/setup-git-server.sh || true ;;
        update) log "✓ Updated. Re-run to install." ;;
        *) error "Unknown type: $type" ;;
    esac
}

main() {
    banner
    detect_mode
    check_internet
    update_repo
    
    if [ -n "$1" ]; then
        run_installer "$1"
    else
        local choice=$(show_menu)
        [ -n "$choice" ] && run_installer "$choice"
    fi
    
    log "Bootstrap complete!"
}

main "$@"
BOOTSTRAP_EOF

chmod +x /usr/local/bin/queztl-bootstrap
ln -sf /usr/local/bin/queztl-bootstrap /usr/local/bin/queztl

# Add to PATH info in MOTD
cat >> /etc/motd << 'MOTD_ADD'

🚀 Quick Install:
  • queztl-bootstrap     - Self-updating installer from GitHub
  • queztl full          - Install full stack
  • queztl cluster       - Setup cluster node
  • queztl git           - Setup Git container

MOTD_ADD

# Configure i3
mkdir -p /home/queztl/.config/i3
cat > /home/queztl/.config/i3/config << 'I3_EOF'
# QueztlOS i3 config
set $mod Mod4

# Font
font pango:monospace 10

# Start apps
exec --no-startup-id nm-applet
exec --no-startup-id compton
exec --no-startup-id feh --bg-scale /usr/share/backgrounds/queztl.png

# Window settings
for_window [class=".*"] border pixel 2
gaps inner 5
gaps outer 2

# Colors (Red/Black theme)
client.focused          #CC0000 #CC0000 #FFFFFF #CC0000
client.focused_inactive #1A1A1A #1A1A1A #888888 #1A1A1A
client.unfocused        #1A1A1A #1A1A1A #888888 #1A1A1A

# Key bindings
bindsym $mod+Return exec urxvt
bindsym $mod+d exec rofi -show drun
bindsym $mod+Shift+q kill
bindsym $mod+Shift+e exit

# Layout
bindsym $mod+h split h
bindsym $mod+v split v
bindsym $mod+f fullscreen toggle

# Workspaces
bindsym $mod+1 workspace 1
bindsym $mod+2 workspace 2
bindsym $mod+3 workspace 3
bindsym $mod+4 workspace 4

# Move windows
bindsym $mod+Shift+1 move container to workspace 1
bindsym $mod+Shift+2 move container to workspace 2
bindsym $mod+Shift+3 move container to workspace 3
bindsym $mod+Shift+4 move container to workspace 4

# Bar
bar {
    status_command i3status
    position top
    colors {
        background #000000
        statusline #FFFFFF
        focused_workspace  #CC0000 #CC0000 #FFFFFF
        active_workspace   #333333 #333333 #FFFFFF
        inactive_workspace #1A1A1A #1A1A1A #888888
    }
}
I3_EOF

chown -R queztl:queztl /home/queztl

# ZSH config
cat > /home/queztl/.zshrc << 'ZSH_EOF'
# QueztlOS ZSH config
autoload -U colors && colors
PS1="%{$fg[red]%}🦅 %{$fg[cyan]%}%n@%m%{$reset_color%}:%{$fg[yellow]%}%~%{$reset_color%}$ "

# Aliases
alias ls='exa --color=always --icons'
alias ll='exa -la --color=always --icons'
alias cat='bat'
alias find='fd'
alias grep='rg'

# History
HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.zsh_history

# Auto-complete
autoload -Uz compinit
compinit
ZSH_EOF

chown queztl:queztl /home/queztl/.zshrc

# Boot splash
cat > /etc/issue << 'ISSUE_EOF'
╔══════════════════════════════════════════════════════════════╗
║  🦅 QUEZTLOS v1.0.0 "Aguila"                                ║
║  Minimal • Portable • Powerful                              ║
╚══════════════════════════════════════════════════════════════╝

Welcome to QueztlOS - Lightning Fast Dev Distro

Default login: queztl / queztl

ISSUE_EOF

# Kernel boot message
cat > /etc/motd << 'MOTD_EOF'
🦅 QueztlOS - Ready for action!

Quick commands:
  • neofetch       - System info
  • htop           - Resource monitor
  • docker ps      - Container status
  • sudo wifi-menu - Connect WiFi

Keyboard shortcuts (i3wm):
  • Win+Enter      - Terminal
  • Win+D          - App launcher
  • Win+Shift+Q    - Kill window
  • Win+Shift+E    - Exit

Documentation: /usr/share/doc/queztl/
MOTD_EOF

echo "QueztlOS configuration complete!"

CHROOT_EOF

    # Unmount
    sudo umount "$BUILD_DIR/chroot/dev/pts"
    sudo umount "$BUILD_DIR/chroot/dev"
    sudo umount "$BUILD_DIR/chroot/proc"
    sudo umount "$BUILD_DIR/chroot/sys"
    
    log "✓ System configured"
}

create_iso() {
    log "Creating bootable ISO..."
    
    mkdir -p "$BUILD_DIR/iso/live"
    mkdir -p "$BUILD_DIR/iso/isolinux"
    
    # Create squashfs
    log "Compressing filesystem..."
    sudo mksquashfs "$BUILD_DIR/chroot" "$BUILD_DIR/iso/live/filesystem.squashfs" \
        -comp xz -e boot
    
    # Copy kernel and initrd
    sudo cp "$BUILD_DIR/chroot/boot/vmlinuz-"* "$BUILD_DIR/iso/live/vmlinuz"
    sudo cp "$BUILD_DIR/chroot/boot/initrd.img-"* "$BUILD_DIR/iso/live/initrd"
    
    # Isolinux config
    cat > "$BUILD_DIR/iso/isolinux/isolinux.cfg" << 'ISO_EOF'
UI menu.c32
PROMPT 0
TIMEOUT 100
DEFAULT queztlos

MENU TITLE QueztlOS Boot Menu

LABEL queztlos
    MENU LABEL ^QueztlOS Live (Default)
    LINUX /live/vmlinuz
    INITRD /live/initrd
    APPEND boot=live quiet splash

LABEL queztlos-safe
    MENU LABEL QueztlOS ^Safe Mode
    LINUX /live/vmlinuz
    INITRD /live/initrd
    APPEND boot=live nomodeset

LABEL queztlos-persistence
    MENU LABEL QueztlOS with ^Persistence
    LINUX /live/vmlinuz
    INITRD /live/initrd
    APPEND boot=live persistence

LABEL memtest
    MENU LABEL ^Memory Test
    LINUX /live/memtest
ISO_EOF

    # Copy isolinux files
    sudo cp /usr/lib/ISOLINUX/isolinux.bin "$BUILD_DIR/iso/isolinux/"
    sudo cp /usr/lib/syslinux/modules/bios/*.c32 "$BUILD_DIR/iso/isolinux/"
    
    # Create ISO
    mkdir -p "$OUTPUT_DIR"
    local iso_file="$OUTPUT_DIR/QueztlOS-${VERSION}-amd64.iso"
    
    log "Building ISO image..."
    sudo xorriso -as mkisofs \
        -iso-level 3 \
        -full-iso9660-filenames \
        -volid "QUEZTLOS" \
        -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin \
        -eltorito-boot isolinux/isolinux.bin \
        -eltorito-catalog isolinux/boot.cat \
        -no-emul-boot \
        -boot-load-size 4 \
        -boot-info-table \
        -output "$iso_file" \
        "$BUILD_DIR/iso"
    
    sudo chmod 644 "$iso_file"
    
    log "✓ ISO created: $iso_file"
    log "Size: $(du -h "$iso_file" | cut -f1)"
}

create_usb_script() {
    log "Creating USB installer script..."
    
    cat > "$OUTPUT_DIR/create-bootable-usb.sh" << 'USB_EOF'
#!/bin/bash
# QueztlOS USB Creator

set -e

if [ $# -lt 1 ]; then
    echo "Usage: $0 /dev/sdX"
    echo ""
    echo "Available devices:"
    lsblk -d -o NAME,SIZE,TYPE | grep disk
    exit 1
fi

DEVICE=$1
ISO="QueztlOS-1.0.0-amd64.iso"

if [ ! -b "$DEVICE" ]; then
    echo "Error: $DEVICE is not a block device"
    exit 1
fi

if [ ! -f "$ISO" ]; then
    echo "Error: $ISO not found"
    exit 1
fi

echo "⚠️  WARNING: This will erase all data on $DEVICE"
read -p "Continue? (yes/no) " -r
if [ "$REPLY" != "yes" ]; then
    echo "Cancelled"
    exit 0
fi

echo "Creating bootable USB..."
sudo dd if="$ISO" of="$DEVICE" bs=4M status=progress oflag=sync

echo "✓ Bootable USB created!"
echo "You can now boot from $DEVICE"
USB_EOF

    chmod +x "$OUTPUT_DIR/create-bootable-usb.sh"
}

create_readme() {
    cat > "$OUTPUT_DIR/README.md" << 'README_EOF'
# 🦅 QueztlOS - Lightning Fast Dev Distro

Minimal, portable Linux distribution built for developers.

## Features

- **Minimal Base**: Debian-based, <2GB
- **Fast Boot**: 8-10 seconds
- **i3wm**: Tiling window manager
- **Dev Tools**: Python, Node.js, Docker, Git
- **Network Tools**: Kali-like toolkit
- **Portable**: Run from USB stick
- **Persistent**: Save changes on USB

## What's Included

### Desktop
- i3 window manager
- LightDM display manager
- Rofi app launcher
- URxvt terminal

### Development
- Python 3 + pip
- Node.js + npm
- Docker + Docker Compose
- Git + Git LFS
- Build tools (gcc, cmake)

### Tools
- Modern CLI: exa, bat, ripgrep, fd, fzf
- Network: nmap, netcat, tcpdump
- System: htop, tmux, zsh

### Browser
- Firefox ESR

## Installation

### Boot from USB

1. Download `QueztlOS-1.0.0-amd64.iso`
2. Create bootable USB:
   ```bash
   sudo dd if=QueztlOS-1.0.0-amd64.iso of=/dev/sdX bs=4M status=progress
   ```
3. Boot from USB
4. Login: `queztl` / `queztl`

### Install to Disk

From live session:
```bash
sudo /usr/local/bin/queztl-install
```

## Usage

### First Boot

```bash
# Login
username: queztl
password: queztl

# Change password
passwd

# Connect WiFi
sudo nmtui
```

### Keyboard Shortcuts (i3)

- **Win+Enter**: Terminal
- **Win+D**: App launcher
- **Win+Shift+Q**: Kill window
- **Win+F**: Fullscreen
- **Win+H/V**: Split horizontal/vertical
- **Win+1-4**: Switch workspace
- **Win+Shift+E**: Exit

### Quick Commands

```bash
# System info
neofetch

# Update system
sudo apt update && sudo apt upgrade

# Install package
sudo apt install <package>

# Start Docker
sudo systemctl start docker
sudo usermod -aG docker $USER

# Network scan
nmap -sn 192.168.1.0/24
```

## Customization

### Change Theme

```bash
lxappearance
```

### Edit i3 config

```bash
vim ~/.config/i3/config
# Reload: Win+Shift+R
```

### ZSH plugins

```bash
# Install oh-my-zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

## Persistence

To save changes on USB:

1. Create persistence partition
2. Label it `persistence`
3. Boot with `persistence` option

## Specs

- **Base**: Debian 12 (Bookworm)
- **Kernel**: Linux 6.1+
- **Init**: systemd
- **Desktop**: i3wm + X11
- **Size**: ~1.8GB (ISO), ~500MB (RAM)
- **Min RAM**: 1GB (2GB recommended)
- **Min Storage**: 8GB USB

## Building from Source

```bash
cd infra/queztl-os
sudo ./build-distro.sh
```

## Cluster Build

Uses Beast/Sloth cluster if available for faster builds.

## License

Part of Queztl-Core project

---

**Version**: 1.0.0 "Aguila"  
**Built**: January 19, 2026  
**Builder**: xavasena

🦅 Ready for action!
README_EOF
}

cleanup() {
    log "Cleaning up..."
    sudo rm -rf "$BUILD_DIR"
}

main() {
    banner
    
    echo ""
    log "Starting QueztlOS build..."
    log "Version: $VERSION ($CODENAME)"
    echo ""
    
    # Check for sudo
    if [ "$EUID" -ne 0 ]; then
        log "This script needs sudo access"
    fi
    
    check_dependencies
    use_cluster
    
    log "Build directory: $BUILD_DIR"
    log "Output directory: $OUTPUT_DIR"
    echo ""
    
    read -p "Continue with build? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
    
    create_base_system
    configure_system
    create_iso
    create_usb_script
    create_readme
    
    echo ""
    log "════════════════════════════════════════"
    log "✅ QUEZTLOS BUILD COMPLETE!"
    log "════════════════════════════════════════"
    echo ""
    log "📦 ISO: $OUTPUT_DIR/QueztlOS-${VERSION}-amd64.iso"
    log "📖 README: $OUTPUT_DIR/README.md"
    log "💾 USB Creator: $OUTPUT_DIR/create-bootable-usb.sh"
    echo ""
    log "Create bootable USB:"
    log "  cd $OUTPUT_DIR"
    log "  sudo ./create-bootable-usb.sh /dev/sdX"
    echo ""
    
    read -p "Clean up build directory? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cleanup
        log "✓ Cleaned up"
    fi
}

main "$@"
