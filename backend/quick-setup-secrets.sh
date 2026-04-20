#!/bin/bash
# Quick start script - opens vault and waits for you to save secrets

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$REPO_ROOT/.env.email"
VAULT_HTML="$REPO_ROOT/secrets-vault.html"

echo "🔐 Queztl Secrets Vault - Quick Setup"
echo "======================================"
echo ""
echo "Opening secrets vault in your browser..."
echo ""

# Open the vault
open "$VAULT_HTML"

echo "📋 Instructions:"
echo ""
echo "1. Get your SendGrid API key:"
echo "   → https://app.sendgrid.com/settings/api_keys"
echo "   → Create API Key → Full Access"
echo ""
echo "2. Paste it into the vault and click 'Save Secrets'"
echo ""
echo "3. Click 'Export .env' to download the file"
echo ""
echo "4. Come back here and press Enter when done..."
echo ""
read -r -p "Press Enter after saving your secrets in the vault..."

# Check if .env.email was downloaded
if [ -f "$HOME/Downloads/.env.email" ]; then
    echo ""
    echo "✅ Found .env.email in Downloads!"
    echo "📁 Moving it to project..."
    mv "$HOME/Downloads/.env.email" "$ENV_FILE"
    echo "✅ Moved to: $ENV_FILE"
else
    echo ""
    echo "⚠️  Couldn't find .env.email in Downloads"
    echo "📁 Looking for it elsewhere..."

    # Search common download locations
    for location in "$HOME/Downloads" "$HOME/Desktop" "$REPO_ROOT"; do
        if [ -f "$location/.env.email" ]; then
            echo "✅ Found at: $location/.env.email"
            if [ "$location" != "$REPO_ROOT" ]; then
                mv "$location/.env.email" "$ENV_FILE"
                echo "✅ Moved to project folder"
            fi
            break
        fi
    done
fi

echo ""
echo "🚀 Next Steps:"
echo ""
echo "Option 1 - Test Locally:"
echo "  ./setup-sendgrid.sh"
echo ""
echo "Option 2 - Deploy to Cloud:"
echo "  ./deploy-email-cloud.sh"
echo ""
echo "Your secrets are encrypted and stored securely! 🔒"
