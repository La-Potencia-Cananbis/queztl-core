# New Mexico Socialists - Optimized Site

## 🎉 What's New

### Performance Improvements
- ✅ Images optimized from 53MB to 4.9MB (91% reduction!)
- ✅ All images converted to WebP format
- ✅ Lazy loading for below-the-fold images
- ✅ Netlify CDN caching configured
- ✅ Text cleaned up and simplified

### New Features
- 🔥 **Meme of the Week** - Automatically rotates every Monday
- 📱 **Meme Gallery** - All 19 memes with download buttons
- ⭐ Featured meme highlighted in gallery
- 📅 Week indicator shows current date range

## How It Works

The site automatically features a different meme each week:
- Week 1 (Jan 1-7): Meme #1
- Week 2 (Jan 8-14): Meme #2
- Week 49 (Dec 5-11, 2025): **Meme #10** ⬅️ THIS WEEK!
- Week 50: Meme #11
- And so on... cycles through all 19 memes

## File Structure

```
optimized-site/
├── index.html              # Main HTML (optimized)
├── netlify.toml            # Netlify configuration
├── _headers                # CDN caching rules
├── assets/
│   ├── css/
│   │   └── styles.css      # Enhanced with gallery styles
│   ├── js/
│   │   └── main.js         # Weekly rotation logic
│   └── img/
│       ├── webp/           # Optimized WebP images (4.9MB)
│       │   ├── meme_1.webp
│       │   └── ... (19 total)
│       └── *.png           # Original fallbacks (53MB)
```

## Deployment to Netlify

### Option 1: Netlify CLI (Fastest)
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy from this directory
cd ~/Documents/NM\ Socialists/optimized-site
netlify deploy --prod --dir=.
```

### Option 2: Git + Netlify (Recommended)
```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Optimized site with weekly memes"

# Push to GitHub
git remote add origin YOUR_REPO_URL
git push -u origin main

# In Netlify dashboard:
# 1. Connect repository
# 2. Set publish directory: /
# 3. Deploy!
```

### Option 3: Drag & Drop
1. Zip this entire folder
2. Go to https://app.netlify.com/drop
3. Drag and drop the zip file

## Testing Locally

```bash
# Simple HTTP server
python3 -m http.server 8000

# Or with Node.js
npx serve .
```

Then open: http://localhost:8000

## Expected Performance

### Before Optimization:
- Mobile Score: 40-50
- Load Time: 8-12 seconds
- Total Size: 53.8 MB
- LCP: 8+ seconds

### After Optimization:
- Mobile Score: **85-95** ✅
- Load Time: **2-3 seconds** ✅
- Total Size: **4.9 MB** ✅
- LCP: **2-3 seconds** ✅

## Maintenance

### Adding New Memes
1. Add new image as `assets/img/meme_20.png`
2. Convert to WebP:
   ```bash
   sharp -i assets/img/meme_20.png -o assets/img/webp/meme_20.webp -f webp -q 80
   ```
3. Update `TOTAL_MEMES` in `assets/js/main.js`

### Changing Featured Meme Manually
Edit line 16 in `assets/js/main.js`:
```javascript
return 5; // Always show meme #5
```

## Notes

- The weekly rotation is automatic - no updates needed!
- Original PNG files are kept as fallbacks for older browsers
- All images have lazy loading except the logo
- Gallery shows all 19 memes with featured badge on current week's meme

## Support

Questions? Email: organizing@newmexicosocialists.com
