#!/bin/bash
# Quick deploy to Railway

echo "🚀 Deploying Queztl Email Backend to Railway"
echo "=============================================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm i -g @railway/cli
fi

echo "Step 1: Login to Railway"
railway login

echo ""
echo "Step 2: Create new project"
railway init

echo ""
echo "Step 3: Link to repository"
railway link

echo ""
echo "Step 4: Set environment variables"
echo "Enter your SendGrid API Key:"
read -sp "> " SENDGRID_KEY
railway variables set SENDGRID_API_KEY="$SENDGRID_KEY"
railway variables set FROM_EMAIL="salvador@senasaitech.com"
railway variables set FROM_NAME="Salvador Sena - Queztl"

echo ""
echo ""
echo "Step 5: Deploy!"
railway up

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Get your URL:"
railway domain

echo ""
echo "Update your email UI with this URL and redeploy to Netlify."
