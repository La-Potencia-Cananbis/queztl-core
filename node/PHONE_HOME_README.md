# QC Zero-Touch Provisioning - Phone-Home Implementation

## Overview
The phone-home flow allows newly installed nodes to automatically:
1. Identify themselves via MAC address fingerprinting
2. Enroll with the headnode's enrollment API
3. Obtain mTLS certificates from step-ca
4. Configure hostname, role, and clone the codebase
5. Bootstrap into the cluster

## Components

### 1. qc-phonehome.sh
- **Location**: `/usr/local/bin/qc-phonehome.sh`
- **Purpose**: First-boot enrollment script
- **Flow**:
  1. Collect all MAC addresses from network interfaces
  2. POST to enrollment API with MACs + IP
  3. Receive: hostname, node_id, role, JWT token
  4. Bootstrap step-ca client with CA root
  5. Request certificate using JWT token
  6. Set hostname
  7. Clone/update git repository
  8. Run bootstrap command
  9. Mark first boot as complete

### 2. qc-phonehome.service
- **Location**: `/etc/systemd/system/qc-phonehome.service`
- **Purpose**: Systemd unit for first-boot execution
- **Features**:
  - Runs once only (ConditionPathExists=!/var/lib/qc/firstboot.done)
  - Waits for network connectivity
  - Runs as root
  - 5-minute timeout
  - Auto-retry on failure (30s interval)
  - Logs to journal + console

## Installation in Preseed

Add to late_command in Debian preseed:

```bash
# Install phone-home scripts
wget -O /target/usr/local/bin/qc-phonehome.sh \
  https://raw.githubusercontent.com/La-Potencia-Cananbis/queztl-core/main/node/qc-phonehome.sh; \
chmod +x /target/usr/local/bin/qc-phonehome.sh; \

wget -O /target/etc/systemd/system/qc-phonehome.service \
  https://raw.githubusercontent.com/La-Potencia-Cananbis/queztl-core/main/node/qc-phonehome.service; \

in-target systemctl enable qc-phonehome.service; \
```

## Environment Variables

Set in qc-phonehome.service or via DHCP option 252:

- **QC_ENROLL_URL**: Enrollment API endpoint (default: https://enroll.qc.lan/enroll)

## Dependencies

Installed by preseed late_command:
- curl
- jq
- git
- ca-certificates
- step-cli (from Smallstep repos)

## Security

- JWT tokens are single-use and short-lived (1 hour)
- Certificates are issued with mTLS subject alternative names
- Node identity is cryptographically bound to MAC fingerprint
- CA root certificate is verified during bootstrap

## Testing

Manual enrollment test (as root on new node):

```bash
export QC_ENROLL_URL="https://enroll.qc.lan/enroll"
bash -x /usr/local/bin/qc-phonehome.sh
```

Check enrollment status:

```bash
journalctl -u qc-phonehome.service -f
ls -l /etc/qc/pki/
step certificate inspect /etc/qc/pki/node.crt
```

## Troubleshooting

### Enrollment fails with network error
- Check DNS resolution: `nslookup enroll.qc.lan`
- Check connectivity: `curl -k https://enroll.qc.lan/health`
- Verify enrollment API is running on headnode

### Certificate request fails
- Check step-ca status: `systemctl status step-ca`
- Verify JWK provisioner exists: `step ca provisioner list`
- Check token validity: Token may have expired (1 hour TTL)

### Script doesn't run on boot
- Check service status: `systemctl status qc-phonehome.service`
- Verify condition: `test -f /var/lib/qc/firstboot.done && echo "Already enrolled"`
- Re-enable: `rm /var/lib/qc/firstboot.done && systemctl restart qc-phonehome.service`

## Re-enrollment

To re-enroll a node (testing only):

```bash
rm /var/lib/qc/firstboot.done
systemctl restart qc-phonehome.service
journalctl -u qc-phonehome.service -f
```

## Integration with Enrollment API

The phone-home script expects this response from POST /enroll:

```json
{
  "node_id": "a1b2c3d4e5f6",
  "hostname": "qc-node-001",
  "role": "node",
  "fingerprint": "a1b2c3...",
  "step_token": "eyJhbGc...",
  "step_ca_url": "https://ca.qc.lan",
  "step_provisioner": "qc-jwk",
  "git_repo": "https://github.com/La-Potencia-Cananbis/queztl-core",
  "git_ref": "main",
  "bootstrap_cmd": "cd /opt/queztl-core && ./scripts/node-setup.sh"
}
```

All fields are required for successful enrollment.
