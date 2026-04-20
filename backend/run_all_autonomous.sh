#!/bin/bash
# Master automation script for Queztl-Core cloud deployment
# Uses project venv Python for all steps (fallback to python3)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_PYTHON="$REPO_ROOT/.venv/bin/python"

if [ -x "$VENV_PYTHON" ]; then
  PYTHON="$VENV_PYTHON"
else
  PYTHON="${PYTHON:-python3}"
fi

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

cd "$SCRIPT_DIR"

step=1; total=4
progress_bar $step $total "Running deep code and config audit..."
"$PYTHON" audit_and_reorganize.py
((step++))
progress_bar $step $total "Running automated tests and deploy verification..."
"$PYTHON" test-api-routes.py
"$PYTHON" test-gis-quick.py
((step++))
progress_bar $step $total "Refactoring GUIs and APIs for production..."
"$PYTHON" infrastructure_monitor.py
"$PYTHON" infrastructure_monitor_web.py
((step++))
progress_bar $step $total "Deploying to cloud and scaling agents..."
docker compose -f "$REPO_ROOT/docker-compose.hive.yml" up -d --scale agent=50 dashboard
((step++))
progress_bar $step $total "All checks and productionization steps finished."
echo "\nDeployment complete."
echo "Access FastAPI docs at: http://localhost:8000/docs"
echo "Access dashboard at: http://localhost:3000"
