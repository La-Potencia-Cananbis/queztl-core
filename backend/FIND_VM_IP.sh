#!/bin/bash

# Find your Ubuntu VM's actual IP address
# Simple script that doesn't exit on failures

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║       Find Your Ubuntu VM's IP Address                ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Method 1: Check common network ranges
echo "🔍 METHOD 1: Scanning common network ranges..."
echo ""

found=0

for ip in 192.168.1.{1..254}; do
    if ping -c 1 -W 0.5 "$ip" &>/dev/null; then
        # Found responsive IP, now check SSH
        if nc -z -w 1 "$ip" 22 2>/dev/null; then
            echo "✅ Found SSH on: $ip"
            found=1
        fi
    fi
done

if [ $found -eq 0 ]; then
    echo "⚠️  No SSH servers found on 192.168.1.0/24"
    echo ""
    echo "Try other network ranges:"
    echo "  • 10.0.0.0/24 (common default)"
    echo "  • 172.16.0.0/24 (docker networks)"
    echo ""
fi

echo ""
echo "🔍 METHOD 2: Check your local machine's network"
echo ""
echo "Your Mac's IP addresses:"
ifconfig | grep -E 'inet ' | grep -v 127.0.0.1

echo ""
echo "🔍 METHOD 3: If you can access VM terminal directly"
echo ""
echo "Run this on the Ubuntu VM:"
echo "  $ hostname -I"
echo ""
echo "That will show you the exact IP address to use."
echo ""
