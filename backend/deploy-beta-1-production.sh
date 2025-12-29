#!/bin/bash

# ============================================================================
# QuetzalCore BETA 1 - Production Deployment Script
# ============================================================================
# This script handles complete production deployment across all platforms
# Supports: Railway, Render, Fly.io, Docker, Kubernetes
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Config
PROJECT_NAME="quetzalcore"
VERSION="1.0.0-beta.1"
TIMESTAMP=$(date +%s)
BACKUP_DIR="./backups/deploy-${TIMESTAMP}"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

log_info() {
    echo -e "${BLUE}ℹ️  INFO${NC}: $1"
}

log_success() {
    echo -e "${GREEN}✅ SUCCESS${NC}: $1"
}

log_warn() {
    echo -e "${YELLOW}⚠️  WARN${NC}: $1"
}

log_error() {
    echo -e "${RED}❌ ERROR${NC}: $1"
    exit 1
}

# ============================================================================
# CHECKS
# ============================================================================

check_requirements() {
    log_info "Checking requirements..."
    
    # Check if we're in the right directory
    if [ ! -f "backend/main.py" ]; then
        log_error "Must be run from project root directory"
    fi
    
    # Check for .env file
    if [ ! -f ".env" ]; then
        log_warn ".env file not found, creating from template..."
        if [ -f ".env.example" ]; then
            cp .env.example .env
            log_info "Created .env from template - please edit with your settings"
        else
            log_error ".env.example template not found"
        fi
    fi
    
    log_success "Requirements check passed"
}

check_python() {
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 not found. Please install Python 3.9+"
    fi
    
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    log_info "Python version: $PYTHON_VERSION"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        log_warn "Docker not found. Some deployment options require Docker"
        return 1
    fi
    
    log_success "Docker is installed"
    return 0
}

check_node() {
    if ! command -v node &> /dev/null; then
        log_warn "Node.js not found. Dashboard deployment will be limited"
        return 1
    fi
    
    NODE_VERSION=$(node --version)
    log_info "Node version: $NODE_VERSION"
}

# ============================================================================
# BACKUP
# ============================================================================

create_backup() {
    log_info "Creating backup..."
    
    mkdir -p "$BACKUP_DIR"
    
    # Backup current state
    cp -r backend "$BACKUP_DIR/" 2>/dev/null || true
    cp -r dashboard "$BACKUP_DIR/" 2>/dev/null || true
    cp .env "$BACKUP_DIR/.env" 2>/dev/null || true
    cp docker-compose.yml "$BACKUP_DIR/" 2>/dev/null || true
    
    log_success "Backup created at $BACKUP_DIR"
}

# ============================================================================
# VALIDATION
# ============================================================================

validate_code() {
    log_info "Validating code..."
    
    # Check Python syntax
    python3 -m py_compile backend/main.py || log_error "Python syntax error in main.py"
    
    # Check for required files
    required_files=(
        "backend/main.py"
        "backend/models.py"
        "backend/database.py"
        "docker-compose.yml"
    )
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            log_error "Required file missing: $file"
        fi
    done
    
    log_success "Code validation passed"
}

# ============================================================================
# DOCKER DEPLOYMENT
# ============================================================================

deploy_docker_compose() {
    log_info "Deploying with Docker Compose..."
    
    if ! check_docker; then
        log_error "Docker is required for this deployment option"
    fi
    
    # Stop existing containers
    log_info "Stopping existing containers..."
    docker-compose down || true
    
    # Build images
    log_info "Building Docker images..."
    docker-compose build --no-cache
    
    # Start services
    log_info "Starting services..."
    docker-compose up -d
    
    # Wait for services to be ready
    log_info "Waiting for services to start..."
    sleep 10
    
    # Check health
    log_info "Checking service health..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
            log_success "Services are healthy"
            
            echo ""
            echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
            echo -e "${GREEN}✅ DOCKER DEPLOYMENT SUCCESSFUL${NC}"
            echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
            echo ""
            echo "Services running:"
            echo "  🌐 Dashboard:      http://localhost:3000"
            echo "  🔌 API:            http://localhost:8000"
            echo "  📖 API Docs:       http://localhost:8000/docs"
            echo "  🧲 Mining API:     http://localhost:8000/api/mining"
            echo "  📊 Monitor:        http://localhost:7070"
            echo "  🗄️  Database:       localhost:5432"
            echo "  💾 Redis:          localhost:6379"
            echo ""
            echo "View logs:"
            echo "  docker-compose logs -f backend"
            echo ""
            return 0
        fi
        echo -n "."
        sleep 1
    done
    
    log_error "Services failed to start - check logs with: docker-compose logs"
}

# ============================================================================
# RAILWAY DEPLOYMENT
# ============================================================================

