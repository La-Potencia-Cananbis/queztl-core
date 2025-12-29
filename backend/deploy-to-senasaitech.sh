#!/bin/bash
# 🚀 DEPLOY TO SENASAITECH.COM
# Full production deployment with SSL certs

set -e

echo "========================================"
echo "🚀 DEPLOYING TO SENASAITECH.COM"
echo "========================================"

# Configuration
SUBDOMAIN="${SUBDOMAIN:-api}"
DOMAIN="senasaitech.com"
FULL_DOMAIN="${SUBDOMAIN}.${DOMAIN}"
SERVER_IP="${SERVER_IP}"
DEPLOY_USER="${DEPLOY_USER:-root}"
EMAIL="${CERTBOT_EMAIL:-admin@senasaitech.com}"

echo ""
echo "📋 Deployment Configuration:"
echo "   Domain: $FULL_DOMAIN"
echo "   Server IP: ${SERVER_IP:-NOT SET}"
echo "   Email: $EMAIL"
echo ""

if [ -z "$SERVER_IP" ]; then
    echo "❌ ERROR: Set SERVER_IP environment variable"
    echo "   Example: export SERVER_IP=192.168.1.100"
    exit 1
fi

# 1. CREATE DEPLOYMENT PACKAGE
echo "📦 Creating deployment package..."
rm -rf /tmp/senasai-deploy
mkdir -p /tmp/senasai-deploy

# Copy backend
cp -r backend /tmp/senasai-deploy/

# Create requirements
cat > /tmp/senasai-deploy/requirements.txt << 'EOF'
torch>=2.0.0
torchvision
fastapi>=0.104.0
uvicorn[standard]
websockets
sqlalchemy>=2.0.0
asyncpg
psutil
pillow
numpy
aiofiles
python-multipart
trimesh
transformers
diffusers
accelerate
scikit-learn
scipy
matplotlib
seaborn
plotly
redis
numba
shapely
rasterio
pyproj
opencv-python
EOF

# Copy deployment scripts
cp register_rgis_worker.py /tmp/senasai-deploy/
cp sync_rgis_data.py /tmp/senasai-deploy/
cp rgis_data_server.py /tmp/senasai-deploy/
cp test_mining_api.py /tmp/senasai-deploy/

# Create systemd service
cat > /tmp/senasai-deploy/quetzalcore.service << 'EOF'
[Unit]
Description=QuetzalCore API Server (SenasaiTech)
After=network.target

[Service]
Type=simple
User=quetzalcore
WorkingDirectory=/opt/quetzalcore
Environment="PATH=/opt/quetzalcore/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONPATH=/opt/quetzalcore"
ExecStart=/opt/quetzalcore/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx config with SSL
cat > /tmp/senasai-deploy/nginx.conf << EOF
# HTTP - redirect to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name ${FULL_DOMAIN};
    
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    
    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

