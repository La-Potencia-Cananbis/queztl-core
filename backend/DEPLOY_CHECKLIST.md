# 🚀 Deployment Checklist

## Phase 1: Deploy Master (YOUR Domain)

```bash
# Set YOUR server IP/domain
export YOUR_MASTER_IP="192.168.1.100"  # or api.yourdomain.com

# Run deployment
./deploy-distributed.sh
```

**Verify:**
```bash
curl http://$YOUR_MASTER_IP:8000/api/health
curl http://$YOUR_MASTER_IP:8000/api/v1.2/network/status
```

---

## Phase 2: Setup RGIS Data Server

```bash
# Copy to RGIS
scp rgis_data_server.py root@rgis.com:/opt/quetzalcore/

# On RGIS.com:
ssh root@rgis.com
mkdir -p /data/surveys /data/results

# Copy your MAG surveys
cp ~/surveys/*.csv /data/surveys/

# Start server
python3 /opt/quetzalcore/rgis_data_server.py &

# Or with systemd (recommended)
# See RGIS_DATA_SYNC_GUIDE.md for systemd setup
```

**Verify:**
```bash
curl http://rgis.com:8000/health
curl http://rgis.com:8000/api/surveys/list
```

---

## Phase 3: Connect RGIS Training Workers

```bash
# Set worker IPs
export RGIS_TRAINING_NODES="10.0.0.10,10.0.0.11,10.0.0.12"

# Workers auto-deploy with ./deploy-distributed.sh
# Or manually on each RGIS worker:
scp /tmp/quetzalcore-deploy.tar.gz root@WORKER_IP:/tmp/
ssh root@WORKER_IP
cd /tmp && tar xzf quetzalcore-deploy.tar.gz
./quetzalcore-deploy/install-worker.sh http://YOUR_MASTER_IP:8000
```

**Verify:**
```bash
curl http://YOUR_MASTER_IP:8000/api/v1.2/network/status | jq '.registry.total_nodes'
# Should show > 1 (master + workers)
```

---

## Phase 4: Sync Data & Test

```bash
# Sync all surveys from RGIS
python3 sync_rgis_data.py \
  --rgis-url http://rgis.com:8000 \
  --master-url http://YOUR_MASTER_IP:8000

# Test mining API
curl -X POST http://YOUR_MASTER_IP:8000/api/mining/discriminate \
  -H "Content-Type: application/json" \
  -d '{"magnetic_data": [150, 890, 450], "locations": [[138.6, -30.5, 250]]}'
```

---

## ✅ Success Criteria

- [ ] Master API responding on YOUR domain
- [ ] Network status shows 1+ worker nodes
- [ ] RGIS data server lists surveys
- [ ] Data sync completes successfully
- [ ] Mining APIs return drill targets
- [ ] Training workers processing tasks

---

## Quick Commands Reference

```bash
# Check master status
ssh root@YOUR_SERVER systemctl status quetzalcore-master

# Check worker status
ssh root@RGIS_WORKER systemctl status quetzalcore-worker

# Check data server
ssh root@rgis.com ps aux | grep rgis_data_server

# View logs
ssh root@YOUR_SERVER journalctl -u quetzalcore-master -f

# Network status
curl http://YOUR_MASTER_IP:8000/api/v1.2/network/status | jq

# List surveys on RGIS
curl http://rgis.com:8000/api/surveys/list | jq

# Test sync
python3 sync_rgis_data.py --rgis-url http://rgis.com:8000 --master-url http://YOUR_MASTER_IP:8000
```

---

## Troubleshooting

**Master won't start:**
```bash
journalctl -u quetzalcore-master -xe
lsof -i:8000
```

**Workers not connecting:**
```bash
# On worker:
journalctl -u quetzalcore-worker -xe
curl http://YOUR_MASTER_IP:8000/api/health
```

**Data sync fails:**
```bash
curl http://rgis.com:8000/health
curl http://rgis.com:8000/api/surveys/list
```

---

**Ready to deploy? Run:**
```bash
export YOUR_MASTER_IP="your.server.ip"
export RGIS_TRAINING_NODES="worker1,worker2,worker3"
./deploy-distributed.sh
```
