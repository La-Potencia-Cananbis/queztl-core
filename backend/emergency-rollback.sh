#!/bin/bash
# Emergency Rollback Script
# Script de Reversión de Emergencia
#
# Copyright (c) 2025 Queztl-Core Project
# CONFIDENTIAL - PATENT PENDING

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     🚨 EMERGENCY ROLLBACK - REVERSIÓN DE EMERGENCIA 🚨      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups"
EMERGENCY_BACKUP="emergency-backup-$DATE.tar.gz"
ROLLBACK_TARGET="${1:-v0.9.0}"  # Default to v0.9.0 if not specified

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

confirm() {
    read -p "$1 (yes/no): " response
    if [ "$response" != "yes" ]; then
        log_error "Operation cancelled by user"
        exit 1
    fi
}

# Main rollback procedure
main() {
    echo "🚨 CRITICAL: This will rollback to version: $ROLLBACK_TARGET"
    echo "🚨 CRÍTICO: Esto revertirá a la versión: $ROLLBACK_TARGET"
    echo ""
    confirm "Are you sure you want to proceed? / ¿Estás seguro que quieres continuar?"

    # Step 1: Stop all services
    log_info "Step 1/7: Stopping all services / Deteniendo todos los servicios..."
    docker-compose down || log_warn "Docker compose down failed (may be already down)"

    # Step 2: Backup current state
    log_info "Step 2/7: Backing up current state / Respaldando estado actual..."
    mkdir -p "$BACKUP_DIR/emergency"
    
    # Backup database
    if docker ps -a | grep -q postgres; then
        log_info "Backing up database / Respaldando base de datos..."
        docker-compose up -d postgres
        sleep 5
        docker-compose exec -T postgres pg_dump -U queztl queztl_db > "$BACKUP_DIR/emergency/db-before-rollback-$DATE.sql"
        gzip "$BACKUP_DIR/emergency/db-before-rollback-$DATE.sql"
        docker-compose down
    fi
    
    # Backup current files
    log_info "Backing up current files / Respaldando archivos actuales..."
    tar -czf "$BACKUP_DIR/emergency/$EMERGENCY_BACKUP" \
        --exclude='node_modules' \
        --exclude='__pycache__' \
        --exclude='.git' \
        --exclude='*.pyc' \
        --exclude='backups' \
        . 2>/dev/null || log_warn "Some files skipped during backup"

    # Step 3: Restore configuration
    log_info "Step 3/7: Restoring configuration / Restaurando configuración..."
    
    # Find latest config backup
    LATEST_ENV=$(ls -t "$BACKUP_DIR/config/.env-"* 2>/dev/null | head -1)
    if [ -n "$LATEST_ENV" ]; then
        cp "$LATEST_ENV" .env
        log_info "Restored .env from $LATEST_ENV"
    else
        log_warn "No .env backup found, keeping current"
    fi

    # Step 4: Checkout previous version
    log_info "Step 4/7: Checking out version $ROLLBACK_TARGET / Cambiando a versión $ROLLBACK_TARGET..."
    
    # Stash any uncommitted changes
    git stash save "Emergency rollback stash - $DATE" 2>/dev/null || true
    
    # Fetch all tags
    git fetch --all --tags
    
    # Checkout target version
    if git tag | grep -q "^$ROLLBACK_TARGET$"; then
        git checkout "$ROLLBACK_TARGET"
        log_info "Checked out tag $ROLLBACK_TARGET"
    else
        log_error "Version $ROLLBACK_TARGET not found!"
        log_error "Available versions:"
        git tag -l
        exit 1
    fi

    # Step 5: Restore database
    log_info "Step 5/7: Restoring database / Restaurando base de datos..."
    
    # Find latest DB backup
    LATEST_DB=$(ls -t "$BACKUP_DIR/database/"*.sql.gz 2>/dev/null | head -1)
    if [ -n "$LATEST_DB" ]; then
        log_info "Restoring database from $LATEST_DB"
        docker-compose up -d postgres
        sleep 10
        gunzip -c "$LATEST_DB" | docker-compose exec -T postgres psql -U queztl -d queztl_db
        docker-compose down
    else
        log_warn "No database backup found, skipping database restore"
    fi

    # Step 6: Rebuild and restart services
    log_info "Step 6/7: Rebuilding services / Reconstruyendo servicios..."
    docker-compose build

    log_info "Starting services / Iniciando servicios..."
    docker-compose up -d

    # Step 7: Verify system health
    log_info "Step 7/7: Verifying system health / Verificando salud del sistema..."
    sleep 15

    # Check backend health
    if curl -f http://localhost:8000/health 2>/dev/null; then
        log_info "✅ Backend health check passed"
    else
        log_error "❌ Backend health check failed!"
        log_error "Check logs: docker-compose logs backend"
    fi

    # Check dashboard
    if curl -f http://localhost:3000 2>/dev/null; then
        log_info "✅ Dashboard check passed"
    else
        log_warn "⚠️  Dashboard check failed (may still be starting)"
    fi

    # Final summary
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              ✅ ROLLBACK COMPLETE / COMPLETO                 ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📊 Summary / Resumen:"
    echo "  - Rolled back to version / Revertido a versión: $ROLLBACK_TARGET"
    echo "  - Emergency backup created / Respaldo emergencia creado: $EMERGENCY_BACKUP"
    echo "  - Services restarted / Servicios reiniciados: ✅"
    echo ""
    echo "📋 Next Steps / Próximos Pasos:"
    echo "  1. Review logs / Revisar logs:"
    echo "     docker-compose logs --tail=100 -f"
    echo ""
    echo "  2. Run tests / Ejecutar pruebas:"
    echo "     ./test-webgpu.sh"
    echo ""
    echo "  3. Create incident report / Crear reporte incidente:"
    echo "     See VERSIONING.md for template"
    echo ""
    echo "  4. Plan hotfix / Planear corrección rápida:"
    echo "     git checkout -b hotfix-emergency-$DATE"
    echo ""
    echo "💾 Emergency backup location / Ubicación respaldo emergencia:"
    echo "   $BACKUP_DIR/emergency/$EMERGENCY_BACKUP"
    echo ""
    
    # Log rollback event
    echo "$(date): Emergency rollback to $ROLLBACK_TARGET completed" >> "$BACKUP_DIR/rollback.log"
}

# Run main function
main

exit 0
