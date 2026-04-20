#!/bin/bash
# QUETZAL GIS Pro - Scheduled Cron Runner

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CRON_FILE="/tmp/quetzal_crons.txt"
RUNNER="$SCRIPT_DIR/runner.sh"
LOGFILE="$REPO_ROOT/cron.log"
FULL_BUILD="$REPO_ROOT/full-build.sh"
DEEP_ANALYSIS="$REPO_ROOT/deep-analysis.sh"

# Add to crontab with: crontab -e
# Then add these lines:
#
# # Run every hour
# 0 * * * * <repo>/backend/runner.sh
#
# # Run every 6 hours for full rebuild
# 0 */6 * * * <repo>/full-build.sh
#
# # Run daily at 2 AM for deep analysis
# 0 2 * * * <repo>/deep-analysis.sh

# Create cron jobs
cat > "$CRON_FILE" << EOF_CRON
# QUETZAL GIS Pro - Automated Runners
# Auto-generated on $(date)

# Hourly test suite
0 * * * * $RUNNER >> $LOGFILE 2>&1

# 6-hourly full rebuild with deployment
0 */6 * * * $FULL_BUILD >> $LOGFILE 2>&1

# Daily detailed analysis
0 2 * * * $DEEP_ANALYSIS >> $LOGFILE 2>&1
EOF_CRON

# Install cron jobs
echo "Installing cron jobs..."
crontab "$CRON_FILE"
echo "✅ Cron jobs installed"
echo "View with: crontab -l"
