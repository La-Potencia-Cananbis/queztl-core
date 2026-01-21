#!/usr/bin/env bash
# Discover Beast/Sloth IPs on local LAN using nmap ping sweep.
# Usage: ./scripts/find-nodes.sh [CIDR]
# Example: ./scripts/find-nodes.sh 192.168.1.0/24

set -euo pipefail

CIDR="${1:-192.168.1.0/24}"
echo "🔍 Scanning ${CIDR} for beast/sloth..."

if ! command -v nmap >/dev/null 2>&1; then
  echo "Installing nmap (sudo required)..."
  sudo apt-get update -y && sudo apt-get install -y nmap
fi

nmap -sn "${CIDR}" \
  | grep -B2 -Ei "(beast|sloth)" \
  | grep "Nmap scan report" \
  | awk '{print $NF}'

echo "Done." 