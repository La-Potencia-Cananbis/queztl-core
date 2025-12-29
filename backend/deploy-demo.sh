#!/bin/bash
# 🚀 Deploy Queztl OS Demo to Workers
# This deploys the interactive demo GUI to your distributed worker infrastructure

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🦅 QUEZTL OS DEMO DEPLOYMENT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if demo file exists
if [ ! -f "queztl_os_demo.html" ]; then
    echo -e "${RED}❌ Error: queztl_os_demo.html not found${NC}"
    exit 1
fi

# Function to deploy to Netlify
deploy_netlify() {
    echo -e "${BLUE}🚀 Deploying to Netlify...${NC}"
    echo ""
    
    # Create temporary directory for deployment
    TEMP_DIR=$(mktemp -d)
    cp queztl_os_demo.html "$TEMP_DIR/index.html"
    
    # Create netlify.toml
    cat > "$TEMP_DIR/netlify.toml" << 'EOF'
[build]
  publish = "."

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
EOF
    
    # Deploy
    cd "$TEMP_DIR"
    
    if command -v netlify &> /dev/null; then
        netlify deploy --prod --dir .
        echo ""
        echo -e "${GREEN}✅ Deployed to Netlify!${NC}"
    else
        echo -e "${YELLOW}⚠️  Netlify CLI not installed${NC}"
        echo "Install with: npm install -g netlify-cli"
        echo "Then run: netlify login && netlify deploy --prod --dir $TEMP_DIR"
    fi
    
    # Cleanup
    cd -
    rm -rf "$TEMP_DIR"
}

# Function to deploy to Vercel
deploy_vercel() {
    echo -e "${BLUE}🚀 Deploying to Vercel...${NC}"
    echo ""
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    cp queztl_os_demo.html "$TEMP_DIR/index.html"
    
    # Create vercel.json
    cat > "$TEMP_DIR/vercel.json" << 'EOF'
{
  "version": 2,
  "builds": [
    {
      "src": "index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
EOF
    
    cd "$TEMP_DIR"
    
    if command -v vercel &> /dev/null; then
        vercel --prod
        echo ""
        echo -e "${GREEN}✅ Deployed to Vercel!${NC}"
    else
        echo -e "${YELLOW}⚠️  Vercel CLI not installed${NC}"
        echo "Install with: npm install -g vercel"
        echo "Then run: cd $TEMP_DIR && vercel --prod"
    fi
    
    cd -
    rm -rf "$TEMP_DIR"
}

# Function to deploy to GitHub Pages
deploy_github_pages() {
    echo -e "${BLUE}🚀 Deploying to GitHub Pages...${NC}"
    echo ""
    
    # Check if gh-pages branch exists
    if git show-ref --verify --quiet refs/heads/gh-pages; then
        git checkout gh-pages
    else
        git checkout -b gh-pages
    fi
    
    # Copy demo to root
    cp queztl_os_demo.html index.html
    
    # Commit and push
    git add index.html
    git commit -m "Deploy Queztl OS Demo to GitHub Pages" || true
    git push origin gh-pages --force
    
    # Switch back to main
    git checkout main
    
    echo ""
    echo -e "${GREEN}✅ Deployed to GitHub Pages!${NC}"
    echo "Your demo will be available at:"
    echo "https://$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/' | awk -F'/' '{print tolower($1)}'}.github.io/$(git config --get remote.origin.url | sed 's/.*\/\(.*\)\.git/\1/')"
}

# Function to start local server
deploy_local() {
    echo -e "${BLUE}🚀 Starting local server...${NC}"
    echo ""
    
    PORT=8080
    
    echo -e "${GREEN}✅ Demo running at: http://localhost:$PORT/queztl_os_demo.html${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
    echo ""
    
    python3 -m http.server $PORT
}

# Function to deploy to custom worker
deploy_worker() {
    echo -e "${BLUE}🚀 Deploying to Queztl Workers...${NC}"
    echo ""
    
    # Check if hive-control exists
    if [ -f "./hive-control" ]; then
        echo "Using hive-control to deploy..."
        ./hive-control status
        
        # TODO: Implement actual worker deployment
        echo -e "${YELLOW}⚠️  Worker deployment not yet implemented${NC}"
        echo "For now, use one of the other deployment options."
    else
        echo -e "${RED}❌ hive-control not found${NC}"
        echo "Falling back to local deployment..."
        deploy_local
    fi
}

# Show menu
echo "Select deployment target:"
echo ""
echo "  1) Local server (http://localhost:8080)"
echo "  2) Netlify (auto-deploy, free)"
echo "  3) Vercel (auto-deploy, free)"
echo "  4) GitHub Pages (free)"
echo "  5) Queztl Workers (distributed)"
echo "  6) Exit"
echo ""
read -p "Enter choice [1-6]: " choice

case $choice in
    1)
        deploy_local
        ;;
    2)
        deploy_netlify
        ;;
    3)
        deploy_vercel
        ;;
    4)
        deploy_github_pages
        ;;
    5)
        deploy_worker
        ;;
    6)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
