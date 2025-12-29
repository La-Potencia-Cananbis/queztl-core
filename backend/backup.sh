#!/bin/bash
# Automated Backup Script
# Script de Respaldo Automatizado
#
# Copyright (c) 2025 Queztl-Core Project
# CONFIDENTIAL - PATENT PENDING

set -e

# Configuration
DATE=$(date +%Y%m%d_%H%M%S)
DATE_SHORT=$(date +%Y%m%d)
BACKUP_DIR="backups"

# Retention periods (in days)
DB_RETENTION=30
CODE_RETENTION=84
CONFIG_RETENTION=90

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# Create backup directories
mkdir -p "$BACKUP_DIR/database"
mkdir -p "$BACKUP_DIR/code"
mkdir -p "$BACKUP_DIR/config"
mkdir -p "$BACKUP_DIR/docker"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         💾 AUTOMATED BACKUP - RESPALDO AUTOMATIZADO         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# 1. Database Backup
log_info "📊 Backing up database / Respaldando base de datos..."
if docker-compose ps | grep -q postgres; then
    docker-compose exec -T postgres pg_dump -U queztl queztl_db \
        > "$BACKUP_DIR/database/backup-$DATE.sql"
    
    # Compress
    gzip "$BACKUP_DIR/database/backup-$DATE.sql"
    
    # Get file size
    SIZE=$(du -h "$BACKUP_DIR/database/backup-$DATE.sql.gz" | cut -f1)
    log_info "   ✅ Database backup complete: $SIZE"
    
    # Clean old backups
    find "$BACKUP_DIR/database" -name "*.sql.gz" -mtime +$DB_RETENTION -delete
    log_info "   🧹 Cleaned backups older than $DB_RETENTION days"
else
    log_warn "   ⚠️  PostgreSQL not running, skipping database backup"
fi

# 2. Code Backup
log_info "📦 Backing up code / Respaldando código..."
tar -czf "$BACKUP_DIR/code/code-$DATE_SHORT.tar.gz" \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='*.pyc' \
    --exclude='backups' \
    --exclude='.env' \
    --exclude='*.log' \
    . 2>/dev/null

SIZE=$(du -h "$BACKUP_DIR/code/code-$DATE_SHORT.tar.gz" | cut -f1)
log_info "   ✅ Code backup complete: $SIZE"

# Clean old backups
find "$BACKUP_DIR/code" -name "*.tar.gz" -mtime +$CODE_RETENTION -delete
log_info "   🧹 Cleaned backups older than $CODE_RETENTION days"

# 3. Configuration Backup
log_info "⚙️  Backing up configuration / Respaldando configuración..."

# Backup .env if it exists
if [ -f .env ]; then
    cp .env "$BACKUP_DIR/config/.env-$DATE_SHORT"
    log_info "   ✅ .env backed up"
fi

# Backup docker-compose.yml
if [ -f docker-compose.yml ]; then
    cp docker-compose.yml "$BACKUP_DIR/config/docker-compose.yml-$DATE_SHORT"
    log_info "   ✅ docker-compose.yml backed up"
fi

# Backup requirements.txt
if [ -f backend/requirements.txt ]; then
    cp backend/requirements.txt "$BACKUP_DIR/config/requirements.txt-$DATE_SHORT"
    log_info "   ✅ requirements.txt backed up"
fi

# Backup package.json
if [ -f dashboard/package.json ]; then
    cp dashboard/package.json "$BACKUP_DIR/config/package.json-$DATE_SHORT"
    log_info "   ✅ package.json backed up"
fi

# Clean old configs
find "$BACKUP_DIR/config" -type f -mtime +$CONFIG_RETENTION -delete
log_info "   🧹 Cleaned backups older than $CONFIG_RETENTION days"

# 4. Docker Images Backup
log_info "🐳 Backing up Docker images / Respaldando imágenes Docker..."

# Get current version tag
VERSION=$(git describe --tags --always 2>/dev/null || echo "latest")

# Save backend image
if docker images | grep -q "hive-backend"; then
    docker save hive-backend:latest | gzip > "$BACKUP_DIR/docker/backend-$VERSION-$DATE_SHORT.tar.gz"
    log_info "   ✅ Backend image saved: backend-$VERSION"
fi

# Save dashboard image
if docker images | grep -q "hive-dashboard"; then
    docker save hive-dashboard:latest | gzip > "$BACKUP_DIR/docker/dashboard-$VERSION-$DATE_SHORT.tar.gz"
    log_info "   ✅ Dashboard image saved: dashboard-$VERSION"
fi

# Keep only last 10 image backups
ls -t "$BACKUP_DIR/docker/"*.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm
log_info "   🧹 Kept only last 10 image backups"

# 5. Generate backup report
log_info "📝 Generating backup report / Generando reporte respaldo..."

REPORT="$BACKUP_DIR/backup-report-$DATE_SHORT.txt"
cat > "$REPORT" << EOF
╔══════════════════════════════════════════════════════════════╗
║               BACKUP REPORT / REPORTE RESPALDO               ║
╚══════════════════════════════════════════════════════════════╝

Date / Fecha: $(date)
Version: $VERSION

📊 Database Backups / Respaldos Base de Datos:
$(ls -lh "$BACKUP_DIR/database/"*.sql.gz 2>/dev/null | tail -5 || echo "   None / Ninguno")

📦 Code Backups / Respaldos Código:
$(ls -lh "$BACKUP_DIR/code/"*.tar.gz 2>/dev/null | tail -5 || echo "   None / Ninguno")

⚙️  Configuration Backups / Respaldos Configuración:
$(ls -lh "$BACKUP_DIR/config/" 2>/dev/null | tail -10 || echo "   None / Ninguno")

🐳 Docker Image Backups / Respaldos Imágenes Docker:
$(ls -lh "$BACKUP_DIR/docker/"*.tar.gz 2>/dev/null | tail -5 || echo "   None / Ninguno")

💾 Total Backup Size / Tamaño Total Respaldo:
$(du -sh "$BACKUP_DIR" | cut -f1)

📈 Disk Usage / Uso Disco:
$(df -h . | tail -1)

🔒 CONFIDENTIAL - PATENT PENDING
🔒 CONFIDENCIAL - PATENTE PENDIENTE
Copyright (c) 2025 Queztl-Core Project
EOF

log_info "   ✅ Backup report created: $REPORT"

# 6. Summary
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║            ✅ BACKUP COMPLETE / COMPLETO                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Backup Summary / Resumen Respaldo:"
echo ""
echo "   Database / Base de Datos:"
echo "     - Location: $BACKUP_DIR/database/"
echo "     - Latest: backup-$DATE.sql.gz"
echo "     - Retention: $DB_RETENTION days"
echo ""
echo "   Code / Código:"
echo "     - Location: $BACKUP_DIR/code/"
echo "     - Latest: code-$DATE_SHORT.tar.gz"
echo "     - Retention: $CODE_RETENTION days"
echo ""
echo "   Configuration / Configuración:"
echo "     - Location: $BACKUP_DIR/config/"
echo "     - Files: .env, docker-compose.yml, requirements.txt, package.json"
echo "     - Retention: $CONFIG_RETENTION days"
echo ""
echo "   Docker Images / Imágenes Docker:"
echo "     - Location: $BACKUP_DIR/docker/"
echo "     - Version: $VERSION"
echo "     - Retention: Last 10 images"
echo ""

# Log backup completion
echo "$(date): Automated backup completed successfully" >> "$BACKUP_DIR/backup.log"

exit 0
