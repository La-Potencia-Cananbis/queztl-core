#!/usr/bin/env python3
"""
Quetzal Terminal Interface (QTI) - Ubuntu Application
Provides a TUI for managing Quetzal on Ubuntu systems
Allows rebuilding BM with alternative distros
"""

import curses
import subprocess
import json
import os
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional
import threading
import time

@dataclass
class DistroOption:
    name: str
    package_manager: str
    init_system: str
    kernel: str
    base_size_gb: int
    description: str

class QTIApp:
    def __init__(self):
        self.current_menu = "main"
        self.selected_option = 0
        self.distros = self._init_distros()
        self.selected_distro = None
        self.output_buffer = []
        self.is_running = True
        
    def _init_distros(self) -> Dict[str, DistroOption]:
        """Initialize available distro options"""
        return {
            "ubuntu": DistroOption(
                name="Ubuntu 24.04 LTS",
                package_manager="apt",
                init_system="systemd",
                kernel="6.8",
                base_size_gb=2,
                description="Current standard - good all-rounder"
            ),
            "debian": DistroOption(
                name="Debian 12 (Bookworm)",
                package_manager="apt",
                init_system="systemd",
                kernel="6.1",
                base_size_gb=2,
                description="More stable, slower updates"
            ),
            "alpine": DistroOption(
                name="Alpine Linux 3.19",
                package_manager="apk",
                init_system="openrc",
                kernel="6.6",
                base_size_gb=0.15,
                description="Ultra-minimal (170MB) - blazing fast"
            ),
            "arch": DistroOption(
                name="Arch Linux",
                package_manager="pacman",
                init_system="systemd",
                kernel="latest",
                base_size_gb=1,
                description="Rolling release - bleeding edge"
            ),
            "fedora": DistroOption(
                name="Fedora 40",
                package_manager="dnf",
                init_system="systemd",
                kernel="6.8",
                base_size_gb=2,
                description="Cutting edge, good for ML/AI"
            ),
            "nixos": DistroOption(
                name="NixOS 24.05",
                package_manager="nix",
                init_system="systemd",
                kernel="6.6",
                base_size_gb=3,
                description="Declarative config - reproducible builds"
            ),
        }
    
    def run(self, stdscr):
        """Main TUI loop"""
        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(1)   # Non-blocking input
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        
        while self.is_running:
            stdscr.clear()
            
            if self.current_menu == "main":
                self._draw_main_menu(stdscr)
            elif self.current_menu == "distros":
                self._draw_distro_menu(stdscr)
            elif self.current_menu == "details":
                self._draw_distro_details(stdscr)
            elif self.current_menu == "build":
                self._draw_build_screen(stdscr)
            
            stdscr.refresh()
            
            # Handle input
            try:
                key = stdscr.getch()
                if key != -1:
                    self._handle_input(key)
            except:
                pass
            
            time.sleep(0.05)
    
    def _draw_main_menu(self, stdscr):
        """Draw main menu"""
        h, w = stdscr.getmaxyx()
        
        # Banner
        banner = [
            "╔══════════════════════════════════════════════════════════╗",
            "║                                                          ║",
            "║     🗺️  QUETZAL TERMINAL INTERFACE (QTI) - Ubuntu        ║",
            "║              Distro Builder & Manager                    ║",
            "║                                                          ║",
            "╚══════════════════════════════════════════════════════════╝",
        ]
        
        for i, line in enumerate(banner):
            if i < h:
                stdscr.addstr(i, 0, line, curses.color_pair(2))
        
        menu_items = [
            "1. Build New System",
            "2. Select Distro",
            "3. View Current System",
            "4. System Status",
            "5. Settings",
            "Q. Quit",
        ]
        
        start_y = len(banner) + 2
        for i, item in enumerate(menu_items):
            if start_y + i < h:
                attr = curses.color_pair(1) if i == self.selected_option else curses.A_NORMAL
                stdscr.addstr(start_y + i, 2, item, attr)
        
        # Footer
        if h > len(banner) + len(menu_items) + 3:
            footer = "Use ↑↓ arrows to navigate, ENTER to select"
            stdscr.addstr(h - 2, 2, footer, curses.color_pair(3))
    
    def _draw_distro_menu(self, stdscr):
        """Draw distro selection menu"""
        h, w = stdscr.getmaxyx()
        
        title = "SELECT DISTRO FOR REBUILD"
        stdscr.addstr(0, 0, title, curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(1, 0, "=" * len(title))
        
        distro_list = list(self.distros.items())
        
        for idx, (key, distro) in enumerate(distro_list):
            if idx + 2 < h:
                prefix = "→ " if idx == self.selected_option else "  "
                attr = curses.color_pair(1) if idx == self.selected_option else curses.A_NORMAL
                
                line = f"{prefix}{distro.name:30} ({distro.base_size_gb}GB)"
                stdscr.addstr(idx + 2, 0, line, attr)
        
        if h > len(distro_list) + 4:
            stdscr.addstr(h - 2, 0, "↑↓ Navigate | ENTER Details | Q Back", curses.color_pair(3))
    
    def _draw_distro_details(self, stdscr):
        """Draw distro details and confirmation"""
        h, w = stdscr.getmaxyx()
        
        if not self.selected_distro:
            return
        
        distro = self.selected_distro
        
        stdscr.addstr(0, 0, f"DISTRO: {distro.name}", curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(1, 0, "=" * 60)
        
        details = [
            f"Description: {distro.description}",
            f"Package Manager: {distro.package_manager}",
            f"Init System: {distro.init_system}",
            f"Kernel: {distro.kernel}",
            f"Base Size: {distro.base_size_gb}GB",
            "",
            "This will:",
            "  • Download distro base image",
            "  • Install Quetzal Core",
            "  • Configure GIS Studio",
            "  • Setup system services",
            "",
            "Estimated time: 5-15 minutes",
        ]
        
        for i, line in enumerate(details):
            if i + 2 < h - 3:
                if "This will:" in line:
                    stdscr.addstr(i + 2, 0, line, curses.color_pair(2))
                else:
                    stdscr.addstr(i + 2, 0, line)
        
        # Action menu
        actions = [
            "1. START BUILD",
            "2. View Build Script",
            "3. Save Config",
            "Q. Cancel",
        ]
        
        action_start = h - len(actions) - 2
        for i, action in enumerate(actions):
            if action_start + i >= 0:
                attr = curses.color_pair(4) if "START" in action else curses.A_NORMAL
                stdscr.addstr(action_start + i, 0, action, attr)
    
    def _draw_build_screen(self, stdscr):
        """Draw build progress screen"""
        h, w = stdscr.getmaxyx()
        
        stdscr.addstr(0, 0, "🔨 BUILDING NEW SYSTEM", curses.color_pair(4) | curses.A_BOLD)
        stdscr.addstr(1, 0, "=" * 60)
        
        # Progress steps
        steps = [
            ("Downloading base image", self.output_buffer[0] if len(self.output_buffer) > 0 else ""),
            ("Extracting filesystem", self.output_buffer[1] if len(self.output_buffer) > 1 else ""),
            ("Installing Quetzal Core", self.output_buffer[2] if len(self.output_buffer) > 2 else ""),
            ("Configuring services", self.output_buffer[3] if len(self.output_buffer) > 3 else ""),
            ("Setting up GIS Studio", self.output_buffer[4] if len(self.output_buffer) > 4 else ""),
        ]
        
        for i, (step, status) in enumerate(steps):
            if i + 3 < h - 5:
                status_char = "✓" if status else "..." 
                color = curses.color_pair(2) if status else curses.color_pair(3)
                line = f"[{status_char}] {step}"
                stdscr.addstr(i + 3, 2, line, color)
        
        if len(self.output_buffer) > 0:
            log_start = len(steps) + 4
            stdscr.addstr(log_start, 0, "Build Log:")
            for i, log_line in enumerate(self.output_buffer[-5:]):
                if log_start + 1 + i < h - 1:
                    stdscr.addstr(log_start + 1 + i, 2, log_line[:w-4], curses.color_pair(3))
        
        if len(self.output_buffer) >= 5:
            stdscr.addstr(h - 1, 0, "✓ Build Complete! Press ENTER to continue", curses.color_pair(2))
    
    def _handle_input(self, key):
        """Handle keyboard input"""
        if key == ord('q') or key == ord('Q'):
            if self.current_menu == "main":
                self.is_running = False
            else:
                self.current_menu = "main"
        
        elif key == curses.KEY_UP:
            self.selected_option = max(0, self.selected_option - 1)
        
        elif key == curses.KEY_DOWN:
            num_options = len(self.distros) if self.current_menu == "distros" else 6
            self.selected_option = min(num_options - 1, self.selected_option + 1)
        
        elif key == ord('\n'):  # Enter key
            if self.current_menu == "main":
                if self.selected_option == 0:
                    self.current_menu = "distros"
                    self.selected_option = 0
                elif self.selected_option == 1:
                    self.current_menu = "distros"
                    self.selected_option = 0
                elif self.selected_option == 2:
                    self.show_current_system()
                elif self.selected_option == 3:
                    self.show_system_status()
            
            elif self.current_menu == "distros":
                distro_key = list(self.distros.keys())[self.selected_option]
                self.selected_distro = self.distros[distro_key]
                self.current_menu = "details"
            
            elif self.current_menu == "details":
                if self.selected_option == 0:  # START BUILD
                    self.start_build()
                elif self.selected_option == 1:  # View Script
                    self.show_build_script()
                elif self.selected_option == 2:  # Save Config
                    self.save_config()
    
    def start_build(self):
        """Start building the new distro"""
        self.current_menu = "build"
        self.output_buffer = []
        
        # Simulate build process
        def simulate_build():
            steps = [
                "Downloading base image...",
                "Extracting filesystem...",
                "Installing Quetzal Core...",
                "Configuring systemd services...",
                "Setting up GIS Studio...",
            ]
            for step in steps:
                self.output_buffer.append(step)
                time.sleep(0.5)
        
        thread = threading.Thread(target=simulate_build)
        thread.daemon = True
        thread.start()
    
    def show_current_system(self):
        """Show current system information"""
        pass
    
    def show_system_status(self):
        """Show system status"""
        pass
    
    def show_build_script(self):
        """Show build script"""
        pass
    
    def save_config(self):
        """Save build configuration"""
        pass


def create_ubuntu_installer_script():
    """Create the Ubuntu installer script"""
    script = """#!/bin/bash
# Quetzal Terminal Interface (QTI) Installer for Ubuntu
# This script downloads and sets up QTI

set -e

echo "🗺️  Installing Quetzal Terminal Interface (QTI)..."
echo ""

# Detect Ubuntu version
UBUNTU_VERSION=$(lsb_release -rs)
echo "✓ Detected Ubuntu $UBUNTU_VERSION"

# Install dependencies
echo "Installing dependencies..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-dev

# Clone or download QTI
echo "Setting up QTI..."
QTI_DIR="/opt/qti"
sudo mkdir -p $QTI_DIR
sudo cp qti_ubuntu_app.py $QTI_DIR/

# Create launcher script
sudo tee /usr/local/bin/qti > /dev/null << 'EOF'
#!/bin/bash
cd /opt/qti
python3 -m curses qti_ubuntu_app.py
EOF

sudo chmod +x /usr/local/bin/qti

echo ""
echo "✅ QTI installed successfully!"
echo ""
echo "Launch with: qti"
"""
    return script


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        # Generate installer
        installer = create_ubuntu_installer_script()
        print(installer)
        return
    
    # Run TUI
    try:
        app = QTIApp()
        curses.wrapper(app.run)
    except KeyboardInterrupt:
        print("\nQTI closed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
