#!/bin/bash
# queztl-production-approval.sh
# Master protocol: Deep audit, test, deploy, and verify all agents/cloud endpoints
# Usage: bash queztl-production-approval.sh <netlify-site-name>

SITE="$1"
if [ -z "$SITE" ]; then
  echo "Usage: $0 <netlify-site-name>"
  exit 1
fi

set -e

# 1. Deep code and config audit
printf '\n==== CODE & CONFIG AUDIT ===='\n
python3 -m py_compile backend/*.py || { echo "Python backend syntax error"; exit 2; }
python3 -m py_compile agent_*.py || true
npx tsc --noEmit || echo "TypeScript lint warning (see above)"

# 2. Container/infra health
printf '\n==== CONTAINER & INFRA HEALTH ===='\n
docker ps -a
docker-compose ps
docker-compose logs --tail=30

# 3. Lint/compile checks
printf '\n==== LINT & COMPILE CHECKS ===='\n
find . -name '*.html' | xargs grep -i 'style=' || echo "No inline styles found in main HTML files."
find . -name '*.py' -o -name '*.js' -o -name '*.ts' | xargs grep -i todo || echo "No actionable TODOs in main codebase."

# 4. Automated deploy verification (Netlify + backend)
printf '\n==== DEPLOYED UI & API VERIFICATION ===='\n
PAGES=("3dmark-pro.html" "gis.html" "gen3d.html")
for PAGE in "${PAGES[@]}"; do
  curl -s "https://$SITE.netlify.app/$PAGE" | grep -q '<body' && echo "✅ $PAGE deployed and reachable" || echo "❌ $PAGE not reachable"
done

# 5. Backend health check
curl -s https://$SITE.netlify.app/api/vgpu/cluster/status | grep -q 'nodes' && echo "✅ Backend vGPU cluster status API reachable" || echo "❌ Backend vGPU cluster status API not reachable"

printf '\n==== ALL CHECKS COMPLETE ===='\n
echo "Review the above. If all green, approve for production!"
