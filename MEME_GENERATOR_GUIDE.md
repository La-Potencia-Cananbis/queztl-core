# AI Meme Generator + Auto-Poster - Quick Reference

## ✅ What's Done

- ✅ Removed Drake meme (meme_7.png) from collection
- ✅ AI meme generator with 3 templates matching NM Socialists style
- ✅ Auto-poster that generates + posts to Facebook
- ✅ 18 existing memes + unlimited AI-generated memes
- ✅ Bilingual captions (English + Spanish)
- ✅ All code committed to GitHub (commit 780db72)

## 🎨 Generate Memes

```bash
cd ~/queztl-core
source venv/bin/activate

# Generate demo memes (one of each type)
python backend/meme_generator.py

# Generate 5 random memes
python backend/meme_generator.py 5

# Generated memes saved to: output/generated_memes/
```

## 🤖 Auto Meme Poster

```bash
cd ~/queztl-core
source venv/bin/activate

# Show help
python backend/auto_meme_poster.py

# Generate memes (no Facebook posting)
python backend/auto_meme_poster.py generate     # 1 meme
python backend/auto_meme_poster.py generate 5   # 5 memes

# Generate + post to Facebook (requires credentials)
python backend/auto_meme_poster.py post         # 1 meme
python backend/auto_meme_poster.py post 5       # 5 memes

# Daily auto-post (for cron job)
python backend/auto_meme_poster.py daily
```

## 🔑 Setup Facebook Credentials (DO THIS LAST)

When ready to enable auto-posting:

```bash
cd ~/queztl-core
source venv/bin/activate

# Interactive setup
python backend/facebook_meme_poster.py setup

# You'll need:
# - Facebook Page ID
# - Page Access Token (from Meta Developer Console)
```

## ⏰ Setup Daily Auto-Posting

After adding credentials, setup cron job:

```bash
# Edit crontab
crontab -e

# Add this line (posts at 10 AM daily):
0 10 * * * cd ~/queztl-core && source venv/bin/activate && python backend/auto_meme_poster.py daily >> ~/queztl-core/logs/auto_meme.log 2>&1
```

## 🎨 Meme Templates

### 1. Text Only
- Bold bilingual slogans
- Red stripes top/bottom
- Cream background
- Examples:
  - "WORKERS OF THE WORLD, UNITE!"
  - "PEOPLE OVER PROFIT"
  - "SOLIDARITY FOREVER"

### 2. Statistics
- Giant number + description
- Black background with red diagonal
- Examples:
  - "40% of workers live paycheck to paycheck"
  - "$7.25 minimum wage hasn't increased since 2009"
  - "70% support Medicare for All"

### 3. Call to Action
- Split design (red top, cream bottom)
- Bold title + action message
- Contact info at bottom
- Examples:
  - "JOIN THE STRUGGLE"
  - "ORGANIZE YOUR WORKPLACE"
  - "FIGHT FOR WORKERS' RIGHTS"

## 📊 Current Status

**Existing Memes:** 18 (Drake meme removed)  
**AI Generated:** Unlimited  
**Templates:** 3 types  
**Slogans:** 40 (20 English + 20 Spanish)  
**Statistics:** 8 workers' rights facts  
**Facebook Ready:** ✓ (credentials needed last)

## 🔥 Next Steps

1. ✓ Review generated demo memes in `output/generated_memes/`
2. ⏳ Add Facebook credentials when ready (user preference: LAST)
3. ⏳ Test posting with `python backend/auto_meme_poster.py post`
4. ⏳ Setup daily cron job for automated posting

## 🎯 Quick Test Flow

```bash
# 1. Generate test memes
cd ~/queztl-core && source venv/bin/activate
python backend/auto_meme_poster.py generate 3

# 2. Check output
open output/generated_memes/

# 3. When ready, add credentials
python backend/facebook_meme_poster.py setup

# 4. Test posting
python backend/auto_meme_poster.py post

# 5. Setup daily automation
crontab -e
# Add: 0 10 * * * cd ~/queztl-core && source venv/bin/activate && python backend/auto_meme_poster.py daily
```

## 🔧 Technical Details

**Meme Generator:** `backend/meme_generator.py` (435 lines)
- PIL/Pillow for image generation
- 1080x1080 PNG output
- Text wrapping, stroke effects
- Color palette: red (#E63946), cream (#F4E1C6), black (#1B120F)

**Auto Poster:** `backend/auto_meme_poster.py` (152 lines)
- Combines generator + Facebook API
- Random caption selection (8 bilingual options)
- Config: `~/queztl-core/config/facebook.json`

**Facebook Poster:** `backend/facebook_meme_poster.py` (270 lines)
- Graph API v18.0
- Daily rotation through existing memes
- Credential management

## 📦 Dependencies

- ✓ Pillow (12.1.0) - Image generation
- ✓ requests (2.32.5) - Facebook API
- ✓ Python 3.14 in venv

All installed and working! 🚀
