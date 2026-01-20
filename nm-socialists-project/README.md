# New Mexico Socialists - Propaganda Generator
**Domain**: https://newmexicosocialists.com

Separate political activism project from Queztl-Core.

## Files Moved Here:
- `backend/communist_theory_library.py` - Theory database
- `backend/meme_generator.py` - Meme creation engine  
- `backend/content_runner.py` - Auto-posting system
- `backend/facebook_meme_poster.py` - Social media integration
- `frontend/beast_image_ui.html` - Image generator UI
- `frontend/theory_library.html` - Theory browser

## Usage:
```bash
# Generate propaganda images
cd backend
python3 meme_generator.py

# Browse theory library  
python3 communist_theory_library.py
```

## Integration:
- Uses Beast (192.168.1.105:8001) for GPU image generation
- Deployed at: newmexicosocialists.com
- Facebook API integration (pending Meta approval)

---
**Note**: This is a political activism project, completely separate from 
the technical Queztl-Core platform (senasaitech.com).
