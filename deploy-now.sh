#!/bin/bash
# One-command deployment script for NM Socialists site
# Usage: ./deploy-now.sh

set -e  # Exit on error

echo "🚀 QUEZTL DEPLOY - Getting Your Site Live NOW"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if NM site exists
NM_SITE="$HOME/Documents/NM Socialists/optimized-site"
if [ ! -d "$NM_SITE" ]; then
    echo -e "${RED}❌ ERROR: NM Socialists site not found at:${NC}"
    echo "   $NM_SITE"
    echo ""
    echo "Looking for the site..."
    find "$HOME/Documents" -name "optimized-site" -type d 2>/dev/null | head -5
    exit 1
fi

echo -e "${GREEN}✅ Found NM Socialists site${NC}"
echo ""

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo -e "${YELLOW}⚠️  Netlify CLI not installed${NC}"
    echo ""
    echo "Installing Netlify CLI..."
    npm install -g netlify-cli
    echo ""
fi

# Navigate to site
cd "$NM_SITE"
echo -e "${GREEN}📁 Current directory:${NC} $PWD"
echo ""

# Check if already logged in
if ! netlify status &> /dev/null; then
    echo -e "${YELLOW}🔐 Netlify login required${NC}"
    echo ""
    echo "Opening browser for authentication..."
    netlify login
    echo ""
fi

# Show site info
echo -e "${GREEN}📋 Site Preview:${NC}"
echo "   - 19 memes with weekly rotation"
echo "   - Responsive design"
echo "   - Download & share buttons"
echo "   - Professional GPT-4 design"
echo ""

# Ask for confirmation
echo -e "${YELLOW}Ready to deploy to production?${NC}"
echo ""
read -p "Type 'yes' to deploy now: " confirm

if [ "$confirm" != "yes" ]; then
    echo ""
    echo -e "${RED}❌ Deployment cancelled${NC}"
    echo ""
    echo "To deploy later, run:"
    echo "   cd '$NM_SITE'"
    echo "   netlify deploy --prod"
    exit 0
fi

echo ""
echo -e "${GREEN}🚀 Deploying to production...${NC}"
echo ""

# Deploy
netlify deploy --prod

# Check if successful
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ DEPLOYMENT SUCCESSFUL!${NC}"
    echo ""
    echo "Your site is now live! 🎉"
    echo ""
    echo "Next steps:"
    echo "  1. Test the meme rotation (changes weekly)"
    echo "  2. Share the URL!"
    echo "  3. Check Render for backend status"
    echo ""
    echo "To customize or rebrand:"
    echo "  ~/queztl-core/quick-deploy.sh (option 2)"
else
    echo ""
    echo -e "${RED}❌ Deployment failed${NC}"
    echo ""
    echo "Try manual deployment:"
    echo "  cd '$NM_SITE'"
    echo "  netlify deploy --prod"
    exit 1
fi
