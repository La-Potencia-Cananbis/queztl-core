#!/usr/bin/env bash
# Discover Beast/Sloth IPs on local LAN using nmap ping sweep.
# Usage: ./scripts/find-nodes.sh [CIDR]
# Example: ./scripts/find-nodes.sh 192.168.1.0/24

set -euo pipefail

CIDR="${1:-192.168.1.0/24}"
echo "🔍 Scanning ${CIDR} for beast/sloth..."

if ! command -v nmap >/dev/null 2>&1; then
  echo "nmap not found. Attempting install..."
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update -y && sudo apt-get install -y nmap
  elif command -v brew >/dev/null 2>&1; then
    brew install nmap
  else
    echo "Please install nmap manually (apt-get or brew)." >&2
    exit 1
  fi
fi

nmap -sn "${CIDR}" \
  | grep -B2 -Ei "(beast|sloth)" \
  | grep "Nmap scan report" \
  | awk '{print $NF}'

echo "Done." 