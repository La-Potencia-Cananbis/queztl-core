# Versioning & Rollback Strategy
# Estrategia de Versionado y Reversión

**Copyright (c) 2025 Queztl-Core Project - All Rights Reserved**

---

## 📋 Table of Contents / Tabla de Contenidos

1. [Semantic Versioning](#semantic-versioning)
2. [Version Numbering](#version-numbering)
3. [Rollback Strategy](#rollback-strategy)
4. [Patch Management](#patch-management)
5. [Backup Procedures](#backup-procedures)
6. [Emergency Procedures](#emergency-procedures)

---

## 🔢 Semantic Versioning

We follow [Semantic Versioning 2.0.0](https://semver.org/):

**Format**: `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

### Version Components / Componentes Versión

```
1.2.3-beta.1+20251204
│ │ │  │     │   └─ Build metadata (YYYYMMDD)
│ │ │  │     └───── Build number
│ │ │  └─────────── Pre-release identifier
│ │ └────────────── PATCH: Bug fixes (backward compatible)
│ └──────────────── MINOR: New features (backward compatible)
└────────────────── MAJOR: Breaking changes
```

### MAJOR Version (X.0.0)
**EN**: Increment when you make incompatible API changes

**ES**: Incrementar cuando haces cambios incompatibles en API

**Examples / Ejemplos**:
- API endpoint URL structure changes
- Database schema breaking changes
- Removal of deprecated features
- Major architectural changes

### MINOR Version (0.X.0)
**EN**: Increment when you add functionality in a backward-compatible manner

**ES**: Incrementar cuando agregas funcionalidad de manera compatible

**Examples / Ejemplos**:
- New API endpoints
- New features that don't break existing code
- Performance improvements
- New language support

### PATCH Version (0.0.X)
**EN**: Increment when you make backward-compatible bug fixes

**ES**: Incrementar cuando haces correcciones de errores compatibles

**Examples / Ejemplos**:
- Bug fixes
- Security patches
- Documentation updates
- Minor performance tweaks

---

## 📦 Version Numbering

### Current Version: 1.0.0 (2025-12-04)

### Version History / Historial Versiones

```
v1.0.0 (2025-12-04) - Initial Release with IP Protection
├── 10 patent claims
├── Bilingual support (EN/ES)
├── Web GPU driver (600+ lines)
├── Software GPU (8,192 threads)
└── Complete documentation

v0.9.0 (2025-11-20) - Beta Release
├── FastAPI migration
├── Basic GPU simulation
└── Training engine

v0.5.0 (2025-11-01) - Alpha Release
└── Proof of concept
```

---

## 🔄 Rollback Strategy

### Types of Rollbacks / Tipos de Reversión

#### 1. Code Rollback / Reversión de Código
**EN**: Revert to a previous Git commit  
**ES**: Revertir a un commit Git anterior

```bash
# View commit history
git log --oneline --graph --all

# Rollback to specific commit
git checkout <commit-hash>

# Create rollback branch
git checkout -b rollback-v1.0.0

# Rollback and force push (DANGEROUS - use with caution)
git reset --hard <commit-hash>
git push origin main --force
```

#### 2. Database Rollback / Reversión de Base de Datos
**EN**: Restore database from backup  
**ES**: Restaurar base de datos desde respaldo

```bash
# List available backups
ls -lh backups/database/

# Restore from backup
docker-compose down
docker-compose run --rm postgres \
  psql -U queztl -d queztl_db < backups/database/backup-20251204.sql
docker-compose up -d
```

#### 3. Docker Rollback / Reversión de Docker
**EN**: Revert to previous Docker image  
**ES**: Revertir a imagen Docker anterior

```bash
# List Docker images
docker images queztl-core

# Tag current as backup
docker tag queztl-core:latest queztl-core:backup-20251204

# Pull previous version
docker pull queztl-core:v0.9.0

# Restart with previous version
docker-compose down
docker-compose up -d
```

#### 4. Configuration Rollback / Reversión de Configuración
**EN**: Restore configuration files  
**ES**: Restaurar archivos configuración

```bash
# Backup current config
cp .env .env.backup-$(date +%Y%m%d)
cp docker-compose.yml docker-compose.yml.backup-$(date +%Y%m%d)

# Restore previous config
cp backups/config/.env-20251201 .env
cp backups/config/docker-compose.yml-20251201 docker-compose.yml

# Restart services
docker-compose down
docker-compose up -d
```

---

## 🩹 Patch Management

### Patch Types / Tipos de Parches

#### Security Patches / Parches de Seguridad
**Priority**: CRITICAL  
**Response Time**: Within 24 hours

```bash
# Create security patch branch
git checkout -b security-patch-CVE-2025-XXXX

# Apply security fix
# ... make changes ...

# Test thoroughly
./test-webgpu.sh
docker-compose run backend pytest

# Commit and deploy
git commit -m "security: Fix CVE-2025-XXXX vulnerability"
git tag v1.0.1-security
git push origin v1.0.1-security
```

#### Bug Fix Patches / Parches Corrección Errores
**Priority**: HIGH  
**Response Time**: Within 1 week

```bash
# Create bug fix branch
git checkout -b bugfix-issue-123

# Apply fix
# ... make changes ...

# Test
./test-webgpu.sh

# Commit
git commit -m "fix: Resolve rendering issue #123"
git tag v1.0.1
git push origin v1.0.1
```

#### Performance Patches / Parches Rendimiento
**Priority**: MEDIUM  
**Response Time**: Within 2 weeks

```bash
# Create performance branch
git checkout -b perf-optimize-gpu-threads

# Apply optimization
# ... make changes ...

# Benchmark before/after
curl -X POST http://localhost:8000/api/gpu/benchmark/compute

# Commit
git commit -m "perf: Optimize thread scheduling for 10% speedup"
git tag v1.0.1
```

---

## 💾 Backup Procedures

### Automated Backups / Respaldos Automatizados

#### Daily Database Backup / Respaldo Diario Base de Datos
```bash
#!/bin/bash
# backup-database.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/database"
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker-compose exec -T postgres pg_dump -U queztl queztl_db \
  > $BACKUP_DIR/backup-$DATE.sql

# Compress
gzip $BACKUP_DIR/backup-$DATE.sql

# Keep only last 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Database backup completed: backup-$DATE.sql.gz"
```

#### Weekly Code Backup / Respaldo Semanal Código
```bash
#!/bin/bash
# backup-code.sh

DATE=$(date +%Y%m%d)
BACKUP_DIR="backups/code"
mkdir -p $BACKUP_DIR

# Create code archive (excluding node_modules, __pycache__, etc.)
tar -czf $BACKUP_DIR/code-$DATE.tar.gz \
  --exclude='node_modules' \
  --exclude='__pycache__' \
  --exclude='.git' \
  --exclude='*.pyc' \
  .

# Keep only last 12 weeks
find $BACKUP_DIR -name "*.tar.gz" -mtime +84 -delete

echo "Code backup completed: code-$DATE.tar.gz"
```

#### Configuration Backup / Respaldo Configuración
```bash
#!/bin/bash
# backup-config.sh

DATE=$(date +%Y%m%d)
BACKUP_DIR="backups/config"
mkdir -p $BACKUP_DIR

# Backup important config files
cp .env $BACKUP_DIR/.env-$DATE
cp docker-compose.yml $BACKUP_DIR/docker-compose.yml-$DATE
cp backend/requirements.txt $BACKUP_DIR/requirements.txt-$DATE
cp dashboard/package.json $BACKUP_DIR/package.json-$DATE

echo "Config backup completed: $DATE"
```

### Backup Schedule / Calendario Respaldos

| Type / Tipo | Frequency / Frecuencia | Retention / Retención |
|-------------|------------------------|------------------------|
| Database | Daily / Diario | 30 days / días |
| Code | Weekly / Semanal | 12 weeks / semanas |
| Config | On change / Al cambiar | 90 days / días |
| Docker Images | On release / Al lanzar | 10 versions / versiones |

---

## 🚨 Emergency Procedures

### Complete System Rollback / Reversión Completa Sistema

#### EN: When to use
- Critical production bug
- Security vulnerability
- Data corruption
- System instability

#### ES: Cuándo usar
- Error crítico producción
- Vulnerabilidad seguridad
- Corrupción datos
- Inestabilidad sistema

#### Procedure / Procedimiento

```bash
#!/bin/bash
# emergency-rollback.sh
# CRITICAL: Only use in emergencies!
# CRÍTICO: ¡Solo usar en emergencias!

echo "🚨 EMERGENCY ROLLBACK INITIATED"
echo "🚨 REVERSIÓN DE EMERGENCIA INICIADA"

# 1. Stop all services / Detener todos servicios
echo "Stopping services / Deteniendo servicios..."
docker-compose down

# 2. Backup current state / Respaldar estado actual
echo "Backing up current state / Respaldando estado actual..."
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf emergency-backup-$DATE.tar.gz .env docker-compose.yml backend/ dashboard/

# 3. Restore database / Restaurar base de datos
echo "Restoring database / Restaurando base de datos..."
LATEST_DB_BACKUP=$(ls -t backups/database/*.sql.gz | head -1)
gunzip -c $LATEST_DB_BACKUP | \
  docker-compose run --rm postgres psql -U queztl -d queztl_db

# 4. Restore code / Restaurar código
echo "Restoring code / Restaurando código..."
git fetch --all
git checkout v0.9.0  # Last known good version

# 5. Restore config / Restaurar configuración
echo "Restoring config / Restaurando configuración..."
LATEST_CONFIG=$(ls -t backups/config/.env-* | head -1)
cp $LATEST_CONFIG .env

# 6. Restart services / Reiniciar servicios
echo "Restarting services / Reiniciando servicios..."
docker-compose up -d

# 7. Verify / Verificar
echo "Verifying system / Verificando sistema..."
sleep 10
curl -f http://localhost:8000/health || echo "❌ Health check failed!"
curl -f http://localhost:3000 || echo "❌ Dashboard check failed!"

echo "✅ Emergency rollback complete!"
echo "✅ ¡Reversión de emergencia completa!"
echo ""
echo "📋 Next steps / Próximos pasos:"
echo "1. Check logs: docker-compose logs"
echo "2. Verify functionality: ./test-webgpu.sh"
echo "3. Document issue: Create incident report"
echo "4. Plan fix: Schedule hotfix release"
```

### Incident Report Template / Plantilla Reporte Incidentes

```markdown
# Incident Report / Reporte de Incidente

**Date / Fecha**: YYYY-MM-DD HH:MM UTC
**Severity / Severidad**: Critical / High / Medium / Low
**Status / Estado**: Investigating / Resolved / Monitoring

## Summary / Resumen
<!-- Brief description in English and Spanish -->

## Timeline / Cronología
- **HH:MM** - Issue detected / Problema detectado
- **HH:MM** - Team notified / Equipo notificado
- **HH:MM** - Rollback initiated / Reversión iniciada
- **HH:MM** - System restored / Sistema restaurado
- **HH:MM** - Monitoring / Monitoreando

## Root Cause / Causa Raíz
<!-- What caused the issue -->

## Impact / Impacto
- Users affected / Usuarios afectados: X
- Downtime / Tiempo caído: X minutes
- Data loss / Pérdida datos: Yes/No

## Resolution / Resolución
<!-- What was done to fix it -->

## Prevention / Prevención
<!-- How to prevent this in the future -->

## Action Items / Items de Acción
- [ ] Fix underlying bug
- [ ] Update tests
- [ ] Improve monitoring
- [ ] Update documentation
```

---

## 🔍 Version Verification

### Check Current Version / Verificar Versión Actual

```bash
# Backend version
curl http://localhost:8000/api/version

# Git version
git describe --tags --always

# Docker image version
docker inspect queztl-core:latest | grep -i version

# Package versions
cat backend/requirements.txt | grep "^[a-z]"
cat dashboard/package.json | grep version
```

### Version Compatibility Matrix / Matriz Compatibilidad

| Component | v1.0.0 | v0.9.0 | v0.5.0 |
|-----------|--------|--------|--------|
| Python | 3.11+ | 3.10+ | 3.9+ |
| Node.js | 18+ | 16+ | 14+ |
| PostgreSQL | 15+ | 14+ | 13+ |
| Redis | 7+ | 6+ | 6+ |
| Docker | 24+ | 20+ | 20+ |

---

## 📝 Version Tagging Best Practices

### Git Tagging / Etiquetado Git

```bash
# Lightweight tag
git tag v1.0.0

# Annotated tag (RECOMMENDED)
git tag -a v1.0.0 -m "Release v1.0.0: Initial release with IP protection"

# Tag with date
git tag -a v1.0.0 -m "Release v1.0.0 ($(date +%Y-%m-%d))"

# Push tags
git push origin v1.0.0
git push origin --tags

# List tags
git tag -l
git tag -l "v1.*"

# View tag details
git show v1.0.0

# Delete tag (if needed)
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
```

### Docker Tagging / Etiquetado Docker

```bash
# Build with version tag
docker build -t queztl-core:v1.0.0 -t queztl-core:latest .

# Tag existing image
docker tag queztl-core:latest queztl-core:v1.0.0

# Push to registry
docker push queztl-core:v1.0.0
docker push queztl-core:latest

# Multi-architecture tags
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t queztl-core:v1.0.0 \
  --push .
```

---

## 🔐 Version Integrity

### Checksums / Sumas de Verificación

```bash
# Generate checksums for release
sha256sum backend/*.py > checksums-v1.0.0.txt
sha256sum dashboard/package.json >> checksums-v1.0.0.txt

# Verify integrity
sha256sum -c checksums-v1.0.0.txt
```

### GPG Signing / Firma GPG

```bash
# Sign release tag
git tag -s v1.0.0 -m "Release v1.0.0 (signed)"

# Verify signature
git tag -v v1.0.0

# Sign release archive
gpg --armor --detach-sign code-v1.0.0.tar.gz
```

---

## 📊 Monitoring Version Health

### Health Check Endpoints / Endpoints Verificación Salud

```bash
# System health
curl http://localhost:8000/health

# Version info
curl http://localhost:8000/api/version

# Component status
curl http://localhost:8000/api/status
```

### Expected Response / Respuesta Esperada

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "build": "20251204",
  "components": {
    "database": "ok",
    "redis": "ok",
    "gpu_simulator": "ok"
  },
  "performance": {
    "uptime": "24h 15m",
    "requests": 10523,
    "avg_response_time": "45ms"
  }
}
```

---

## 🎯 Release Checklist / Lista Verificación Lanzamiento

### Pre-Release / Pre-Lanzamiento

- [ ] All tests passing / Todas pruebas pasando
- [ ] Documentation updated / Documentación actualizada
- [ ] CHANGELOG.md updated / CHANGELOG.md actualizado
- [ ] Version numbers bumped / Números versión incrementados
- [ ] Database migrations tested / Migraciones BD probadas
- [ ] Backup created / Respaldo creado
- [ ] Security scan passed / Escaneo seguridad pasado
- [ ] Performance benchmarks run / Benchmarks rendimiento ejecutados

### Release / Lanzamiento

- [ ] Git tag created / Etiqueta Git creada
- [ ] Docker images built / Imágenes Docker construidas
- [ ] Docker images pushed / Imágenes Docker subidas
- [ ] Release notes published / Notas lanzamiento publicadas
- [ ] Team notified / Equipo notificado

### Post-Release / Post-Lanzamiento

- [ ] Deployment verified / Despliegue verificado
- [ ] Health checks passing / Verificaciones salud pasando
- [ ] Monitoring alerts configured / Alertas monitoreo configuradas
- [ ] Rollback plan tested / Plan reversión probado
- [ ] Incident report template ready / Plantilla reporte incidente lista

---

## 📞 Support / Soporte

### Version Support Policy / Política Soporte Versiones

| Version Type | Support Duration | Updates |
|--------------|------------------|---------|
| Current (1.x) | Ongoing | All updates |
| Previous (0.9.x) | 6 months | Security only |
| Legacy (0.5.x) | End of life | None |

### Getting Help / Obtener Ayuda

**EN**:
- Check CHANGELOG.md for version changes
- Review VERSIONING.md (this file) for procedures
- Contact: support@queztl-core.com (to be established)

**ES**:
- Consultar CHANGELOG.md para cambios versión
- Revisar VERSIONING.md (este archivo) para procedimientos
- Contacto: support@queztl-core.com (a establecer)

---

🔒 **CONFIDENTIAL - PATENT PENDING**  
🔒 **CONFIDENCIAL - PATENTE PENDIENTE**

**Copyright (c) 2025 Queztl-Core Project - All Rights Reserved**

**Last Updated / Última Actualización**: December 4, 2025  
**Version / Versión**: 1.0.0
