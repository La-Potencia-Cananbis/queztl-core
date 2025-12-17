#!/bin/bash
# 🌐 Quick Web Deployment Script for Queztl-Core 3DMark Benchmark

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🦅 QUEZTL-CORE WEB DEPLOYMENT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display menu
show_menu() {
    echo "Select deployment option:"
    echo ""
    echo "  1) Deploy to GitHub Pages (FREE)"
    echo "  2) Deploy to Netlify (FREE, Auto-deploy)"
    echo "  3) Deploy to Vercel (FREE)"
    echo "  4) Test locally (open in browser)"
    echo "  5) Generate standalone HTML (portable)"
    echo "  6) Exit"
    echo ""
}

# Function to deploy to GitHub Pages
deploy_github_pages() {
    echo -e "${BLUE}🚀 Deploying to GitHub Pages...${NC}"
    echo ""
    
    # Check if gh-pages branch exists
    if git show-ref --verify --quiet refs/heads/gh-pages; then
        echo "✅ gh-pages branch exists"
        git checkout gh-pages
    else
        echo "Creating gh-pages branch..."
        git checkout -b gh-pages
    fi
    
    # Copy benchmark to root
    cp dashboard/public/3dmark-benchmark.html index.html
    
    # Commit and push
    git add index.html
    git commit -m "Deploy 3DMark benchmark to GitHub Pages"
    git push origin gh-pages
    
    echo ""
    echo -e "${GREEN}✅ Deployed to GitHub Pages!${NC}"
    echo ""
    echo "Your benchmark will be available at:"
    echo "https://$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/' | awk -F'/' '{print $1".github.io/"$2}')/"
    echo ""
    echo "⚠️  Note: Enable GitHub Pages in Settings > Pages > Source: gh-pages branch"
    
    # Go back to main branch
    git checkout main
}

# Function to deploy to Netlify
deploy_netlify() {
    echo -e "${BLUE}🚀 Deploying to Netlify...${NC}"
    echo ""
    
    # Check if netlify CLI is installed
    if ! command -v netlify &> /dev/null; then
        echo "Installing Netlify CLI..."
        npm install -g netlify-cli
    fi
    
    # Deploy
    cd dashboard/public
    netlify deploy --prod
    cd ../..
    
    echo ""
    echo -e "${GREEN}✅ Deployed to Netlify!${NC}"
}

# Function to deploy to Vercel
deploy_vercel() {
    echo -e "${BLUE}🚀 Deploying to Vercel...${NC}"
    echo ""
    
    # Check if vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
        echo "Installing Vercel CLI..."
        npm install -g vercel
    fi
    
    # Deploy
    cd dashboard/public
    vercel --prod
    cd ../..
    
    echo ""
    echo -e "${GREEN}✅ Deployed to Vercel!${NC}"
}

# Function to test locally
test_local() {
    echo -e "${BLUE}🧪 Testing locally...${NC}"
    echo ""
    
    FILE="dashboard/public/3dmark-benchmark.html"
    
    # Detect OS and open browser
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open "$FILE"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        xdg-open "$FILE"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        # Windows
        start "$FILE"
    else
        echo "Could not detect OS. Please open manually:"
        echo "$(pwd)/$FILE"
    fi
    
    echo -e "${GREEN}✅ Opening in browser...${NC}"
    echo ""
    echo "💡 Tips:"
    echo "   - Make sure backend is running: docker-compose up -d"
    echo "   - Or set API URL to production: https://queztl-core-api.onrender.com"
}

# Function to generate standalone HTML
generate_standalone() {
    echo -e "${BLUE}📦 Generating standalone HTML...${NC}"
    echo ""
    
    # Copy to a standalone file
    cp dashboard/public/3dmark-benchmark.html queztl-3dmark-standalone.html
    
    echo -e "${GREEN}✅ Generated: queztl-3dmark-standalone.html${NC}"
    echo ""
    echo "You can:"
    echo "   1. Email this file to anyone"
    echo "   2. Upload to any web host"
    echo "   3. Open directly in browser"
    echo "   4. Share via Dropbox/Google Drive"
    echo ""
    echo "File location: $(pwd)/queztl-3dmark-standalone.html"
}

# Main loop
while true; do
    show_menu
    read -p "Enter choice [1-6]: " choice
    echo ""
    
    case $choice in
        1)
            deploy_github_pages
            ;;
        2)
            deploy_netlify
            ;;
        3)
            deploy_vercel
            ;;
        4)
            test_local
            ;;
        5)
            generate_standalone
            ;;
        6)
            echo "Goodbye! 👋"
            exit 0
            ;;
        *)
            echo -e "${YELLOW}Invalid choice. Please enter 1-6.${NC}"
            echo ""
            ;;
    esac
    
    read -p "Press Enter to continue..."
    clear
done
