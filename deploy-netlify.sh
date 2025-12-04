#!/bin/bash

echo "🚀 Deploying Hive Dashboard to Netlify"
echo "========================================"
echo ""

# Check if netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "📦 Netlify CLI not found. Installing..."
    npm install -g netlify-cli
fi

echo "📁 Building dashboard..."
cd dashboard

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Build the project
echo "🔨 Building Next.js application..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"
echo ""

# Deploy
echo "🌐 Deploying to Netlify..."
netlify deploy --prod

echo ""
echo "========================================"
echo "✅ Deployment complete!"
echo ""
echo "🌍 Your site is live at: https://senzeni.netlify.app"
echo "📊 Dashboard: https://app.netlify.com"
echo ""
echo "⚠️  Remember to:"
echo "   1. Set NEXT_PUBLIC_API_URL in Netlify environment variables"
echo "   2. Deploy your backend API to a hosting service"
echo "   3. Update CORS settings in backend to allow your Netlify domain"
echo "========================================"
