#!/bin/bash

# 🦅 Queztl-Core 3DMark Standalone Deployment Script
# This script helps you deploy the benchmark to various platforms

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🦅 Queztl-Core 3DMark Standalone Deployment"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "This benchmark can be deployed anywhere to test any Queztl-Core API"
echo ""
echo "Choose deployment option:"
echo "  1) 🌐 GitHub Pages (free, easy)"
echo "  2) ☁️  Netlify (free, auto-deploy)"
echo "  3) ⚡ Vercel (free, fast)"
echo "  4) 🏠 Local Test Server (Python)"
echo "  5) 📦 Create Standalone Package"
echo "  6) ℹ️  Show Info Only"
echo ""
read -p "Enter choice [1-6]: " choice

case $choice in
  1)
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🌐 GitHub Pages Deployment"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Check if git repo exists
    if [ ! -d ".git" ]; then
      echo "❌ Error: Not a git repository"
      echo "   Run: git init"
      exit 1
    fi
    
    # Create gh-pages branch
    echo "📝 Creating gh-pages branch..."
    git checkout -b gh-pages 2>/dev/null || git checkout gh-pages
    
    # Copy benchmark file
    echo "📦 Copying benchmark file..."
    cp dashboard/public/3dmark-benchmark.html index.html
    
    # Create README
    cat > README.md << 'EOF'
# Queztl-Core 3DMark Benchmark

Professional GPU benchmark suite for testing Queztl-Core API performance.

## Quick Start

1. Open: [3DMark Benchmark](https://yourusername.github.io/repo-name/)
2. Enter your API URL
3. Click "Test Connection"
4. Click "RUN ALL BENCHMARKS"
5. View results (expected Grade A)

## Configuration

The benchmark includes preset endpoints:
- 🏠 Localhost: `http://localhost:8000`
- ☁️ Production: Your production API URL
- 🐝 Custom: Enter any Queztl-Core API endpoint

## Documentation

See [3DMARK_STANDALONE_GUIDE.md](./3DMARK_STANDALONE_GUIDE.md) for full docs.
EOF
    
    # Commit
    echo "💾 Committing changes..."
    git add index.html README.md
    git commit -m "Deploy 3DMark benchmark to GitHub Pages" || true
    
    echo ""
    echo "✅ Ready to push!"
    echo ""
    echo "Next steps:"
    echo "  1. Push: git push origin gh-pages"
    echo "  2. Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/settings/pages"
    echo "  3. Set source to: gh-pages branch"
    echo "  4. Access at: https://YOUR_USERNAME.github.io/YOUR_REPO/"
    echo ""
    ;;
    
  2)
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "☁️  Netlify Deployment"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Check if netlify CLI is installed
    if ! command -v netlify &> /dev/null; then
      echo "📦 Installing Netlify CLI..."
      npm install -g netlify-cli
    fi
    
    # Create temp directory
    mkdir -p .deploy-temp
    cp dashboard/public/3dmark-benchmark.html .deploy-temp/index.html
    
    # Deploy
    echo "🚀 Deploying to Netlify..."
    cd .deploy-temp
    netlify deploy --prod --dir=.
    
    echo ""
    echo "✅ Deployed to Netlify!"
    echo "   Copy the URL shown above to access your benchmark"
    echo ""
    
    # Cleanup
    cd ..
    rm -rf .deploy-temp
    ;;
    
  3)
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚡ Vercel Deployment"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Check if vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
      echo "📦 Installing Vercel CLI..."
      npm install -g vercel
    fi
    
    # Create temp directory
    mkdir -p .deploy-temp
    cp dashboard/public/3dmark-benchmark.html .deploy-temp/index.html
    
    # Deploy
    echo "🚀 Deploying to Vercel..."
    cd .deploy-temp
    vercel --prod
    
    echo ""
    echo "✅ Deployed to Vercel!"
    echo "   Copy the URL shown above to access your benchmark"
    echo ""
    
    # Cleanup
    cd ..
    rm -rf .deploy-temp
    ;;
    
  4)
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🏠 Local Test Server"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Starting local server on port 3001..."
    echo ""
    echo "Access benchmark at:"
    echo "  👉 http://localhost:3001/3dmark-benchmark.html"
    echo ""
    echo "Press Ctrl+C to stop server"
    echo ""
    
    cd dashboard/public
    python3 -m http.server 3001
    ;;
    
  5)
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📦 Creating Standalone Package"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Create package directory
    PACKAGE_DIR="queztl-3dmark-standalone"
    mkdir -p "$PACKAGE_DIR"
    
    # Copy files
    cp dashboard/public/3dmark-benchmark.html "$PACKAGE_DIR/index.html"
    
    # Create README
    cat > "$PACKAGE_DIR/README.md" << 'EOF'
