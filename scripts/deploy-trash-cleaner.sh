#!/bin/bash
# Deploy Trash Cleaner to Beast and Sloth
# Sets up automated cleanup routines

NODES=("192.168.1.105" "192.168.1.106")
NODE_NAMES=("beast" "sloth")
USER="xava"

echo "🗑️  TRASH CLEANER DEPLOYMENT"
echo "═══════════════════════════════════════════════════════════"

for i in "${!NODES[@]}"; do
    IP="${NODES[$i]}"
    NAME="${NODE_NAMES[$i]}"
    
    echo ""
    echo "📡 Deploying to $NAME ($IP)..."
    
    # Check if reachable
    if ! ping -c 1 -W 2 "$IP" > /dev/null 2>&1; then
        echo "❌ $NAME unreachable - skipping"
        continue
    fi
    
    # Copy script
    echo "  📤 Copying trash-cleaner.sh..."
    scp -q scripts/trash-cleaner.sh "$USER@$IP:/tmp/"
    
    # Install and setup
    ssh "$USER@$IP" bash << 'ENDSSH'
        echo "  🔧 Installing..."
        
        # Move script
        sudo mv /tmp/trash-cleaner.sh /usr/local/bin/
        sudo chmod +x /usr/local/bin/trash-cleaner.sh
        
        # Create log directory
        sudo mkdir -p /var/log
        sudo touch /var/log/queztl-trash-cleaner.log
        sudo chown $USER:$USER /var/log/queztl-trash-cleaner.log
        
        # Setup cron job (run every hour)
        CRON_JOB="0 * * * * /usr/local/bin/trash-cleaner.sh >> /var/log/queztl-trash-cleaner.log 2>&1"
        (crontab -l 2>/dev/null | grep -v trash-cleaner.sh; echo "$CRON_JOB") | crontab -
        
        echo "  ✅ Installed with hourly cron job"
        
        # Run once now
        echo "  🧹 Running initial cleanup..."
        /usr/local/bin/trash-cleaner.sh
ENDSSH
    
    echo "  ✅ $NAME configured"
done

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ Trash Cleaner deployed to all nodes"
echo ""
echo "📋 Status:"
echo "  • Runs hourly via cron"
echo "  • Logs: /var/log/queztl-trash-cleaner.log"
echo "  • Reports: ~/queztl-core/data/trash-cleaner-*.txt"
echo ""
echo "🔍 Manual run: ssh <node> /usr/local/bin/trash-cleaner.sh"
echo "📊 View logs: ssh <node> tail -f /var/log/queztl-trash-cleaner.log"
