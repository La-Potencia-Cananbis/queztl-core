"""Queztl cluster discovery + role detection.

This module centralizes *network reality*:
- Beast/Sloth may be DHCP (IPs change)
- Optiplex workers may be DNS hostnames (optiplex1, optiplex2, ...)
- Laptop/Mac is command-center only (no heavy compute)

Design goals:
- Fail fast by default (no silent local-compute fallback on command-center)
- Prefer explicit config via env vars, but support best-effort discovery

Environment variables (all optional):
- QUEZTL_NODE_NAME: override local node name (e.g. 'mac', 'beast', 'sloth')
- QUEZTL_COMMAND_CENTER: '1' to force command-center mode
- QUEZTL_SSH_USER: SSH username (default: 'xava')
- QUEZTL_DISCOVER_SUBNET: subnet for nmap discovery (default: '192.168.1.0/24')
- QUEZTL_BEAST_HOST: explicit host/IP for Beast
- QUEZTL_SLOTH_HOST: explicit host/IP for Sloth
- QUEZTL_OPTIPLEX_HOSTS: comma-separated optiplex hostnames (default: optiplex1..4)
- QUEZTL_SEED_NODES: comma-separated seed nodes for peer discovery (hostnames/IPs)

If Beast/Sloth hosts are not explicitly provided, resolve_cluster_hosts() will try:
1) nmap -sn <subnet>
2) SSH hostname probing to map discovered IPs to 'beast'/'sloth'

If that still fails, it returns partial results and leaves it to callers
to error out or request user configuration.
"""

from __future__ import annotations

import os
import platform
import re
import shlex
import socket
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Optional


DEFAULT_SUBNET = "192.168.1.0/24"
DEFAULT_OPTIPLEX_HOSTS = [f"optiplex{i}" for i in range(1, 5)]


@dataclass(frozen=True)
class ClusterHosts:
    beast: Optional[str] = None
    sloth: Optional[str] = None
    optiplex: List[str] = None

    def __post_init__(self):
        # dataclass(frozen=True) doesn't allow normal assignment; use object.__setattr__
        if self.optiplex is None:
            object.__setattr__(self, "optiplex", [])


def node_name() -> str:
    return os.environ.get("QUEZTL_NODE_NAME") or socket.gethostname()


def is_command_center() -> bool:
    """Command-center is the orchestration-only machine (typically macOS laptop)."""
    if os.environ.get("QUEZTL_COMMAND_CENTER") == "1":
        return True
    # Conservative: treat macOS as command center unless explicitly overridden.
    if platform.system().lower() == "darwin" and os.environ.get("QUEZTL_ALLOW_LOCAL_COMPUTE") != "1":
        return True
    # Also treat hostnames containing 'mac' or 'laptop' as command center unless overridden.
    hn = node_name().lower()
    if any(tok in hn for tok in ("mac", "laptop", "mbp", "command")) and os.environ.get("QUEZTL_ALLOW_LOCAL_COMPUTE") != "1":
        return True
    return False


def ssh_user(default: str = "xava") -> str:
    return os.environ.get("QUEZTL_SSH_USER") or default


def _has_cmd(cmd: str) -> bool:
    return subprocess.call(["bash", "-lc", f"command -v {shlex.quote(cmd)} >/dev/null 2>&1"]) == 0


def discover_live_ips(subnet: Optional[str] = None) -> List[str]:
    """Best-effort L2 discovery using nmap -sn.

    Returns list of IPs. If nmap isn't available, returns empty list.
    """
    subnet = subnet or os.environ.get("QUEZTL_DISCOVER_SUBNET") or DEFAULT_SUBNET
    if not _has_cmd("nmap"):
        return []

    try:
        proc = subprocess.run(
            ["nmap", "-sn", subnet],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        out = proc.stdout or ""
    except Exception:
        return []

    # Lines look like: "Nmap scan report for 192.168.1.105"
    ips = re.findall(r"Nmap scan report for (\d+\.\d+\.\d+\.\d+)", out)
    # Keep unique while preserving order
    seen = set()
    ordered = []
    for ip in ips:
        if ip not in seen:
            seen.add(ip)
            ordered.append(ip)
    return ordered


def probe_hostname_via_ssh(ip: str, user: str, timeout_s: int = 3) -> Optional[str]:
    """Return remote hostname for an IP using SSH, or None."""
    try:
        proc = subprocess.run(
            [
                "ssh",
                "-o",
                "BatchMode=yes",
                "-o",
                f"ConnectTimeout={timeout_s}",
                f"{user}@{ip}",
                "hostname",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_s + 2,
        )
        if proc.returncode != 0:
            return None
        hn = (proc.stdout or "").strip()
        return hn or None
    except Exception:
        return None


def probe_has_nvidia_gpu(ip: str, user: str, timeout_s: int = 4) -> bool:
    """True if remote host appears to have NVIDIA GPU (nvidia-smi present + works)."""
    try:
        proc = subprocess.run(
            [
                "ssh",
                "-o",
                "BatchMode=yes",
                "-o",
                f"ConnectTimeout={timeout_s}",
                f"{user}@{ip}",
                "bash",
                "-lc",
                "command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi -L >/dev/null 2>&1",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_s + 2,
        )
        return proc.returncode == 0
    except Exception:
        return False


def resolve_cluster_hosts() -> ClusterHosts:
    """Resolve Beast/Sloth/Optiplex hosts using env vars and best-effort discovery."""
    beast = os.environ.get("QUEZTL_BEAST_HOST")
    sloth = os.environ.get("QUEZTL_SLOTH_HOST")

    optiplex_env = os.environ.get("QUEZTL_OPTIPLEX_HOSTS")
    if optiplex_env:
        optiplex = [h.strip() for h in optiplex_env.split(",") if h.strip()]
    else:
        optiplex = DEFAULT_OPTIPLEX_HOSTS

    if beast and sloth:
        return ClusterHosts(beast=beast, sloth=sloth, optiplex=optiplex)

    # Attempt discovery for missing hosts
    user = ssh_user()
    live_ips = discover_live_ips()

    # Try to map via hostname first
    for ip in live_ips:
        if beast and sloth:
            break
        hn = probe_hostname_via_ssh(ip, user=user)
        if not hn:
            continue
        lhn = hn.lower()
        if (not beast) and "beast" in lhn:
            beast = ip
        elif (not sloth) and "sloth" in lhn:
            sloth = ip

    # If still missing, use GPU heuristic for Beast
    if not beast:
        for ip in live_ips:
            if probe_has_nvidia_gpu(ip, user=user):
                beast = ip
                break

    # Sloth: choose a remaining live IP that isn't Beast (best effort)
    if not sloth and live_ips:
        for ip in live_ips:
            if ip != beast:
                sloth = ip
                break

    return ClusterHosts(beast=beast, sloth=sloth, optiplex=optiplex)


def seed_nodes() -> List[str]:
    """Seed nodes for peer discovery / cluster join."""
    env = os.environ.get("QUEZTL_SEED_NODES")
    if env:
        return [h.strip() for h in env.split(",") if h.strip()]

    hosts = resolve_cluster_hosts()
    seeds: List[str] = []
    if hosts.sloth:
        seeds.append(hosts.sloth)
    if hosts.beast:
        seeds.append(hosts.beast)
    # Optiplex hostnames are stable DNS in the remote site
    seeds.extend(hosts.optiplex)

    # Deduplicate while preserving order
    seen = set()
    out: List[str] = []
    for h in seeds:
        if h not in seen:
            seen.add(h)
            out.append(h)
    return out
