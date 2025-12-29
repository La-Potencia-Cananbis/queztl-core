# 🌐 Complete Distributed Setup - RGIS + Your Domain

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ YOUR DOMAIN (api.yourdomain.com)                            │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ MASTER COORDINATOR (Port 8000)                          │ │
│ │ - Mining/GIS Processing APIs                            │ │
│ │ - Distributed Task Scheduler                            │ │
│ │ - Client-Facing Endpoints                               │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                          ↓ ↑
          ┌───────────────┴───────────────┐
          ↓ pulls data                    ↑ sends results
┌─────────────────────────────────────────────────────────────┐
│ RGIS.COM (Training + Data Infrastructure)                   │
│ ┌──────────────────────┐ ┌─────────────────────────────────┐ │
│ │ DATA SERVER          │ │ WORKER NODES (Training)         │ │
│ │ Port 8000            │ │ ┌──────┐ ┌──────┐ ┌──────┐    │ │
│ │ - Survey Files       │ │ │ GPU  │ │ GPU  │ │ CPU  │    │ │
│ │ - Results Storage    │ │ │ Node │ │ Node │ │ Node │    │ │
│ │ /data/surveys/*.csv  │ │ └──────┘ └──────┘ └──────┘    │ │
│ └──────────────────────┘ └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Deploy YOUR Master Coordinator

```bash
# Set configuration
export YOUR_MASTER_IP="api.yourdomain.com"  # Your production server

# Deploy
./deploy-distributed.sh
```

Your master will be running at: `http://api.yourdomain.com:8000`

### 2. Setup RGIS Data Server

On **RGIS.com** (data storage node):

```bash
# Copy files to RGIS
scp rgis_data_server.py root@rgis.com:/opt/quetzalcore/

# Setup data directories on RGIS
ssh root@rgis.com
mkdir -p /data/surveys /data/results

# Put your MAG survey files in /data/surveys/
cp ~/mining_project/*.csv /data/surveys/

# Start data server
cd /opt/quetzalcore
python3 rgis_data_server.py &

# Or use systemd
cat > /etc/systemd/system/rgis-data-server.service << 'EOF'
[Unit]
Description=RGIS Survey Data Server
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/quetzalcore
Environment="SURVEY_DATA_DIR=/data/surveys"
Environment="RESULTS_DIR=/data/results"
ExecStart=/usr/bin/python3 /opt/quetzalcore/rgis_data_server.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable rgis-data-server
systemctl start rgis-data-server
```

### 3. Deploy RGIS Training Workers

Still on **RGIS.com** (compute nodes):

```bash
# For each GPU/CPU training node on RGIS
export RGIS_TRAINING_NODES="10.0.0.10,10.0.0.11,10.0.0.12"

# Deploy workers (from deployment script)
# Workers will register with YOUR master at api.yourdomain.com:8000
```

### 4. Sync Data from RGIS to YOUR Domain

On **YOUR master** or from anywhere:

```bash
# Sync all surveys from RGIS
python3 sync_rgis_data.py \
  --rgis-url http://rgis.com:8000 \
  --master-url http://api.yourdomain.com:8000

# Or sync specific survey
python3 sync_rgis_data.py \
  --rgis-url http://rgis.com:8000 \
  --master-url http://api.yourdomain.com:8000 \
  --survey-id abc123 \
  --survey-name my_survey.csv
```

This will:
1. 📥 Download survey from RGIS
2. ⚙️  Process on YOUR master using distributed workers
3. 📤 Upload results back to RGIS
4. 💾 Save locally on YOUR domain

## Data Flow

### Workflow 1: Process RGIS Data on YOUR Domain

```bash
# 1. List available surveys on RGIS
curl http://rgis.com:8000/api/surveys/list

# 2. Sync and process
python3 sync_rgis_data.py \
  --rgis-url http://rgis.com:8000 \
  --master-url http://api.yourdomain.com:8000
  
# 3. Results are:
#    - Stored on YOUR domain (/opt/quetzalcore/data/)
#    - Sent back to RGIS (/data/results/)
#    - Available via API (YOUR domain)
```

### Workflow 2: Direct Upload to YOUR Domain

```bash
# Upload MAG survey directly to YOUR master
curl -X POST http://api.yourdomain.com:8000/api/mining/mag-survey \
  -F "file=@survey.csv" \
  -F "file_format=csv"
```

### Workflow 3: Training Jobs on RGIS Workers

```bash
# Submit AI training job (uses RGIS GPU nodes)
curl -X POST http://api.yourdomain.com:8000/api/v1.2/workload/submit \
  -H "Content-Type: application/json" \
  -d '{
    "workload_type": "neural_training",
    "payload": {
      "model": "mineral_discriminator",
      "dataset": "mag_surveys",
      "epochs": 100
    },
    "priority": 8
  }'
```

## File Organization

### On YOUR Domain (api.yourdomain.com)

```
/opt/quetzalcore/
├── backend/              # Mining APIs + Distributed coordinator
├── data/                 # Synced survey data
│   ├── survey1.csv
│   ├── survey2.xyz
│   └── abc123_summary.json
└── venv/                 # Python environment
```

### On RGIS.com (Data Server)

```
/data/
├── surveys/              # Original MAG survey files
│   ├── project1/
│   │   ├── mag_survey_001.csv
│   │   └── mag_survey_002.csv
│   └── project2/
│       └── lidar_mag_combined.xyz
└── results/              # Processing results from YOUR master
    ├── abc123_results.json
    └── def456_results.json
```

### On RGIS.com (Worker Nodes)

```
/opt/quetzalcore/
├── backend/              # Minimal backend for distributed tasks
├── register_rgis_worker.py
└── venv/
```

## Monitoring

### Check Network Status

```bash
# See all connected nodes (master + RGIS workers)
curl http://api.yourdomain.com:8000/api/v1.2/network/status | jq

# Should show:
# - 1 master node (YOUR domain)
# - N worker nodes (RGIS.com)
```

### Check Available Surveys on RGIS

```bash
curl http://rgis.com:8000/api/surveys/list | jq
```

### Check Processing Results

```bash
# On YOUR domain
ls -lh /opt/quetzalcore/data/

# On RGIS
ssh root@rgis.com ls -lh /data/results/
```

## Security Considerations

### Firewall Rules

**YOUR Master (api.yourdomain.com):**
```bash
# Allow clients to access APIs
ufw allow 8000/tcp

# Allow RGIS workers to register
ufw allow from RGIS_IP_RANGE to any port 8000
```

**RGIS Data Server:**
```bash
# Allow YOUR master to pull data
ufw allow from YOUR_MASTER_IP to any port 8000
```

**RGIS Workers:**
```bash
# Allow YOUR master to send tasks
ufw allow from YOUR_MASTER_IP to any port 8001
```

### Authentication (Optional)

Add API key authentication:

```bash
# Set API key on YOUR master
export QUETZALCORE_API_KEY="your-secret-key"

# Use in requests
curl -H "X-API-Key: your-secret-key" \
  http://api.yourdomain.com:8000/api/mining/mag-survey
```

## Troubleshooting

### RGIS workers not connecting

```bash
# On RGIS worker, check logs
journalctl -u quetzalcore-worker -f

# Test connectivity
curl http://api.yourdomain.com:8000/api/health
```

### Data sync failing

```bash
# Check RGIS data server
curl http://rgis.com:8000/health

# Check surveys available
curl http://rgis.com:8000/api/surveys/list

# Test download manually
curl http://rgis.com:8000/api/surveys/download/SURVEY_ID -o test.csv
```

### No training workers available

```bash
# Check network status
curl http://api.yourdomain.com:8000/api/v1.2/network/status | jq '.registry'

# Should show:
# - total_nodes > 1
# - worker_gpu or worker_cpu > 0
```

## Complete Example

```bash
# 1. Deploy everything
export YOUR_MASTER_IP="api.yourdomain.com"
export RGIS_TRAINING_NODES="10.0.0.10,10.0.0.11"
./deploy-distributed.sh

# 2. Setup RGIS data server
scp rgis_data_server.py root@rgis.com:/opt/
ssh root@rgis.com "python3 /opt/rgis_data_server.py &"

# 3. Put survey data on RGIS
scp *.csv root@rgis.com:/data/surveys/

# 4. Sync and process
python3 sync_rgis_data.py \
  --rgis-url http://rgis.com:8000 \
  --master-url http://api.yourdomain.com:8000

# 5. Get drill targets
curl http://api.yourdomain.com:8000/api/v1.2/network/status | jq
```

**✅ You now have:**
- Mining APIs on YOUR domain
- Training compute on RGIS
- Data storage on RGIS
- Automatic sync between them

**¡Listo para producción!** 🚀