# HTTPS
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name ${FULL_DOMAIN};
    
    # SSL certificates (will be created by certbot)
    ssl_certificate /etc/letsencrypt/live/${FULL_DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${FULL_DOMAIN}/privkey.pem;
    
    # SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Logging
    access_log /var/log/nginx/${FULL_DOMAIN}_access.log;
    error_log /var/log/nginx/${FULL_DOMAIN}_error.log;
    
    # Proxy settings
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        
        # Timeouts for long-running requests
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
    
    # WebSocket support
    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

# Create installation script
cat > /tmp/senasai-deploy/install.sh << 'INSTALLSCRIPT'
#!/bin/bash
set -e

DOMAIN="$1"
EMAIL="$2"

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo "Usage: $0 <domain> <email>"
    exit 1
fi

echo "🔧 Installing QuetzalCore for SenasaiTech..."
echo "   Domain: $DOMAIN"
echo "   Email: $EMAIL"

# Update system
apt-get update
apt-get upgrade -y

# Install dependencies
apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    build-essential \
    nginx \
    certbot \
    python3-certbot-nginx \
    ufw \
    git \
    curl \
    htop

# Create quetzalcore user
useradd -r -s /bin/bash -d /opt/quetzalcore quetzalcore 2>/dev/null || echo "User exists"

# Create directories
mkdir -p /opt/quetzalcore /var/www/html
cd /opt/quetzalcore

# Copy files
cp -r backend .
cp requirements.txt .
cp *.py . 2>/dev/null || true

# Create venv
echo "🐍 Creating Python environment..."
sudo -u quetzalcore python3.11 -m venv venv

# Install dependencies
echo "📦 Installing Python packages (this takes ~5 minutes)..."
sudo -u quetzalcore /opt/quetzalcore/venv/bin/pip install --upgrade pip wheel setuptools
sudo -u quetzalcore /opt/quetzalcore/venv/bin/pip install -r requirements.txt

# Set permissions
chown -R quetzalcore:quetzalcore /opt/quetzalcore

# Install systemd service
cp quetzalcore.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable quetzalcore
systemctl start quetzalcore

echo "⏳ Waiting for backend to start..."
sleep 5

# Check if backend is running
if systemctl is-active --quiet quetzalcore; then
    echo "✅ Backend started successfully"
else
    echo "❌ Backend failed to start. Check logs:"
    journalctl -u quetzalcore -n 50
    exit 1
fi

# Configure Nginx
echo "🌐 Configuring Nginx..."
cp nginx.conf /etc/nginx/sites-available/$DOMAIN
ln -sf /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx config
nginx -t

# Start Nginx
systemctl enable nginx
systemctl restart nginx

# Get SSL certificate
echo "🔐 Getting SSL certificate..."
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email $EMAIL --redirect

# Configure firewall
echo "🔥 Configuring firewall..."
ufw --force enable
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw allow 8000/tcp # Direct API access (optional)
ufw reload

# Test the deployment
echo "🧪 Testing deployment..."
sleep 2
curl -k https://localhost/api/health > /dev/null 2>&1 && echo "✅ HTTPS working!" || echo "⚠️ HTTPS test failed"

# Setup auto-renewal for SSL
echo "⏰ Setting up SSL auto-renewal..."
systemctl enable certbot.timer
systemctl start certbot.timer

echo ""
echo "========================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "========================================"
echo ""
echo "🌐 Your API is now live at:"
echo "   https://$DOMAIN"
echo ""
echo "📊 Test endpoints:"
echo "   https://$DOMAIN/api/health"
echo "   https://$DOMAIN/api/gen3d/capabilities"
echo "   https://$DOMAIN/api/mining/survey-cost?area_km2=10"
echo ""
echo "📖 API Documentation:"
echo "   https://$DOMAIN/docs"
echo ""
echo "🔧 Management commands:"
echo "   systemctl status quetzalcore"
echo "   systemctl status nginx"
echo "   journalctl -u quetzalcore -f"
echo "   certbot certificates"
echo ""
echo "🔐 SSL certificate expires in 90 days (auto-renews)"
echo ""
INSTALLSCRIPT

chmod +x /tmp/senasai-deploy/install.sh

# Create tarball
cd /tmp
tar czf senasai-deploy.tar.gz senasai-deploy/
echo "✅ Package created: /tmp/senasai-deploy.tar.gz"

# 2. DEPLOY TO SERVER
echo ""
echo "=========================================="
echo "🚀 DEPLOYING TO SERVER"
echo "=========================================="
echo ""

echo "📤 Copying to $SERVER_IP..."
scp /tmp/senasai-deploy.tar.gz $DEPLOY_USER@$SERVER_IP:/tmp/ || {
    echo "❌ Could not copy to server"
    echo ""
    echo "🔧 MANUAL DEPLOYMENT:"
    echo "   1. Copy /tmp/senasai-deploy.tar.gz to your server"
    echo "   2. On server: cd /tmp && tar xzf senasai-deploy.tar.gz"
    echo "   3. Run: sudo bash /tmp/senasai-deploy/install.sh $FULL_DOMAIN $EMAIL"
    echo ""
    exit 1
}

echo "🔧 Installing on server..."
ssh $DEPLOY_USER@$SERVER_IP << EOSSH
cd /tmp
tar xzf senasai-deploy.tar.gz
cd senasai-deploy
bash install.sh $FULL_DOMAIN $EMAIL
EOSSH

# 3. VERIFY DEPLOYMENT
echo ""
echo "=========================================="
echo "✅ VERIFYING DEPLOYMENT"
echo "=========================================="
echo ""

sleep 5

echo "🧪 Testing HTTPS endpoint..."
curl -s https://$FULL_DOMAIN/api/health | head -5 && echo "✅ API responding!" || echo "⚠️ API not responding yet"

echo ""
echo "🧪 Testing SSL certificate..."
echo | openssl s_client -servername $FULL_DOMAIN -connect $FULL_DOMAIN:443 2>/dev/null | grep -A 2 "Verify return code" || true

# 4. UPDATE DNS (if needed)
echo ""
echo "=========================================="
echo "📋 FINAL STEPS"
echo "=========================================="
echo ""
echo "🌐 DNS Configuration (if not done):"
echo "   Add A record for: $SUBDOMAIN"
echo "   Points to: $SERVER_IP"
echo "   TTL: 300"
echo ""
echo "   In your DNS provider (Cloudflare/GoDaddy/etc):"
echo "   Type: A"
echo "   Name: $SUBDOMAIN"
echo "   Content: $SERVER_IP"
echo "   Proxy: Disabled (for initial setup)"
echo ""
echo "✅ DEPLOYMENT COMPLETE!"
echo ""
echo "🚀 Your mining/GIS APIs are now live at:"
echo "   https://$FULL_DOMAIN"
echo ""
echo "📊 Test it:"
echo "   curl https://$FULL_DOMAIN/api/gen3d/capabilities"
echo "   curl https://$FULL_DOMAIN/api/mining/survey-cost?area_km2=10"
echo ""
echo "📖 API Docs:"
echo "   https://$FULL_DOMAIN/docs"
echo ""
