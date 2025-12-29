# 🚀 QuetzalCore Distributed Deployment Guide

## Architecture

```
┌─────────────────────────────────────────────┐
│  YOUR DOMAIN (Production)                   │
│  ┌──────────────────────────────────────┐  │
│  │  MASTER COORDINATOR                   │  │
│  │  - Mining/GIS APIs                    │  │
│  │  - Geophysics Engine                  │  │
│  │  - Distributed Scheduler              │  │
│  │  Port: 8000                           │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                    ↓ registers + heartbeat
┌─────────────────────────────────────────────┐
│  RGIS.COM (Training Infrastructure)         │
│  ┌───────────┐ ┌───────────┐ ┌──────────┐  │
│  │ Worker 1  │ │ Worker 2  │ │ Worker N │  │
│  │ GPU/CPU   │ │ GPU/CPU   │ │ GPU/CPU  │  │
│  │ Training  │ │ Training  │ │ Training │  │
│  └───────────┘ └───────────┘ └──────────┘  │
└─────────────────────────────────────────────┘
```

## Quick Deploy

### 1. Set Your Configuration

```bash
# YOUR production domain/server
export YOUR_DOMAIN="api.yourdomain.com"
export YOUR_MASTER_IP="192.168.1.100"  # Or use domain

# RGIS.com training workers (optional)
export RGIS_TRAINING_NODES="10.0.0.10,10.0.0.11,10.0.0.12"

# SSH user (usually root)
export DEPLOY_USER="root"
```

### 2. Run Deployment

```bash
chmod +x deploy-distributed.sh
./deploy-distributed.sh
```

### 3. Verify Deployment

```bash
# Check master
curl http://$YOUR_MASTER_IP:8000/api/health

# Check network
curl http://$YOUR_MASTER_IP:8000/api/v1.2/network/status | jq
```

## Manual Deployment

### Deploy Master (YOUR domain)

```bash
# 1. Copy package to YOUR server
scp /tmp/quetzalcore-deploy.tar.gz root@YOUR_SERVER:/tmp/

# 2. Install on YOUR server
ssh root@YOUR_SERVER
cd /tmp && tar xzf quetzalcore-deploy.tar.gz
sudo bash /tmp/quetzalcore-deploy/install-master.sh
```

### Add Training Workers (RGIS.com)

```bash
# For each RGIS.com training node:

# 1. Copy package
scp /tmp/quetzalcore-deploy.tar.gz root@RGIS_WORKER:/tmp/

# 2. Install worker
ssh root@RGIS_WORKER
cd /tmp && tar xzf quetzalcore-deploy.tar.gz
sudo bash /tmp/quetzalcore-deploy/install-worker.sh http://YOUR_MASTER_IP:8000
```

## Management Commands

### Check Status

```bash
# Master status
ssh root@YOUR_SERVER systemctl status quetzalcore-master

# Worker status
ssh root@RGIS_WORKER systemctl status quetzalcore-worker

# Network status
curl http://YOUR_MASTER_IP:8000/api/v1.2/network/status
```

### View Logs

```bash
# Master logs
ssh root@YOUR_SERVER journalctl -u quetzalcore-master -f

# Worker logs
ssh root@RGIS_WORKER journalctl -u quetzalcore-worker -f
```

### Restart Services

```bash
# Restart master
ssh root@YOUR_SERVER systemctl restart quetzalcore-master

# Restart worker
ssh root@RGIS_WORKER systemctl restart quetzalcore-worker
```

## Using the APIs

### Mining APIs (from anywhere)

```bash
# Upload MAG survey
curl -X POST http://YOUR_MASTER_IP:8000/api/mining/mag-survey \
  -F "file=@survey.csv" \
  -F "file_format=csv"

# Get drill targets
curl -X POST http://YOUR_MASTER_IP:8000/api/mining/target-drills \
  -H "Content-Type: application/json" \
  -d '{
    "magnetic_data": [150, 890, 450],
    "locations": [[138.6, -30.5, 250], [138.7, -30.5, 245]],
    "top_n": 10
  }'

# Cost analysis
curl "http://YOUR_MASTER_IP:8000/api/mining/survey-cost?area_km2=10"
```

### Submit Training Job (uses RGIS workers)

```bash
curl -X POST http://YOUR_MASTER_IP:8000/api/v1.2/workload/submit \
  -H "Content-Type: application/json" \
  -d '{
    "workload_type": "neural_training",
    "payload": {
      "model": "mineral_discriminator",
      "epochs": 100
    },
    "priority": 8
  }'
```

## Firewall Rules

### On YOUR Master Server

```bash
# Allow API access (port 8000)
ufw allow 8000/tcp

# If using HTTPS (recommended for production)
ufw allow 443/tcp
```

### On RGIS Training Workers

```bash
# Allow master to connect
ufw allow from YOUR_MASTER_IP to any port 8001

# Or open to all (for development)
ufw allow 8001/tcp
```

## Production Setup (Optional)

### Add HTTPS with Nginx

```bash
# On YOUR master server
apt-get install nginx certbot python3-certbot-nginx

# Configure Nginx
cat > /etc/nginx/sites-available/quetzalcore << 'EOF'
server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

ln -s /etc/nginx/sites-available/quetzalcore /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# Get SSL certificate
certbot --nginx -d api.yourdomain.com
```

### Add Monitoring

```bash
# Install monitoring script on master
cat > /opt/quetzalcore/monitor.sh << 'EOF'
#!/bin/bash
while true; do
    curl -s http://localhost:8000/api/v1.2/network/status | \
        jq '.registry | "Nodes: \(.total_nodes), Online: \(.online_nodes), Tasks: \(.total_tasks)"'
    sleep 30
done
EOF

chmod +x /opt/quetzalcore/monitor.sh
```

## Troubleshooting

### Master won't start

```bash
# Check logs
journalctl -u quetzalcore-master -xe

# Common issues:
# - Port 8000 already in use: lsof -i:8000
# - Python deps missing: /opt/quetzalcore/venv/bin/pip install -r /opt/quetzalcore/requirements.txt
# - Permission issues: chown -R quetzalcore:quetzalcore /opt/quetzalcore
```

### Worker can't connect

```bash
# Check worker logs
journalctl -u quetzalcore-worker -xe

# Test connectivity
curl http://YOUR_MASTER_IP:8000/api/health

# Check firewall
ufw status
```

### No training workers showing up

```bash
# Check network status
curl http://YOUR_MASTER_IP:8000/api/v1.2/network/status | jq

# Manually test worker registration
ssh root@RGIS_WORKER
/opt/quetzalcore/venv/bin/python /opt/quetzalcore/register_rgis_worker.py http://YOUR_MASTER_IP:8000
```

## Architecture Benefits

✅ **YOUR Domain = Production APIs**
- Mining/GIS services always available
- Client-facing endpoints on YOUR infrastructure
- Full control over production

✅ **RGIS.com = Training Power**
- Heavy AI/ML training offloaded to RGIS
- Scale training workers up/down
- Keep YOUR domain responsive

✅ **Distributed Architecture**
- Master coordinates all work
- Workers auto-register and heartbeat
- Failed workers automatically removed
- Load balancing across workers

## Next Steps

1. Deploy master to YOUR domain ✅
2. Connect RGIS training workers
3. Test mining APIs
4. Scale training workers as needed
5. Add HTTPS for production
6. Set up monitoring

**¡Listo! Your mining/GIS system runs on YOUR domain, powered by RGIS training!**
