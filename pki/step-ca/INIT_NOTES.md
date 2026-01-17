# Step-CA Initialization Guide

## Initial Setup

### 1. Initialize CA
```bash
sudo -u step step ca init
```

**Configuration:**
- Name: `QC Internal CA`
- DNS: `ca.qc.lan` (or your internal domain)
- Address: `:8443`
- Provisioner name: `qc-jwk`
- Password: (secure password for intermediate CA)

### 2. Configuration Location
- Config: `/etc/step-ca/config/ca.json`
- Certificates: `/etc/step-ca/certs/`
- Keys: `/etc/step-ca/secrets/`

### 3. Root CA Security
**CRITICAL**: After initialization, move root CA private key OFFLINE

```bash
# Backup root CA key
sudo cp /etc/step-ca/secrets/root_ca_key /secure/offline/location/

# Remove from online system
sudo rm /etc/step-ca/secrets/root_ca_key

# Verify intermediate CA can still operate
sudo systemctl status step-ca
```

### 4. Export Root Certificate
Nodes need the root CA certificate to trust the CA:

```bash
# Copy root cert to system trust store
sudo cp /etc/step-ca/certs/root_ca.crt /usr/local/share/ca-certificates/qc-root-ca.crt

# Update certificate trust
sudo update-ca-certificates
```

### 5. Install Systemd Service
```bash
sudo cp pki/step-ca/step-ca.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable step-ca
sudo systemctl start step-ca
```

### 6. Create Environment File
```bash
sudo tee /etc/default/step-ca > /dev/null <<EOF
# Step-CA environment
STEPPATH=/var/lib/step
EOF
```

## Provisioner Setup

### JWK Provisioner
The JWK provisioner is used by the enrollment API to mint tokens:

```bash
# Generate JWK keypair
step crypto jwk create /etc/qc-enroll/jwk_public.json /etc/qc-enroll/jwk_private.json

# Add to step-ca configuration
step ca provisioner add qc-jwk \
  --type JWK \
  --public-key /etc/qc-enroll/jwk_public.json
```

### ACME Provisioner
For automatic certificate renewal of services:

```bash
step ca provisioner add acme --type ACME
```

ACME endpoint will be: `https://ca.qc.lan:8443/acme/acme/directory`

## Verification

### Test CA is Running
```bash
curl -k https://ca.qc.lan:8443/health
```

### Test Certificate Issuance
```bash
step ca certificate test.qc.lan test.crt test.key
```

## Security Notes

1. **Root CA Key**: Must be offline after initialization
2. **Intermediate CA Key**: Kept online, encrypted at rest
3. **JWK Private Key**: Only accessible by enrollment API
4. **mTLS**: All node-to-head communication uses mutual TLS
5. **ACME**: Only for service certificates, not node identity

## Troubleshooting

### Check CA Status
```bash
sudo systemctl status step-ca
sudo journalctl -u step-ca -f
```

### Validate Configuration
```bash
sudo -u step step ca health
```

### Test Token Generation
```bash
# This should be done by enrollment API, but for testing:
step ca token test-node.qc.lan
```

## Integration Points

- **Enrollment API**: Uses JWK to mint tokens → `enroll/app/main.py`
- **Node Bootstrap**: Requests certificates → `node/qc-phonehome.sh`
- **Service Renewal**: Uses ACME for web services
- **Monitoring**: Health endpoint for cluster monitoring
