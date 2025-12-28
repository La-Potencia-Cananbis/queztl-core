#!/bin/bash
# Master automation script for Queztl-Core cloud deployment
# Uses project venv Python for all steps

set -e

PYTHON="/Users/xavasena/hive/backup_before_rename_20251207_171939/backup_before_rename_20251207_171939/backup_before_rename_20251207_171939/.venv/bin/python"

# 1. Deep code and config audit
echo "[1/4] Running deep code and config audit..."
$PYTHON audit_and_reorganize.py

# 2. Automated test and deploy verification
echo "[2/4] Running automated tests and deploy verification..."
$PYTHON test-api-routes.py
$PYTHON test-gis-quick.py

# 3. Productionize GUIs and APIs
echo "[3/4] Refactoring GUIs and APIs for production..."
$PYTHON infrastructure_monitor.py
$PYTHON infrastructure_monitor_web.py

# 4. Deploy to cloud and scale agents
echo "[4/4] Deploying to cloud and scaling agents..."
docker compose -f docker-compose.hive.yml up -d --scale agent=50 dashboard

# Output approval summary
echo "Deployment complete. All checks and productionization steps finished."
echo "Access FastAPI docs at: http://localhost:8000/docs"
echo "Access dashboard at: http://localhost:3000"
