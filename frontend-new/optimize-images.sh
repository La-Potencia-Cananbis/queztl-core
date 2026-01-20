#!/bin/bash

# Image Optimization Script for newmexicosocialists.com
# This script will optimize all images in the assets/img directory

echo "🖼️  Image Optimization Script for newmexicosocialists.com"
echo "=========================================================="
echo ""

# Check if required tools are installed
command -v npm >/dev/null 2>&1 || { echo "❌ npm is required but not installed. Install Node.js first."; exit 1; }

# Install sharp-cli if not already installed
if ! command -v sharp &> /dev/null; then
    echo "📦 Installing sharp-cli..."
    npm install -g sharp-cli
fi

# Create output directories
echo "📁 Creating optimized image directories..."
mkdir -p assets/img/optimized
mkdir -p assets/img/webp

echo ""
echo "🎯 Optimizing images..."
echo "------------------------"

# Loop through all PNG and JPG files
for img in assets/img/*.{png,jpg,jpeg,PNG,JPG,JPEG}; do
    if [ -f "$img" ]; then
        filename=$(basename "$img")
        name="${filename%.*}"
        
        echo "Processing: $filename"
        
        # Create WebP versions at different sizes
        # Original size WebP
        sharp -i "$img" -o "assets/img/webp/${name}.webp" -f webp -q 80
        
        # Create responsive sizes (320w, 640w, 1024w)
        sharp -i "$img" -o "assets/img/webp/${name}-320w.webp" -f webp -q 80 -- resize 320
        sharp -i "$img" -o "assets/img/webp/${name}-640w.webp" -f webp -q 80 -- resize 640
        sharp -i "$img" -o "assets/img/webp/${name}-1024w.webp" -f webp -q 80 -- resize 1024
        
        echo "  ✅ Created WebP versions"
    fi
done

echo ""
echo "✨ Optimization complete!"
echo ""
echo "📊 Size comparison:"
du -sh assets/img/*.{png,jpg,jpeg,PNG,JPG,JPEG} 2>/dev/null | head -5
echo "vs."
du -sh assets/img/webp/*.webp 2>/dev/null | head -5

echo ""
echo "📝 Next steps:"
echo "1. Update your HTML to use the new WebP images"
echo "2. Add width and height attributes to all <img> tags"
echo "3. Deploy to Netlify"
echo ""
