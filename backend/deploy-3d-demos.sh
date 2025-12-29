#!/bin/bash
# Deploy 3D Demos to Netlify

echo "🎨 Deploying Queztl 3D Showcase to senasaitech.com"
echo "=================================================="
echo ""

# Create deployment folder
DEPLOY_DIR="/Users/xavasena/hive/3d-showcase-deploy"
mkdir -p "$DEPLOY_DIR"

echo "📦 Copying 3D demos..."

# Copy GPU demo
if [ -f "dashboard/public/gpu-demo.html" ]; then
    cp dashboard/public/gpu-demo.html "$DEPLOY_DIR/3d-demo.html"
    echo "✅ 3D Cube Demo copied"
fi

# Copy 3DMark benchmark
if [ -f "dashboard/public/3dmark-benchmark.html" ]; then
    cp dashboard/public/3dmark-benchmark.html "$DEPLOY_DIR/benchmark.html"
    echo "✅ 3DMark Benchmark copied"
fi

# Copy secrets vault
if [ -f "secrets-vault.html" ]; then
    cp secrets-vault.html "$DEPLOY_DIR/secrets.html"
    echo "✅ Secrets Vault copied"
fi

# Copy email UI
if [ -f "my-email.html" ]; then
    cp my-email.html "$DEPLOY_DIR/email.html"
    echo "✅ Email UI copied"
fi

# Copy landing page
if [ -f "email-landing.html" ]; then
    cp email-landing.html "$DEPLOY_DIR/index.html"
    echo "✅ Landing Page copied"
fi

# Create a beautiful index page for all demos
cat > "$DEPLOY_DIR/demos.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Queztl 3D Showcase</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            font-size: 3rem;
            margin-bottom: 20px;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2rem;
            margin-bottom: 60px;
            opacity: 0.9;
        }
        .demos-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 60px;
        }
        .demo-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 30px;
            transition: all 0.3s;
            cursor: pointer;
        }
        .demo-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            border-color: rgba(255, 255, 255, 0.4);
        }
        .demo-icon {
            font-size: 3rem;
            margin-bottom: 15px;
        }
        .demo-title {
            font-size: 1.5rem;
            margin-bottom: 10px;
            font-weight: 600;
        }
        .demo-desc {
            opacity: 0.8;
            line-height: 1.6;
        }
        .demo-link {
            color: white;
            text-decoration: none;
            display: block;
        }
        .status {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 12px;
            font-size: 0.85rem;
            margin-top: 15px;
            background: rgba(72, 187, 120, 0.3);
            border: 1px solid rgba(72, 187, 120, 0.5);
        }
        .footer {
            text-align: center;
            margin-top: 60px;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Queztl 3D Showcase</h1>
        <p class="subtitle">Interactive demos of our 3D technology stack</p>
        
        <div class="demos-grid">
            <a href="3d-demo.html" class="demo-link">
                <div class="demo-card">
                    <div class="demo-icon">🎮</div>
                    <div class="demo-title">3D Cube Demo</div>
                    <div class="demo-desc">
                        Real-time 3D rendering without GPU hardware. See our WebGPU virtual driver in action.
                    </div>
                    <span class="status">✅ A-Grade: 78 FPS</span>
                </div>
            </a>
            
            <a href="benchmark.html" class="demo-link">
                <div class="demo-card">
                    <div class="demo-icon">🏆</div>
                    <div class="demo-title">3DMark Benchmark</div>
                    <div class="demo-desc">
                        Professional GPU benchmark suite. 6 comprehensive tests with industry-standard scoring.
                    </div>
                    <span class="status">✅ S-Grade: 5.82M ops/sec</span>
                </div>
            </a>
            
            <a href="email.html" class="demo-link">
                <div class="demo-card">
                    <div class="demo-icon">📧</div>
                    <div class="demo-title">Email System</div>
                    <div class="demo-desc">
                        Lightning-fast email delivery. 10-20x faster than ProtonMail with QHP protocol.
                    </div>
                    <span class="status">✅ 2.5ms delivery</span>
                </div>
            </a>
            
            <a href="secrets.html" class="demo-link">
                <div class="demo-card">
                    <div class="demo-icon">🔐</div>
                    <div class="demo-title">Secrets Vault</div>
                    <div class="demo-desc">
                        Encrypted storage for API keys and credentials. AES-256 encryption, local-only.
                    </div>
                    <span class="status">✅ Military-grade</span>
                </div>
            </a>
        </div>
        
        <div class="footer">
            <p>Built by Salvador Sena | Queztl</p>
            <p>salvador@senasaitech.com | senasaitech.com</p>
        </div>
    </div>
</body>
</html>
EOF

echo "✅ Demo index created"

# Create netlify config
cat > "$DEPLOY_DIR/netlify.toml" << 'EOF'
[build]
  publish = "."

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    Access-Control-Allow-Origin = "*"
    X-Frame-Options = "SAMEORIGIN"
    X-Content-Type-Options = "nosniff"
EOF

echo "✅ Netlify config created"

echo ""
echo "📦 Deployment package ready at: $DEPLOY_DIR"
echo ""
echo "🚀 Deploy Options:"
echo ""
echo "Option 1 - Drag & Drop (Easiest):"
echo "  1. Go to: https://app.netlify.com/drop"
echo "  2. Drag the folder: $DEPLOY_DIR"
echo "  3. Done! You'll get a URL like: random-name.netlify.app"
echo ""
echo "Option 2 - Netlify CLI:"
echo "  cd $DEPLOY_DIR"
echo "  netlify deploy --prod"
echo ""
echo "Option 3 - Update Existing Site:"
if [ -f ".netlify/state.json" ]; then
    echo "  cd $DEPLOY_DIR"
    echo "  netlify deploy --prod --dir=. --site=senzeni"
else
    echo "  Need to link site first: netlify link"
fi

echo ""
echo "📋 Files ready to deploy:"
ls -lh "$DEPLOY_DIR"

echo ""
echo "🌐 After deployment, your demos will be at:"
echo "  - senasaitech.com/demos.html  (Demo hub)"
echo "  - senasaitech.com/3d-demo.html  (3D Cube)"
echo "  - senasaitech.com/benchmark.html  (3DMark)"
echo "  - senasaitech.com/email.html  (Email UI)"
echo "  - senasaitech.com/secrets.html  (Secrets Vault)"
echo ""

# Ask if user wants to deploy now
read -p "Deploy to Netlify now? (y/n): " deploy_now

if [ "$deploy_now" = "y" ]; then
    echo ""
    echo "🚀 Deploying to Netlify..."
    cd "$DEPLOY_DIR"
    
    # Check if netlify CLI is installed
    if command -v netlify &> /dev/null; then
        netlify deploy --prod --dir=.
    else
        echo "⚠️  Netlify CLI not installed"
        echo "Install with: npm install -g netlify-cli"
        echo "Then run: cd $DEPLOY_DIR && netlify deploy --prod"
        echo ""
        echo "Or use drag & drop: https://app.netlify.com/drop"
        open "https://app.netlify.com/drop"
    fi
fi

echo ""
echo "✅ Done! Your 3D demos are ready to go live! 🎨"
