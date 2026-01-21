#!/usr/bin/env bash
# Deploy the frontend-new static site to local nginx on a target host.
# Usage: ./nginx-deploy-frontend-new.sh [user@host]
# Example: ./nginx-deploy-frontend-new.sh xava@192.168.1.105

set -euo pipefail

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "Usage: $0 user@host" >&2
  exit 1
fi

SITE_NAME="frontend-new"
REMOTE_ROOT="/var/www/${SITE_NAME}"
NGINX_CONF="/etc/nginx/sites-available/${SITE_NAME}.conf"

echo "🚀 Deploying ${SITE_NAME} to ${TARGET} via rsync + nginx"

# 1) Sync files
rsync -avz --delete \
  --exclude '.git' \
  --exclude '.DS_Store' \
  --exclude 'node_modules' \
  $(pwd)/frontend-new/ ${TARGET}:${REMOTE_ROOT}/

# 2) Install nginx and enable site
ssh -o BatchMode=yes ${TARGET} << 'EOF'
set -euo pipefail
sudo apt-get update -y
sudo apt-get install -y nginx

sudo tee /etc/nginx/sites-available/frontend-new.conf >/dev/null <<'NGCONF'
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    root /var/www/frontend-new;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Basic security headers
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header Referrer-Policy "strict-origin-when-cross-origin";
}
NGCONF

sudo ln -sf /etc/nginx/sites-available/frontend-new.conf /etc/nginx/sites-enabled/frontend-new.conf

sudo nginx -t
sudo systemctl restart nginx
EOF

echo "✅ Deployed. Test: http://${TARGET#*@}/"