# QC-PROVISIONING MASTER DOCUMENTATION
# Canonical PXE + PKI + Enrollment + Node Bootstrap for Qc Cluster

This file serves as the authoritative reference for the Queztl cluster provisioning system.

## SYSTEM OVERVIEW

- **OS**: Debian-based (head node + nodes)
- **PKI**: Smallstep step-ca
- **Enrollment**: FastAPI-based phone-home service
- **Authentication**: mTLS with node identity
- **Deployment**: Zero-touch PXE boot
- **Configuration**: Git-driven Python runtime

## ARCHITECTURE

### Boot Flow
```
PXE boot
 → unattended Debian install (base OS only)
 → first boot systemd unit
 → phone-home enrollment (weak auth)
 → head node assigns identity + role
 → node requests mTLS cert from step-ca
 → node reconfigures hostname, pulls Git repo
 → node runs Python Qc bootstrap
 → node joins evolving cluster
```

### Roles
- **server**: head node / hypervisor / orchestration
- **node**: headless compute
- **hybrid**: compute + optional GUI

**Important**: PXE never decides role. HEAD NODE decides role.

## PKI: STEP-CA (DEBIAN)

### Installation Script
Location: `pki/step-ca/install-step-ca.sh`

### Service Configuration
Location: `pki/step-ca/step-ca.service`

### Initialization Notes
- Name: "QC Internal CA"
- DNS: ca.qc.lan
- Provisioner: qc-jwk
- Root CA key moved OFFLINE after init
- Intermediate key kept online
- Root cert exported to nodes: `/usr/local/share/ca-certificates/qc-root-ca.crt`

## ENROLLMENT API (FASTAPI)

### Dependencies
Location: `enroll/requirements.txt`

### Main Application
Location: `enroll/app/main.py`

### Endpoints
- `POST /enroll`: Node enrollment with MAC fingerprinting

### Authentication Flow
1. Node sends MAC addresses
2. Server generates fingerprint
3. Server assigns role and identity
4. Server mints JWT token
5. Node receives certificate from step-ca

## NODE FIRST-BOOT AGENT

### Phone-home Script
Location: `node/qc-phonehome.sh`

### Systemd Service
Location: `node/qc-phonehome.service`

### Process
1. Collect MAC addresses
2. POST to enrollment API
3. Bootstrap step-ca
4. Request mTLS certificate
5. Set hostname
6. Clone Git repository
7. Run Qc bootstrap

## ACME / SERVICE CERTS

- step-ca ACME endpoint: `https://ca.qc.lan:8443/acme/acme/directory`
- Internal services use certbot or acme.sh
- Automatic certificate renewal
- Node identity certs remain mTLS (NOT ACME-issued)

## INTEGRATION WITH QUEZTL

This provisioning system integrates with the existing Queztl deployment:

1. **Phase 1**: Manual Ubuntu Server install (Beast/Sloth)
2. **Phase 2**: PXE-based Debian install (Lab Optiplexes)
3. **Phase 3**: Full zero-touch provisioning

See `MULTI_SITE_DEPLOYMENT.md` for deployment phases.

---

**Authoritative Document**: qc-provisioning_master.txt
**Status**: Canonical reference for all provisioning automation
