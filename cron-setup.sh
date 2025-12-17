#!/bin/bash
# QUETZAL GIS Pro - Scheduled Cron Runner
# Add to crontab with: crontab -e
# Then add these lines:
#
# # Run every hour
# 0 * * * * /Users/xavasena/hive/runner.sh
#
# # Run every 6 hours for full rebuild
# 0 */6 * * * /Users/xavasena/hive/full-build.sh
#
# # Run daily at 2 AM for deep analysis
# 0 2 * * * /Users/xavasena/hive/deep-analysis.sh
#

# To install:
# chmod +x /Users/xavasena/hive/cron-setup.sh
# bash /Users/xavasena/hive/cron-setup.sh

CRON_FILE="/tmp/quetzal_crons.txt"
RUNNER="/Users/xavasena/hive/runner.sh"
LOGFILE="/Users/xavasena/hive/cron.log"

# Create cron jobs
cat > "$CRON_FILE" << EOF
# QUETZAL GIS Pro - Automated Runners
# Auto-generated on $(date)

# Hourly test suite
0 * * * * $RUNNER >> $LOGFILE 2>&1

# 6-hourly full rebuild with deployment
0 */6 * * * /Users/xavasena/hive/full-build.sh >> $LOGFILE 2>&1

# Daily detailed analysis
0 2 * * * /Users/xavasena/hive/deep-analysis.sh >> $LOGFILE 2>&1
EOF

# Install cron jobs
echo "Installing cron jobs..."
crontab "$CRON_FILE"
echo "✅ Cron jobs installed"
echo "View with: crontab -l"
