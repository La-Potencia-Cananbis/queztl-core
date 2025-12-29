#!/bin/bash
# 🚀 Deploy Queztl Email System
set -e

echo "🚀 Deploying Queztl Email System to Netlify"
echo "============================================"

# Check if we're in the right directory
if [ ! -d "email-app" ]; then
    echo "❌ Error: email-app directory not found"
    exit 1
fi

cd email-app

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Build the app
echo "🔨 Building Next.js app..."
npm run build

# Deploy to Netlify
echo "🌐 Deploying to Netlify..."
if command -v netlify &> /dev/null; then
    netlify deploy --prod --dir=out --site=senasaitech
else
    echo "⚠️  Netlify CLI not found. Install with: npm install -g netlify-cli"
    echo "💡 Or manually deploy the 'out' directory to Netlify"
    exit 1
fi

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your email app is live at: https://senasaitech.netlify.app"
echo ""
echo "Next steps:"
echo "1. Start the backend: python3 backend/email_service.py"
echo "2. Update NEXT_PUBLIC_API_URL in netlify.toml with your backend URL"
echo "3. Test sending emails through the interface"
