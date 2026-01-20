#!/usr/bin/env bash
# Quick SSH Key Setup for Queztl Cluster
# This script will install your SSH public key on cluster nodes

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  Queztl Cluster SSH Key Setup                                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo

# Check if SSH key exists
if [ ! -f ~/.ssh/id_rsa.pub ]; then
    echo "❌ No SSH public key found at ~/.ssh/id_rsa.pub"
    echo "   Generating SSH key..."
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -C "queztl-cluster-$(hostname)"
    echo "✅ SSH key generated"
    echo
fi

echo "📋 This script will install your SSH public key on cluster nodes"
echo "   You'll be prompted for the password for each node"
echo

# Setup Sloth
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 Setting up Sloth (Coordinator)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
SLOTH_IP="192.168.1.102"
echo "   Testing connection to ${SLOTH_IP}..."

if ping -c 1 -W 2 $SLOTH_IP >/dev/null 2>&1; then
    echo "   ✅ Sloth is reachable"
    echo "   Installing SSH key (you'll be prompted for password)..."
    
    if ssh-copy-id -o ConnectTimeout=10 xava@${SLOTH_IP} 2>&1; then
        echo "   ✅ SSH key installed on Sloth"
        
        # Test connection
        if ssh -o BatchMode=yes -o ConnectTimeout=5 xava@${SLOTH_IP} echo "Connection OK" >/dev/null 2>&1; then
            echo "   ✅ Passwordless SSH verified"
        else
            echo "   ⚠️  SSH key installed but connection test failed"
        fi
    else
        echo "   ❌ Failed to install SSH key on Sloth"
    fi
else
    echo "   ⚠️  Sloth not reachable at ${SLOTH_IP} - skipping"
fi
echo

# Setup Beast
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 Setting up Beast (GPU Node)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Try to find Beast's IP
BEAST_IP="192.168.1.105"
echo "   Trying ${BEAST_IP}..."

if ping -c 1 -W 2 $BEAST_IP >/dev/null 2>&1; then
    echo "   ✅ Beast is reachable at ${BEAST_IP}"
    echo "   Installing SSH key (you'll be prompted for password)..."
    
    if ssh-copy-id -o ConnectTimeout=10 xava@${BEAST_IP} 2>&1; then
        echo "   ✅ SSH key installed on Beast"
        
        # Test connection
        if ssh -o BatchMode=yes -o ConnectTimeout=5 xava@${BEAST_IP} echo "Connection OK" >/dev/null 2>&1; then
            echo "   ✅ Passwordless SSH verified"
        else
            echo "   ⚠️  SSH key installed but connection test failed"
        fi
    else
        echo "   ❌ Failed to install SSH key on Beast"
    fi
else
    echo "   ⚠️  Beast not reachable at ${BEAST_IP}"
    echo "   Scanning network for Beast..."
    
    # Try to find Beast by scanning common IPs
    for ip in 192.168.1.{100..110}; do
        if ping -c 1 -W 1 $ip >/dev/null 2>&1; then
            hostname=$(ssh -o ConnectTimeout=2 -o BatchMode=no xava@${ip} hostname 2>/dev/null || echo "unknown")
            if [[ "$hostname" == *"beast"* ]]; then
                echo "   ✅ Found Beast at ${ip}"
                BEAST_IP=$ip
                echo "   Installing SSH key..."
                ssh-copy-id -o ConnectTimeout=10 xava@${BEAST_IP}
                break
            fi
        fi
    done
fi
echo

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Setup Complete - Verifying Connections"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test Sloth
if ssh -o BatchMode=yes -o ConnectTimeout=5 xava@192.168.1.102 echo "OK" >/dev/null 2>&1; then
    echo "✅ Sloth (192.168.1.102) - Connected"
else
    echo "❌ Sloth (192.168.1.102) - Connection failed"
fi

# Test Beast
if ssh -o BatchMode=yes -o ConnectTimeout=5 xava@${BEAST_IP} echo "OK" >/dev/null 2>&1; then
    echo "✅ Beast (${BEAST_IP}) - Connected"
else
    echo "❌ Beast (${BEAST_IP}) - Connection failed"
fi

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 Next Steps:"
echo "   1. Run: python3 backend/setup_cluster.py"
echo "   2. Test executor with discovered IPs"
echo "   3. Start distributed execution!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
