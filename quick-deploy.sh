#!/usr/bin/env bash
# Quick Deploy - Get Your Site Live NOW

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  Emergency Site Deploy - NM Socialists Working Site          ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo

# Check if NM site exists
if [ ! -d ~/Documents/NM\ Socialists/optimized-site ]; then
    echo "❌ NM Socialists site not found"
    echo "   Expected: ~/Documents/NM Socialists/optimized-site/"
    exit 1
fi

echo "✅ Found NM Socialists site"
echo

# Choice menu
echo "What would you like to do?"
echo
echo "1) Deploy NM Socialists site as-is (FASTEST)"
echo "2) Copy to queztl-core and customize"
echo "3) Just show me what's there"
echo
read -p "Choice [1-3]: " choice

case $choice in
    1)
        echo
        echo "🚀 Deploying NM Socialists site..."
        echo
        cd ~/Documents/NM\ Socialists/optimized-site/
        
        # Check if netlify cli exists
        if ! command -v netlify &> /dev/null; then
            echo "Installing Netlify CLI..."
            npm install -g netlify-cli
        fi
        
        echo "📦 Running netlify deploy --prod"
        echo
        netlify deploy --prod
        
        echo
        echo "✅ Site deployed!"
        echo "   Your site should now be live"
        echo
        ;;
        
    2)
        echo
        echo "📋 Copying site to queztl-core..."
        echo
        
        # Backup old frontend
        if [ -d ~/queztl-core/frontend ]; then
            echo "   Backing up old frontend..."
            mv ~/queztl-core/frontend ~/queztl-core/frontend-backup-$(date +%Y%m%d-%H%M%S)
        fi
        
        # Copy NM site
        echo "   Copying NM Socialists site..."
        cp -r ~/Documents/NM\ Socialists/optimized-site ~/queztl-core/frontend
        
        echo
        echo "✅ Site copied to ~/queztl-core/frontend"
        echo
        echo "📝 Next steps:"
        echo "   1. Edit frontend/index.html (change branding)"
        echo "   2. Update frontend/assets/js/main.js (add API calls)"
        echo "   3. Deploy: cd frontend && netlify deploy --prod"
        echo
        ;;
        
    3)
        echo
        echo "📊 NM Socialists Site Status:"
        echo
        echo "Location: ~/Documents/NM Socialists/optimized-site/"
        echo
        echo "Files:"
        ls -lh ~/Documents/NM\ Socialists/optimized-site/ | grep -E "index.html|README"
        echo
        echo "Memes:"
        echo "  Count: $(ls ~/Documents/NM\ Socialists/optimized-site/assets/img/*.png 2>/dev/null | wc -l | xargs)"
        echo
        echo "Features:"
        echo "  ✅ Meme rotation (weekly)"
        echo "  ✅ Responsive design"
        echo "  ✅ Image optimization"
        echo "  ✅ Netlify ready"
        echo
        echo "To deploy: cd ~/Documents/NM\ Socialists/optimized-site/ && netlify deploy --prod"
        echo
        ;;
        
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo
echo "╚═══════════════════════════════════════════════════════════════╝"
