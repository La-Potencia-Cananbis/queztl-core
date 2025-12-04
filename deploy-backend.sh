#!/bin/bash

echo "🦅 Queztl-Core Deployment Helper"
echo "=================================="
echo ""

# Check if git repo exists
if [ ! -d .git ]; then
    echo "❌ Not a git repository. Run 'git init' first."
    exit 1
fi

# Check if remote exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "📝 No GitHub remote found."
    echo ""
    echo "Please create a GitHub repository and add it as remote:"
    echo ""
    echo "  1. Go to https://github.com/new"
    echo "  2. Create repository named 'queztl-core'"
    echo "  3. Run:"
    echo ""
    echo "     git remote add origin https://github.com/YOUR_USERNAME/queztl-core.git"
    echo "     git branch -M main"
    echo "     git push -u origin main"
    echo ""
    exit 1
fi

echo "✅ Git repository configured"
echo ""

# Check for uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo "📝 Uncommitted changes detected. Committing..."
    git add .
    git commit -m "Update $(date +%Y-%m-%d)"
    echo "✅ Changes committed"
else
    echo "✅ No uncommitted changes"
fi

echo ""
echo "🚀 Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 Next Steps:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1. Deploy Backend to Render:"
    echo "   → Go to: https://render.com"
    echo "   → Click 'New +' → 'Blueprint'"
    echo "   → Connect your GitHub repo"
    echo "   → Render will auto-deploy using render.yaml"
    echo ""
    echo "2. Get your backend URL:"
    echo "   → Wait for deployment (~5 min)"
    echo "   → Copy URL from Render dashboard"
    echo "   → Example: https://queztl-core-backend.onrender.com"
    echo ""
    echo "3. Update frontend:"
    echo "   → Edit dashboard/.env.production"
    echo "   → Set: NEXT_PUBLIC_API_URL=https://YOUR-BACKEND-URL"
    echo "   → Run: netlify deploy --prod"
    echo ""
    echo "4. Test everything:"
    echo "   → Visit: https://senzeni.netlify.app"
    echo "   → Try power measurement and stress tests!"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📚 Full guide: cat RENDER_DEPLOY.md"
    echo ""
else
    echo ""
    echo "❌ Push failed. Check your GitHub credentials."
    exit 1
fi
