#!/bin/bash
# Deploy Native Hypervisor to QuetzalCore Core Worker Nodes

set -e

echo "🦅 QUETZALCORE CORE - HYPERVISOR DEPLOYMENT"
echo "======================================"
echo ""

# Configuration
QUETZALCORE_MASTER="${QUETZALCORE_MASTER:-localhost:9000}"
WORKER_NODES="${WORKER_NODES:-worker1,worker2,worker3}"

echo "📋 Deployment Configuration:"
echo "  Master Node: $QUETZALCORE_MASTER"
echo "  Worker Nodes: $WORKER_NODES"
echo ""

# Package HV components
echo "📦 Packaging Hypervisor components..."
tar -czf quetzalcore-hv-package.tar.gz \
  backend/native_hypervisor.py \
  backend/gpu_simulator.py \
  backend/webgpu_driver.py \
  backend/distributed_network.py \
  requirements.txt

echo "✅ Package created: quetzalcore-hv-package.tar.gz"
echo ""

# Deploy to each worker node
IFS=',' read -ra WORKERS <<< "$WORKER_NODES"
for worker in "${WORKERS[@]}"; do
  echo "🚀 Deploying to worker: $worker"
  
  # Copy package
  scp quetzalcore-hv-package.tar.gz quetzalcore@${worker}:/tmp/
  
  # Install on worker
  ssh quetzalcore@${worker} << 'EOF'
    cd /opt/quetzalcore
    tar -xzf /tmp/quetzalcore-hv-package.tar.gz
    
    # Install dependencies
    pip3 install -r requirements.txt
    
    # Start Hypervisor service
    cat > /etc/systemd/system/quetzalcore-hv.service << 'SERVICE'
[Unit]
Description=QuetzalCore Native Hypervisor
After=network.target

[Service]
Type=simple
User=quetzalcore
WorkingDirectory=/opt/quetzalcore
ExecStart=/usr/bin/python3 -m backend.native_hypervisor
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE
    
    # Enable and start
    systemctl daemon-reload
    systemctl enable quetzalcore-hv
    systemctl restart quetzalcore-hv
    
    echo "✅ Hypervisor started on $(hostname)"
EOF
  
  echo ""
done

echo "🎉 Deployment complete!"
echo ""
echo "Verify with:"
echo "  ssh quetzalcore@worker1 'systemctl status quetzalcore-hv'"
echo ""