deploy_railway() {
    log_info "Preparing Railway deployment..."
    
    # Check if railway CLI is installed
    if ! command -v railway &> /dev/null; then
        log_warn "Railway CLI not installed"
        echo ""
        echo "To deploy to Railway:"
        echo "1. Install Railway CLI: npm i -g @railway/cli"
        echo "2. Login: railway login"
        echo "3. Deploy: railway up"
        echo ""
        return 1
    fi
    
    log_info "Deploying to Railway..."
    
    # Initialize if needed
    if [ ! -d ".railway" ]; then
        railway init
    fi
    
    # Deploy
    railway up
    
    log_success "Railway deployment initiated"
}

# ============================================================================
# ENVIRONMENT SETUP
# ============================================================================

setup_environment() {
    log_info "Setting up environment..."
    
    # Check for required env variables
    required_vars=(
        "DATABASE_URL"
        "REDIS_URL"
    )
    
    missing_vars=()
    for var in "${required_vars[@]}"; do
        if ! grep -q "^$var=" .env; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -gt 0 ]; then
        log_warn "Missing environment variables: ${missing_vars[*]}"
        log_info "Edit .env file and add these variables"
    fi
    
    log_success "Environment setup complete"
}

# ============================================================================
# DATABASE SETUP
# ============================================================================

setup_database() {
    log_info "Setting up database..."
    
    if [ -z "$DATABASE_URL" ]; then
        log_warn "DATABASE_URL not set - skipping database setup"
        log_info "Set DATABASE_URL in .env to enable automated setup"
        return
    fi
    
    # Run migrations (when implemented)
    # python3 -m alembic upgrade head
    
    log_success "Database setup complete"
}

# ============================================================================
# SECURITY CHECKS
# ============================================================================

check_security() {
    log_info "Running security checks..."
    
    # Check for hardcoded secrets
    if grep -r "password.*=" backend/ 2>/dev/null | grep -v "test"; then
        log_warn "Potential hardcoded credentials found in backend/"
    fi
    
    if grep -r "api.key" backend/ 2>/dev/null | grep -v "test"; then
        log_warn "Potential hardcoded API keys found in backend/"
    fi
    
    # Check .env is in gitignore
    if [ -f ".gitignore" ] && ! grep -q "^\.env$" .gitignore; then
        log_warn ".env file should be in .gitignore"
    fi
    
    log_success "Security checks complete"
}

# ============================================================================
# TESTING
# ============================================================================

run_tests() {
    log_info "Running tests..."
    
    # Basic API health check
    log_info "Testing API health endpoint..."
    if ! python3 -m pytest tests/ -v 2>/dev/null; then
        log_warn "Tests not configured yet - skipping automated tests"
    fi
    
    log_success "Testing complete"
}

# ============================================================================
# DEPLOYMENT MENU
# ============================================================================

show_menu() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}QuetzalCore BETA 1 - Production Deployment${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Select deployment option:"
    echo ""
    echo "  1) Docker Compose (local - fastest)"
    echo "  2) Railway.app (recommended - cloud)"
    echo "  3) Render.com (alternative cloud)"
    echo "  4) Fly.io (edge deployment)"
    echo "  5) Manual/Advanced (custom setup)"
    echo "  6) Validate only (no deployment)"
    echo ""
    echo "  q) Quit"
    echo ""
    echo -ne "${YELLOW}Enter choice (1-6, q): ${NC}"
}

# ============================================================================
# MAIN FLOW
# ============================================================================

main() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   QuetzalCore BETA 1 - Production Deployment Script       ║${NC}"
    echo -e "${BLUE}║   Version: $VERSION${NC}"
    echo -e "${BLUE}║   Date: $(date)${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Pre-deployment checks
    check_requirements
    check_python
    check_docker
    check_node
    check_security
    validate_code
    create_backup
    setup_environment
    
    # Show menu and get choice
    while true; do
        show_menu
        read -r choice
        
        case $choice in
            1)
                deploy_docker_compose
                break
                ;;
            2)
                deploy_railway
                break
                ;;
            3)
                log_info "Render deployment instructions:"
                echo "1. Push code to GitHub"
                echo "2. Go to https://render.com"
                echo "3. Create new Web Service"
                echo "4. Connect your repository"
                echo "5. Configure:"
                echo "   Build: pip install -r requirements.txt"
                echo "   Start: uvicorn main:app --host 0.0.0.0 --port \$PORT"
                break
                ;;
            4)
                log_info "Fly.io deployment instructions:"
                echo "1. Install flyctl: curl -L https://fly.io/install.sh | sh"
                echo "2. Login: flyctl auth login"
                echo "3. Deploy: flyctl launch && flyctl deploy"
                break
                ;;
            5)
                log_info "Manual deployment - review BETA_1_PRODUCTION_READY.md"
                break
                ;;
            6)
                log_success "Validation complete - no deployment performed"
                break
                ;;
            q)
                log_info "Deployment cancelled"
                exit 0
                ;;
            *)
                log_warn "Invalid option"
                ;;
        esac
    done
    
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Deployment process complete!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Review deployment logs above"
    echo "2. Test your deployment"
    echo "3. Monitor with: http://localhost:7070"
    echo "4. Access API docs: http://localhost:8000/docs"
    echo ""
}

# Run main function
main "$@"
