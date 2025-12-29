#!/bin/bash
# Deploy Queztl Email System - Complete Setup

echo "🚀 Queztl Email - Full Cloud Deployment"
echo "========================================"
echo ""
echo "This will deploy your email system so you can access it from anywhere."
echo ""
echo "Choose deployment method:"
echo ""
echo "1) Railway (Easiest - Web UI, no CLI)"
echo "2) Render (Reliable - Web UI, no CLI)"
echo "3) Exit"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "📦 Railway Deployment"
        echo "===================="
        echo ""
        echo "1. Open: https://railway.app/"
        echo "2. Click 'Start a New Project'"
        echo "3. Select 'Deploy from GitHub repo'"
        echo "4. Choose: SalChicanoLoco/queztl-core"
        echo "5. Add these environment variables:"
        echo ""
        echo "   SENDGRID_API_KEY = (your SendGrid key)"
        echo "   FROM_EMAIL = salvador@senasaitech.com"
        echo "   FROM_NAME = Salvador Sena - Queztl"
        echo ""
        echo "6. Settings → Update start command:"
        echo "   cd backend && uvicorn email_service:app --host 0.0.0.0 --port \$PORT"
        echo ""
        echo "7. Deploy!"
        echo ""
        echo "8. Copy the URL (e.g., queztl-email.railway.app)"
        echo ""
        read -p "Press Enter to open Railway..." 
        open "https://railway.app/"
        echo ""
        echo "Once deployed, paste your backend URL here:"
        read -p "> " BACKEND_URL
        ;;
    2)
        echo ""
        echo "📦 Render Deployment"
        echo "==================="
        echo ""
        echo "1. Open: https://render.com/"
        echo "2. New → Web Service"
        echo "3. Connect GitHub → queztl-core"
        echo "4. Settings:"
        echo "   - Name: queztl-email"
        echo "   - Environment: Python 3"
        echo "   - Build Command: pip install -r backend/requirements.txt"
        echo "   - Start Command: cd backend && uvicorn email_service:app --host 0.0.0.0 --port \$PORT"
        echo ""
        echo "5. Add environment variables (same as Railway)"
        echo "6. Create Web Service"
        echo ""
        echo "7. Copy the URL (e.g., queztl-email.onrender.com)"
        echo ""
        read -p "Press Enter to open Render..." 
        open "https://render.com/"
        echo ""
        echo "Once deployed, paste your backend URL here:"
        read -p "> " BACKEND_URL
        ;;
    3)
        echo "Exiting..."
        exit 0
        ;;
esac

if [ -n "$BACKEND_URL" ]; then
    echo ""
    echo "✅ Updating email UI..."
    
    # Update my-email.html with new backend URL
    sed -i '' "s|http://localhost:8001|https://$BACKEND_URL|g" my-email.html
    
    # Copy to netlify public folder
    cp my-email.html email-landing.html netlify.toml .
    
    echo "✅ Files updated!"
    echo ""
    echo "📤 Deploy to Netlify:"
    echo "1. Drag & drop 'my-email.html' to Netlify"
    echo "2. Or run: netlify deploy --prod --dir=."
    echo ""
    echo "Your email UI will be live at:"
    echo "https://senasaitech.com/my-email.html"
    echo ""
fi

echo ""
echo "✅ Setup complete!"
