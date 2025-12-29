#!/bin/bash
# Generate self-signed SSL certificate for mobile dashboard
# This creates a temporary cert for HTTPS - replace with real cert in production

CERT_DIR="ssl_certs"
DAYS_VALID=365

echo "🔐 Generating SSL Certificate for Mobile Dashboard..."

# Create cert directory
mkdir -p "$CERT_DIR"

# Generate private key and self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes \
    -keyout "$CERT_DIR/key.pem" \
    -out "$CERT_DIR/cert.pem" \
    -days $DAYS_VALID \
    -subj "/C=US/ST=California/L=San Francisco/O=QuetzalCore/OU=Mobile/CN=quetzalcore-mobile" \
    -addext "subjectAltName=IP:10.112.221.224,DNS:localhost"

# Set proper permissions
chmod 600 "$CERT_DIR/key.pem"
chmod 644 "$CERT_DIR/cert.pem"

echo "✅ SSL Certificate generated!"
echo "📁 Certificate: $CERT_DIR/cert.pem"
echo "🔑 Private Key: $CERT_DIR/key.pem"
echo ""
echo "⚠️  This is a SELF-SIGNED certificate. Your phone will show a security warning."
echo "    You'll need to accept it to proceed."
echo ""
echo "🔒 For PRODUCTION, replace with a real certificate from:"
echo "   - Let's Encrypt (free, automated)"
echo "   - Your domain registrar"
echo "   - Corporate CA"
echo ""
echo "📱 Dashboard will now run on: https://10.112.221.224:9999"