# Queztl-Core 3DMark Benchmark - Standalone Package

## What's Inside

- `index.html` - The complete benchmark (open in browser)

## How to Use

### Option 1: Open Directly (may have CORS issues)
```bash
# Mac
open index.html

# Windows
start index.html

# Linux
xdg-open index.html
```

### Option 2: Use Local Server (recommended)
```bash
# Python 3
python3 -m http.server 3001
# Then open: http://localhost:3001

# Node.js
npx http-server -p 3001
# Then open: http://localhost:3001

# PHP
php -S localhost:3001
# Then open: http://localhost:3001
```

### Option 3: Deploy to Web Host

Upload `index.html` to any web host:
- GitHub Pages
- Netlify
- Vercel
- AWS S3
- Your own server

## Configuration

1. Open the benchmark in browser
2. Enter your Queztl-Core API URL
3. Click "Test Connection"
4. Click "RUN ALL BENCHMARKS"

Presets available:
- 🏠 Localhost: `http://localhost:8000`
- ☁️ Production: Your deployed API
- 🐝 Custom: Any Queztl-Core instance

## Troubleshooting

**"Cannot reach API"**
- Make sure your API is running
- Check CORS is enabled on API
- Verify URL is correct

**CORS Errors**
- Don't use `file://` protocol
- Use a local web server
- Or deploy to actual web host

## Support

See full documentation in main repo:
- 3DMARK_STANDALONE_GUIDE.md
- 3DMARK_BENCHMARK_GUIDE.md

---

Built with ❤️ by Queztl-Core Team
EOF
    
    # Create zip
    ZIP_NAME="queztl-3dmark-standalone-$(date +%Y%m%d).zip"
    zip -r "$ZIP_NAME" "$PACKAGE_DIR"
    
    echo "✅ Package created!"
    echo ""
    echo "📦 Files:"
    echo "   - $PACKAGE_DIR/index.html"
    echo "   - $PACKAGE_DIR/README.md"
    echo "   - $ZIP_NAME"
    echo ""
    echo "🎁 Share this package:"
    echo "   - Email to clients"
    echo "   - Upload to file share"
    echo "   - Distribute on USB drives"
    echo "   - Post on GitHub Releases"
    echo ""
    echo "Recipients can:"
    echo "   1. Extract the zip"
    echo "   2. Open index.html"
    echo "   3. Test YOUR API"
    echo "   4. See performance results"
    echo ""
    ;;
    
  6)
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "ℹ️  Deployment Information"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📍 Benchmark Location:"
    echo "   dashboard/public/3dmark-benchmark.html"
    echo ""
    echo "🎯 What It Does:"
    echo "   - Standalone HTML file (no dependencies)"
    echo "   - Tests ANY Queztl-Core API"
    echo "   - Can be hosted ANYWHERE"
    echo "   - Like real 3DMark, but for your API"
    echo ""
    echo "🌐 Deployment Options:"
    echo ""
    echo "   1. GitHub Pages (free)"
    echo "      - Create gh-pages branch"
    echo "      - Copy file as index.html"
    echo "      - Enable Pages in settings"
    echo ""
    echo "   2. Netlify (free, auto-deploy)"
    echo "      - netlify deploy --dir=dashboard/public"
    echo "      - Or connect GitHub repo"
    echo ""
    echo "   3. Vercel (free, fast)"
    echo "      - vercel dashboard/public"
    echo "      - Or connect GitHub repo"
    echo ""
    echo "   4. Local Testing"
    echo "      - python3 -m http.server 3001"
    echo "      - Open localhost:3001"
    echo ""
    echo "   5. AWS S3 Static Website"
    echo "      - Upload to S3 bucket"
    echo "      - Enable static hosting"
    echo ""
    echo "📖 Full Guide:"
    echo "   See: 3DMARK_STANDALONE_GUIDE.md"
    echo ""
    echo "🚀 Quick Test:"
    echo "   1. Run: ./deploy-benchmark.sh"
    echo "   2. Choose option 4 (Local Server)"
    echo "   3. Open: http://localhost:3001/3dmark-benchmark.html"
    echo "   4. Select: 🏠 Localhost"
    echo "   5. Click: 🔌 Test Connection"
    echo "   6. Click: 🚀 RUN ALL BENCHMARKS"
    echo ""
    ;;
    
  *)
    echo "❌ Invalid choice"
    exit 1
    ;;
esac

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Done!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
