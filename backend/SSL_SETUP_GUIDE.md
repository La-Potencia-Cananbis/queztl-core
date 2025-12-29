# 🔒 SSL/TLS Configuration for Mobile Dashboard

## Current Setup: Self-Signed Certificate

The mobile dashboard now supports HTTPS with a self-signed certificate for development/testing.

### Quick Start

```bash
# Generate SSL certificate (one-time)
./generate_ssl_cert.sh

# Start dashboard with SSL
./start-mobile-dashboard.sh
```

### Accessing HTTPS Dashboard

1. **From your Samsung phone**: `https://10.112.221.224:9999`
2. **First access warning**: You'll see "Your connection is not private"
   - Click **Advanced**
   - Click **Proceed to 10.112.221.224 (unsafe)**
   - This is safe - it's YOUR certificate on YOUR local network

3. **After accepting**: Dashboard works normally with encryption

---

## Production SSL (TODO)

For production deployment, replace self-signed cert with real certificate:

### Option 1: Let's Encrypt (FREE + Automated)

```bash
# Install certbot
brew install certbot  # macOS
# OR
sudo apt install certbot  # Linux

# Get certificate (requires public domain)
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl_certs/cert.pem
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl_certs/key.pem

# Restart dashboard
./start-mobile-dashboard.sh
```

**Auto-renewal** (Let's Encrypt certs expire in 90 days):
```bash
# Add to crontab
0 0 1 * * certbot renew --quiet && cp /etc/letsencrypt/live/yourdomain.com/*.pem /path/to/ssl_certs/
```

### Option 2: Domain Registrar Certificate

If you have a domain (senasaitech.com, quetzalcore.com, etc.):

1. **Purchase SSL certificate** from registrar (GoDaddy, Namecheap, etc.)
2. **Download certificate files**:
   - Certificate: `certificate.crt` → rename to `cert.pem`
   - Private Key: `private.key` → rename to `key.pem`
   - Certificate Chain (optional): `ca_bundle.crt`

3. **Install**:
```bash
cp certificate.crt ssl_certs/cert.pem
cp private.key ssl_certs/key.pem
chmod 644 ssl_certs/cert.pem
chmod 600 ssl_certs/key.pem
```

4. **Restart**:
```bash
./start-mobile-dashboard.sh
```

### Option 3: Corporate/Internal CA

If you have internal Certificate Authority:

```bash
# Generate CSR (Certificate Signing Request)
openssl req -new -newkey rsa:4096 -nodes \
    -keyout ssl_certs/key.pem \
    -out ssl_certs/request.csr \
    -subj "/CN=quetzalcore-mobile/O=YourCompany"

# Submit request.csr to your CA
# Receive signed certificate back

# Install signed cert
cp signed-certificate.pem ssl_certs/cert.pem

# Restart
./start-mobile-dashboard.sh
```

---

## Security Checklist

### Current Status: ⚠️ Development Mode
- [x] Self-signed certificate generated
- [x] HTTPS enabled on port 9999
- [x] Local network encryption active
- [ ] **Production certificate needed for public access**
- [ ] Certificate auto-renewal configured
- [ ] HSTS headers enabled
- [ ] Certificate pinning implemented

### For Production:
```python
# Add to mobile_dashboard.py for production hardening:
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Force HTTPS
app.add_middleware(HTTPSRedirectMiddleware)

# Only allow specific hosts
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
)
```

---

## Certificate Files

- **Location**: `ssl_certs/`
- **Certificate**: `cert.pem` (public, 644 permissions)
- **Private Key**: `key.pem` (secret, 600 permissions)
- **Valid for**: 365 days (self-signed)

### Renewal Reminder

Set calendar reminder for **November 7, 2026** (1 year from now) to:
1. Generate new certificate OR
2. Switch to Let's Encrypt auto-renewal

---

## Troubleshooting

### Certificate Error on Phone
**Problem**: "NET::ERR_CERT_AUTHORITY_INVALID"
**Solution**: This is expected with self-signed certs. Click "Advanced" → "Proceed"

### Dashboard Won't Start with SSL
```bash
# Check certificate files exist
ls -lh ssl_certs/

# Check permissions
chmod 644 ssl_certs/cert.pem
chmod 600 ssl_certs/key.pem

# Regenerate if corrupted
rm -rf ssl_certs/
./generate_ssl_cert.sh
```

### Port Already in Use
```bash
# Kill existing process
lsof -ti:9999 | xargs kill -9

# Restart
./start-mobile-dashboard.sh
```

---

## Testing

```bash
# Test HTTPS endpoint (skip cert verification for self-signed)
curl -k https://localhost:9999/health

# Test from another device
curl -k https://10.112.221.224:9999/health

# Check certificate details
openssl x509 -in ssl_certs/cert.pem -text -noout
```

---

## Next Steps

**For Local Development** (Current):
- ✅ Keep using self-signed certificate
- ✅ Accept browser warning on first access
- ✅ Works perfectly on local network

**For Production Deployment**:
1. Register domain or use existing (senasaitech.com)
2. Get Let's Encrypt certificate (FREE)
3. Configure auto-renewal
4. Update DNS to point to server
5. Enable HSTS and security headers
6. Consider certificate pinning for mobile app

---

## Support

- **Let's Encrypt Docs**: https://letsencrypt.org/docs/
- **FastAPI SSL**: https://fastapi.tiangolo.com/deployment/https/
- **OpenSSL Commands**: https://www.openssl.org/docs/

Last Updated: December 7, 2025
