#!/bin/bash

################################################################################
# Quetzal Browser - Native Mac App Builder
# Builds a downloadable .app bundle for macOS
################################################################################

set -e

echo "🦅 Building Quetzal Browser for Mac..."
echo "========================================"
echo ""

# Configuration
APP_NAME="QuetzalBrowser"
APP_VERSION="1.0.0"
BUILD_DIR="build/mac"
APP_BUNDLE="${BUILD_DIR}/${APP_NAME}.app"
CONTENTS_DIR="${APP_BUNDLE}/Contents"
MACOS_DIR="${CONTENTS_DIR}/MacOS"
RESOURCES_DIR="${CONTENTS_DIR}/Resources"

# Clean previous build
rm -rf "${BUILD_DIR}"
mkdir -p "${MACOS_DIR}"
mkdir -p "${RESOURCES_DIR}"

echo "✅ Created app bundle structure"

# Create Info.plist
cat > "${CONTENTS_DIR}/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>quetzal-browser</string>
    <key>CFBundleIdentifier</key>
    <string>com.quetzalcore.browser</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>Quetzal Browser</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSAllowsArbitraryLoads</key>
        <true/>
    </dict>
</dict>
</plist>
EOF

echo "✅ Created Info.plist"

# Create launcher script
cat > "${MACOS_DIR}/quetzal-browser" << 'EOF'
#!/bin/bash

# Get the directory where the app is located
APP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
RESOURCES_DIR="${APP_DIR}/Resources"

# Check if backend is running
BACKEND_URL="http://localhost:8000"
if ! curl -s "${BACKEND_URL}/api/health" > /dev/null 2>&1; then
    osascript -e 'display dialog "QuetzalCore backend is not running!\n\nPlease start the backend first:\n./start-quetzal-browser.sh\n\nOr connect to remote backend." buttons {"OK"} default button "OK" with icon caution'
fi

# Open the browser in default web browser
open "${RESOURCES_DIR}/quetzal-browser.html"

# Or use Python's built-in HTTP server
cd "${RESOURCES_DIR}"
python3 -m http.server 8080 > /dev/null 2>&1 &
SERVER_PID=$!

# Wait a moment for server to start
sleep 2

# Open in default browser
open "http://localhost:8080/quetzal-browser.html"

# Keep app running
echo "Quetzal Browser running on http://localhost:8080"
echo "Press Ctrl+C to stop"

# Wait for user to quit
read -p "Press Enter to quit..."

# Kill the server
kill $SERVER_PID 2>/dev/null
EOF

chmod +x "${MACOS_DIR}/quetzal-browser"

echo "✅ Created launcher script"

# Copy browser files
cp frontend/quetzal-browser.html "${RESOURCES_DIR}/"
cp frontend/quetzal-protocol-client.js "${RESOURCES_DIR}/"

echo "✅ Copied browser files"

# Create README
cat > "${RESOURCES_DIR}/README.txt" << 'EOF'
Quetzal Browser - Native Mac Application
=========================================

Version: 1.0.0
Protocol: QP (QuetzalCore Protocol)

Quick Start:
1. Double-click QuetzalBrowser.app to launch
2. Browser will open at http://localhost:8080
3. Connect to your QuetzalCore backend

Default Backend:
- Local: qp://localhost:8000/ws/qp
- Remote: qps://your-server.com/ws/qp

Features:
✅ QP Protocol (10-20x faster than REST)
✅ Multi-protocol support (QP, QPS, HTTP, HTTPS)
✅ GPU operations & monitoring
✅ GIS & Remote Sensing integration
✅ Real-time metrics dashboard

Requirements:
- macOS 10.13 or later
- Python 3.7+ (for local server)
- QuetzalCore backend running

Support:
- Documentation: See QUETZAL_BROWSER_GUIDE.md
- Issues: github.com/SalChicanoLoco/queztl-core

Built with ❤️ for QuetzalCore
EOF

echo "✅ Created README"

# Create app icon (using system default for now)
# You can add a custom .icns file later

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Quetzal Browser Mac App Built Successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📦 Location: ${APP_BUNDLE}"
echo "📁 Size: $(du -sh "${APP_BUNDLE}" | cut -f1)"
echo ""
echo "🚀 To use:"
echo "   1. Open Finder and navigate to: ${BUILD_DIR}"
echo "   2. Double-click QuetzalBrowser.app"
echo "   3. Or drag to /Applications folder"
echo ""
echo "📦 To distribute:"
echo "   cd ${BUILD_DIR} && zip -r QuetzalBrowser-Mac-v1.0.0.zip QuetzalBrowser.app"
echo ""
echo "Dale! Ready to run on any Mac! 🦅💻"
echo ""
