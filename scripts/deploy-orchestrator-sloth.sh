#!/bin/bash
# Deploy Orchestrator to Sloth (slow memory host)

echo "🧠 Deploying Orchestrator to Sloth (192.168.1.102)..."

# Copy orchestrator
scp backend/orchestrator.py xava@192.168.1.102:~/queztl-core/backend/

# Setup and start
ssh xava@192.168.1.102 << 'ENDSSH'
cd ~/queztl-core
mkdir -p logs data inbox

# Start orchestrator in background
nohup python3 backend/orchestrator.py > logs/orchestrator.log 2>&1 &

echo "✓ Orchestrator started on Sloth"
echo "  Log: ~/queztl-core/logs/orchestrator.log"
echo "  Neural signals: ~/queztl-core/logs/neural_sloth.log"
ENDSSH

echo "✓ Deployment complete"
