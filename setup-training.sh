#!/bin/bash
# Queztl Training System - Interactive Setup & Demo

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

clear

echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║          ██████╗ ██╗   ██╗███████╗███████╗████████╗██╗                   ║
║         ██╔═══██╗██║   ██║██╔════╝╚══███╔╝╚══██╔══╝██║                   ║
║         ██║   ██║██║   ██║█████╗    ███╔╝    ██║   ██║                   ║
║         ██║▄▄ ██║██║   ██║██╔══╝   ███╔╝     ██║   ██║                   ║
║         ╚██████╔╝╚██████╔╝███████╗███████╗   ██║   ███████╗              ║
║          ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚══════╝              ║
║                                                                           ║
║                    TRAINING SYSTEM SETUP & DEMO                          ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo ""
echo "Welcome to the Queztl Training System!"
echo ""
echo "This system provides TWO powerful training solutions:"
echo ""
echo -e "${GREEN}1. QTM (Queztl Training Manager)${NC}"
echo "   - Simple, apt-like interface"
echo "   - Perfect for quick training"
echo "   - Command: ./qtm <command>"
echo ""
echo -e "${GREEN}2. Hive (Distributed Training)${NC}"
echo "   - Kubernetes-like orchestration"
echo "   - Parallel training with multiple runners"
echo "   - Command: ./hive-control <command>"
echo ""
echo "────────────────────────────────────────────────────────────────────"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found${NC}"
    echo "   Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "${GREEN}✅ Docker installed${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}⚠️  docker-compose not found (optional for Hive)${NC}"
else
    echo -e "${GREEN}✅ Docker Compose installed${NC}"
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python 3 installed${NC}"

echo ""
echo "────────────────────────────────────────────────────────────────────"
echo ""

# Interactive menu
while true; do
    echo "What would you like to do?"
    echo ""
    echo "  1) Test QTM (Quick & Easy)"
    echo "  2) Setup Hive (Distributed Training)"
    echo "  3) View Available Modules"
    echo "  4) Check System Status"
    echo "  5) Read Documentation"
    echo "  6) Exit"
    echo ""
    read -p "Enter choice [1-6]: " choice
    
    case $choice in
        1)
            clear
            echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
            echo -e "${BLUE}   QTM DEMO${NC}"
            echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
            echo ""
            
            echo "📦 Listing all available modules..."
            echo ""
            ./qtm list
            
            echo ""
            echo "🔍 Searching for '3D' modules..."
            echo ""
            ./qtm search 3d
            
            echo ""
            echo "ℹ️  Getting info about 'gis-lidar'..."
            echo ""
            ./qtm info gis-lidar
            
            echo ""
            echo "🔧 Checking dependencies..."
            echo ""
            ./qtm check-deps
            
            echo ""
            echo "📊 Checking training status..."
            echo ""
            ./qtm status
            
            echo ""
            echo -e "${GREEN}✅ QTM Demo Complete!${NC}"
            echo ""
            echo "To train a module, run:"
            echo "  ${YELLOW}./qtm install <module-id>${NC}"
            echo ""
            echo "For example:"
            echo "  ${YELLOW}./qtm install gis-lidar${NC}"
            echo ""
            read -p "Press Enter to continue..."
            clear
            ;;
        
        2)
            clear
            echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
            echo -e "${BLUE}   HIVE SETUP${NC}"
            echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
            echo ""
            
            if ! command -v docker-compose &> /dev/null; then
                echo -e "${RED}❌ Docker Compose is required for Hive${NC}"
                echo "   Install it from: https://docs.docker.com/compose/install/"
                echo ""
                read -p "Press Enter to continue..."
                clear
                continue
            fi
            
            echo "This will:"
            echo "  1. Build orchestrator image"
            echo "  2. Build runner image"
            echo "  3. Create necessary directories"
            echo ""
            read -p "Proceed with setup? (y/n) " -n 1 -r
            echo ""
            
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo ""
                echo "🚀 Initializing Hive..."
                ./hive-control init
                
                echo ""
                echo -e "${GREEN}✅ Hive initialized!${NC}"
                echo ""
                echo "Next steps:"
                echo "  1. Start the hive: ${YELLOW}./hive-control start${NC}"
                echo "  2. Check status: ${YELLOW}./hive-control status${NC}"
                echo "  3. Submit jobs: ${YELLOW}./hive-control submit <module> high${NC}"
                echo "  4. Scale up: ${YELLOW}./hive-control scale 4${NC}"
                echo ""
            fi
            
            read -p "Press Enter to continue..."
            clear
            ;;
        
        3)
            clear
            echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
            echo -e "${BLUE}   AVAILABLE TRAINING MODULES${NC}"
            echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
            echo ""
            
            ./qtm list
            
            echo ""
            echo "To get details about a module:"
            echo "  ${YELLOW}./qtm info <module-id>${NC}"
            echo ""
            echo "To search for modules:"
            echo "  ${YELLOW}./qtm search <keyword>${NC}"
            echo ""
            read -p "Press Enter to continue..."
            clear
            ;;
        
        4)
            clear
            echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
            echo -e "${BLUE}   SYSTEM STATUS${NC}"
            echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
            echo ""
            
            echo "📊 QTM Status:"
            echo ""
            ./qtm status
            
            echo ""
            echo "────────────────────────────────────────────────────────────"
            echo ""
            
            if command -v docker-compose &> /dev/null; then
                echo "🐝 Hive Status:"
                echo ""
                
                if curl -sf http://localhost:9000/health > /dev/null 2>&1; then
                    ./hive-control status
                else
                    echo "Hive not running (use './hive-control start')"
                fi
            fi
            
            echo ""
            read -p "Press Enter to continue..."
            clear
            ;;
        
        5)
            clear
            echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
            echo -e "${BLUE}   DOCUMENTATION${NC}"
            echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
            echo ""
            
            echo "📚 Available documentation:"
            echo ""
            echo "  1. QTM Quick Reference"
            echo "     ${YELLOW}cat QTM_QUICKREF.md${NC}"
            echo ""
            echo "  2. Hive Full Guide"
            echo "     ${YELLOW}cat training-runner/README.md${NC}"
            echo ""
            echo "  3. Training System Complete"
            echo "     ${YELLOW}cat TRAINING_SYSTEM_COMPLETE.md${NC}"
            echo ""
            echo "  4. QTM Help"
            echo "     ${YELLOW}./qtm --help${NC}"
            echo ""
            echo "  5. Hive Help"
            echo "     ${YELLOW}./hive-control${NC}"
            echo ""
            
            read -p "View which doc? [1-5, or Enter to skip]: " doc_choice
            
            case $doc_choice in
                1) less QTM_QUICKREF.md ;;
                2) less training-runner/README.md ;;
                3) less TRAINING_SYSTEM_COMPLETE.md ;;
                4) ./qtm --help | less ;;
                5) ./hive-control | less ;;
            esac
            
            clear
            ;;
        
        6)
            echo ""
            echo -e "${GREEN}Thank you for using Queztl Training System!${NC}"
            echo ""
            echo "Quick reference:"
            echo "  QTM:  ${YELLOW}./qtm list${NC}"
            echo "  Hive: ${YELLOW}./hive-control status${NC}"
            echo ""
            exit 0
            ;;
        
        *)
            echo -e "${RED}Invalid choice${NC}"
            echo ""
            ;;
    esac
done
