#!/bin/bash
# Quick start script - opens vault and waits for you to save secrets

echo "🔐 Queztl Secrets Vault - Quick Setup"
echo "======================================"
echo ""
echo "Opening secrets vault in your browser..."
echo ""

# Open the vault
open /Users/xavasena/hive/secrets-vault.html

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
read -p "Press Enter after saving your secrets in the vault..."

# Check if .env.email was downloaded
if [ -f "$HOME/Downloads/.env.email" ]; then
    echo ""
    echo "✅ Found .env.email in Downloads!"
    echo "📁 Moving it to project..."
    mv "$HOME/Downloads/.env.email" /Users/xavasena/hive/.env.email
    echo "✅ Moved to: /Users/xavasena/hive/.env.email"
else
    echo ""
    echo "⚠️  Couldn't find .env.email in Downloads"
    echo "📁 Looking for it elsewhere..."
    
    # Search common download locations
    for location in "$HOME/Downloads" "$HOME/Desktop" "/Users/xavasena/hive"; do
        if [ -f "$location/.env.email" ]; then
            echo "✅ Found at: $location/.env.email"
            if [ "$location" != "/Users/xavasena/hive" ]; then
                mv "$location/.env.email" /Users/xavasena/hive/.env.email
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
