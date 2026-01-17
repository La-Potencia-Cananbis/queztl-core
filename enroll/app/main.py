#!/usr/bin/env python3
"""
QC Enrollment API
Handles zero-touch node enrollment with mTLS identity
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib
import json
import os
import time
from pathlib import Path
from jose import jwt
from typing import Optional

app = FastAPI(title="QC Enrollment API", version="1.0.0")

# Configuration
DB_PATH = os.getenv("QC_ENROLL_DB", "/var/lib/qc-enroll/nodes.json")
STEP_CA_URL = os.getenv("STEP_CA_URL", "https://ca.qc.lan:8443")
PROVISIONER = os.getenv("STEP_PROVISIONER", "qc-jwk")
JWK_PATH = os.getenv("JWK_PRIVATE_PATH", "/etc/qc-enroll/jwk_private.json")
GIT_REPO = os.getenv("QC_GIT_REPO", "https://github.com/La-Potencia-Cananbis/queztl-core.git")
GIT_REF = os.getenv("QC_GIT_REF", "main")
TOKEN_TTL = int(os.getenv("TOKEN_TTL", "300"))


def load_db():
    """Load node database from disk."""
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH) as f:
        return json.load(f)


def save_db(db):
    """Save node database to disk."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)


def fingerprint(macs: list[str]) -> str:
    """Generate deterministic fingerprint from MAC addresses."""
    return hashlib.sha256(",".join(sorted(macs)).encode()).hexdigest()


def mint_token(node_id: str, hostname: str, ip: Optional[str]) -> str:
    """
    Mint a JWT token for step-ca certificate request.
    Uses JWK provisioner credentials.
    """
    if not os.path.exists(JWK_PATH):
        raise HTTPException(500, f"JWK private key not found at {JWK_PATH}")
    
    with open(JWK_PATH) as f:
        jwk = json.load(f)
    
    now = int(time.time())
    
    sans = [hostname]
    if ip:
        sans.append(ip)
    
    payload = {
        "iss": "https://enroll.qc.lan",  # Issuer
        "aud": STEP_CA_URL,               # Audience (step-ca)
        "sub": node_id,                   # Subject (node identity)
        "iat": now,                       # Issued at
        "nbf": now - 5,                   # Not before (5s grace)
        "exp": now + TOKEN_TTL,           # Expires
        "provisioner": PROVISIONER,       # step-ca provisioner name
        "sans": sans                      # Subject Alternative Names
    }
    
    return jwt.encode(payload, jwk, algorithm="ES256")


class EnrollRequest(BaseModel):
    """Node enrollment request payload."""
    macs: list[str]
    ip: Optional[str] = None


class EnrollResponse(BaseModel):
    """Node enrollment response payload."""
    node_id: str
    hostname: str
    role: str
    fingerprint: str
    step_token: str
    step_ca_url: str
    step_provisioner: str
    git_repo: str
    git_ref: str
    bootstrap_cmd: str


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "qc-enrollment"}


@app.post("/enroll", response_model=EnrollResponse)
def enroll(req: EnrollRequest):
    """
    Enroll a new node or return existing identity.
    
    Flow:
    1. Generate fingerprint from MAC addresses
    2. Look up existing node or assign new identity
    3. Determine role (server, node, hybrid)
    4. Generate hostname based on role
    5. Mint JWT token for step-ca
    6. Return configuration to node
    """
    db = load_db()
    
    # Generate fingerprint
    fp = fingerprint(req.macs)
    
    # Get or create node identity
    existing = db.get(fp, {})
    node_id = existing.get("id", f"qc-node-{fp[-6:]}")
    role = existing.get("role", "node")
    
    # Generate hostname based on role
    if role == "server":
        hostname = "head.qc.lan"
    else:
        hostname = f"qc-{role}-{fp[-4:]}.qc.lan"
    
    # Mint certificate token
    try:
        token = mint_token(node_id, hostname, req.ip)
    except Exception as e:
        raise HTTPException(500, f"Failed to mint token: {e}")
    
    # Update database
    db[fp] = {
        "id": node_id,
        "role": role,
        "hostname": hostname,
        "macs": req.macs,
        "last_seen": time.time()
    }
    save_db(db)
    
    return EnrollResponse(
        node_id=node_id,
        hostname=hostname,
        role=role,
        fingerprint=fp,
        step_token=token,
        step_ca_url=STEP_CA_URL,
        step_provisioner=PROVISIONER,
        git_repo=GIT_REPO,
        git_ref=GIT_REF,
        bootstrap_cmd="cd /opt/queztl-core && ./scripts/node-setup.sh"
    )


@app.get("/nodes")
def list_nodes():
    """List all enrolled nodes (admin endpoint)."""
    db = load_db()
    return {
        "nodes": [
            {
                "fingerprint": fp,
                **data
            }
            for fp, data in db.items()
        ]
    }


@app.post("/admin/set-role/{fingerprint}")
def set_role(fingerprint: str, role: str):
    """
    Manually set node role (admin endpoint).
    Roles: server, node, hybrid
    """
    if role not in ["server", "node", "hybrid"]:
        raise HTTPException(400, "Invalid role. Must be: server, node, or hybrid")
    
    db = load_db()
    if fingerprint not in db:
        raise HTTPException(404, "Node not found")
    
    db[fingerprint]["role"] = role
    save_db(db)
    
    return {"status": "ok", "fingerprint": fingerprint, "role": role}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
