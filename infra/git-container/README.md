# 🦅 Queztl-Core Git Container

Self-hosted Git server with automation, webhooks, and cluster integration.

## Features

- 🐙 **Gitea** - Lightweight Git server with web UI
- 🤖 **Automation** - Auto-build on push, PR checks
- 🪝 **Webhooks** - Integrate with Beast/Sloth cluster
- 🐘 **PostgreSQL** - Reliable database backend
- 🔴 **Redis** - Job queue for builds
- ☁️  **Cloud-ready** - Deploy to AWS/Azure/GCP
- 💾 **Backups** - Automated repository backups
- 🔒 **Secure** - SSH + HTTPS support

## Quick Start

```bash
cd infra/git-container
./scripts/setup-git-server.sh
```

Access: http://localhost:3000

## Architecture

```
┌─────────────────────────────────────────┐
│  Gitea Web UI (Port 3000)               │
│  - Repository management                │
│  - Pull requests, issues                │
│  - User management                      │
└─────────┬───────────────────────────────┘
          │
          ├─→ PostgreSQL (Database)
          ├─→ Redis (Job Queue)
          └─→ Git Automation Runner
                    │
                    ├─→ Beast (192.168.1.105) - Builds
                    ├─→ Sloth (192.168.1.102) - Orchestrator
                    └─→ Command Center - Monitoring
```

## Configuration

### Environment Variables

```bash
# Gitea
GITEA_URL=http://gitea:3000
GITEA_TOKEN=your_gitea_access_token

# Cluster
BEAST_URL=http://192.168.1.105:8001
SLOTH_URL=http://192.168.1.102:9000

# Database
POSTGRES_USER=gitea
POSTGRES_PASSWORD=gitea
POSTGRES_DB=gitea
```

### Generate Access Token

1. Open http://localhost:3000
2. Login as admin
3. Settings → Applications → Generate Token
4. Copy token and set environment variable:
   ```bash
   export GITEA_TOKEN=your_token_here
   docker-compose restart git-automation
   ```

## Automation Features

### Automatic Builds

When you push to any repository:

1. **Webhook triggered** - Git server sends event
2. **Commit analyzed** - Automation checks what changed
3. **Build queued** - Job added to Redis queue
4. **Cluster notified** - Orchestrator on Sloth receives task
5. **Build executed** - Beast runs tests/builds
6. **Results reported** - Status updated in Gitea

### Triggers

- `backend/` changes → Run tests, restart API
- `frontend/` changes → Build frontend
- `Dockerfile` changes → Rebuild containers
- `infra/` changes → Update infrastructure
- Pull requests → Run checks

## Cloud Deployment

### AWS (ECS)

```bash
export AWS_REGION=us-east-1
./scripts/deploy-to-cloud.sh aws
```

### Azure (ACI)

```bash
export ACR_NAME=myregistry
./scripts/deploy-to-cloud.sh azure
```

### GCP (Cloud Run)

```bash
export GCP_PROJECT=my-project
./scripts/deploy-to-cloud.sh gcp
```

### Docker Hub

```bash
export DOCKER_USERNAME=myusername
./scripts/deploy-to-cloud.sh docker-hub
```

## Backup & Restore

### Manual Backup

```bash
./scripts/backup-repos.sh
```

Backup location: `./backups/YYYYMMDD_HHMMSS/`

### Automated Backup

Automation runner backs up all repos every 6 hours.

### Restore from Backup

```bash
# Stop services
docker-compose stop

# Restore data
tar xzf backups/20260119_120000/data.tar.gz -C ./

# Restore database
docker exec -i queztl-git-db psql -U gitea gitea < backups/20260119_120000/database.sql

# Restart
docker-compose start
```

## Integration with Cluster

### Webhook Endpoint on Sloth

The orchestrator on Sloth should expose `/git-webhook`:

```python
@app.post("/git-webhook")
async def git_webhook(request: Request):
    data = await request.json()
    # Process webhook
    return {"status": "received"}
```

### Build Queue

Automation pushes build jobs to Redis:

```json
{
  "id": "build_1234567890",
  "type": "git_build",
  "repo": "queztl-core",
  "branch": "main",
  "commit": "abc123def456",
  "timestamp": "2026-01-19T12:00:00Z",
  "status": "queued"
}
```

## Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f git-automation

# Automation logs
tail -f logs/git_automation_*.log
```

### Check Status

```bash
# Container status
docker-compose ps

# Gitea health
curl http://localhost:3000/api/healthz

# Build queue
docker exec queztl-git-redis redis-cli LLEN build_queue
```

## Useful Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose stop

# Restart automation
docker-compose restart git-automation

# View logs
docker-compose logs -f

# Backup repos
./scripts/backup-repos.sh

# Deploy to cloud
./scripts/deploy-to-cloud.sh [aws|azure|gcp]

# SSH to Gitea container
docker exec -it queztl-git sh

# Access Redis CLI
docker exec -it queztl-git-redis redis-cli
```

## Ports

- **3000** - Gitea web UI (HTTP)
- **2222** - Gitea SSH (Git operations)
- **5432** - PostgreSQL (internal)
- **6379** - Redis (internal)

## Repository URLs

### HTTP Clone

```bash
git clone http://localhost:3000/username/repo.git
```

### SSH Clone

```bash
git clone ssh://git@localhost:2222/username/repo.git
```

## Troubleshooting

### Gitea not starting

```bash
docker-compose logs gitea
```

Check database connection and permissions.

### Webhooks not firing

1. Check Gitea webhook settings
2. Verify automation container is running: `docker-compose ps`
3. Check automation logs: `docker-compose logs git-automation`
4. Test webhook manually:
   ```bash
   curl -X POST http://localhost:3000/api/v1/repos/user/repo/hooks/test \
     -H "Authorization: token YOUR_TOKEN"
   ```

### Build queue stuck

```bash
# Check queue length
docker exec queztl-git-redis redis-cli LLEN build_queue

# Clear queue
docker exec queztl-git-redis redis-cli DEL build_queue
```

## Security

### Change Default Passwords

Edit `docker-compose.yml`:

```yaml
environment:
  - POSTGRES_PASSWORD=your_secure_password
```

### Enable HTTPS

1. Get SSL certificate (Let's Encrypt)
2. Update docker-compose.yml:
   ```yaml
   environment:
     - GITEA__server__PROTOCOL=https
     - GITEA__server__CERT_FILE=/data/cert.pem
     - GITEA__server__KEY_FILE=/data/key.pem
   ```

### SSH Key Setup

```bash
# Generate key
ssh-keygen -t ed25519 -C "git@queztl"

# Add to Gitea
# Settings → SSH Keys → Add Key
```

## Migration from GitHub

```bash
# In Gitea UI:
# + → New Migration → GitHub
# Enter repo URL and credentials
```

Or use CLI:

```bash
docker exec -it queztl-git gitea admin repo migrate \
  --source https://github.com/user/repo \
  --owner username
```

## Advanced Features

### Git LFS

Enabled by default. Usage:

```bash
git lfs install
git lfs track "*.psd"
git add .gitattributes
```

### Actions (CI/CD)

Enable in `docker-compose.yml`:

```yaml
environment:
  - GITEA__actions__ENABLED=true
```

Create `.gitea/workflows/build.yaml`:

```yaml
name: Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: make build
```

## Contributing

This is part of Queztl-Core. See main repo for contribution guidelines.

## License

Part of Queztl-Core project.

---

**Ready to pass to GPT Copilot for additional help! 🚀**
