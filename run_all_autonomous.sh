#!/bin/bash
# Master automation script for Queztl-Core cloud deployment
# Uses project venv Python for all steps

set -e

PYTHON="/Users/xavasena/hive/backup_before_rename_20251207_171939/backup_before_rename_20251207_171939/backup_before_rename_20251207_171939/.venv/bin/python"


# Progress bar function
progress_bar() {
	local progress=$1
	local total=$2
	local message=$3
	local percent=$(( 100 * progress / total ))
	local bar_length=30
	local filled=$(( bar_length * progress / total ))
	local empty=$(( bar_length - filled ))
	printf "\r["
	for ((i=0; i<filled; i++)); do printf "#"; done
	for ((i=0; i<empty; i++)); do printf "-"; done
	printf "] %3d%% %s" "$percent" "$message"
	if [ "$progress" -eq "$total" ]; then printf "\n"; fi
}

step=1; total=4
progress_bar $step $total "Running deep code and config audit..."
$PYTHON audit_and_reorganize.py
((step++))
progress_bar $step $total "Running automated tests and deploy verification..."
$PYTHON test-api-routes.py
$PYTHON test-gis-quick.py
((step++))
progress_bar $step $total "Refactoring GUIs and APIs for production..."
$PYTHON infrastructure_monitor.py
$PYTHON infrastructure_monitor_web.py
((step++))
progress_bar $step $total "Deploying to cloud and scaling agents..."
docker compose -f docker-compose.hive.yml up -d --scale agent=50 dashboard
((step++))
progress_bar $step $total "All checks and productionization steps finished."
echo "\nDeployment complete."
echo "Access FastAPI docs at: http://localhost:8000/docs"
echo "Access dashboard at: http://localhost:3000"
