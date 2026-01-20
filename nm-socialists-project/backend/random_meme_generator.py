#!/usr/bin/env python3
"""
Random Meme Generator - Creates memes from templates + text overlays
No GPU needed! Uses PIL to add text to existing images
"""

import os
import random
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime

# Meme templates directory
TEMPLATES_DIR = Path.home() / "queztl-core" / "nm-socialists-project" / "meme_templates"
OUTPUT_DIR = Path.home() / "queztl-core" / "nm-socialists-project" / "frontend" / "generated"

TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Revolutionary quotes and slogans
QUOTES = [
    {
        "top": "WORKERS OF THE WORLD",
        "bottom": "UNITE!",
        "theme": "revolutionary"
    },
    {
        "top": "THE PEOPLE",
        "bottom": "UNITED WILL NEVER BE DEFEATED",
        "theme": "unity"
    },
    {
        "top": "LAND BACK",
        "bottom": "AGUA ES VIDA",
        "theme": "land_rights"
    },
    {
        "top": "HOUSING IS A HUMAN RIGHT",
        "bottom": "NOT A COMMODITY",
        "theme": "housing"
    },
    {
        "top": "¡LA LUCHA SIGUE!",
        "bottom": "THE STRUGGLE CONTINUES",
        "theme": "bilingual"
    },
    {
        "top": "FROM THE RÍO GRANDE",
        "bottom": "TO THE SANGRE DE CRISTO",
        "theme": "new_mexico"
    },
    {
        "top": "WORKERS, NOT BOSSES",
        "bottom": "PEOPLE, NOT PROFIT",
        "theme": "anticapitalist"
    },
    {
        "top": "ORGANIZE",
        "bottom": "AGITATE • EDUCATE",
        "theme": "organizing"
    },
    {
        "top": "NO JUSTICE",
        "bottom": "NO PEACE",
        "theme": "justice"
    },
    {
        "top": "TIERRA Y LIBERTAD",
        "bottom": "LAND AND LIBERTY",
        "theme": "land_grant"
    },
    {
        "top": "EAT THE RICH",
        "bottom": "FEED THE POOR",
        "theme": "wealth"
    },
    {
        "top": "SOLIDARITY",
        "bottom": "IS OUR WEAPON",
        "theme": "solidarity"
    },
]

def create_solid_background(width=1080, height=1080, color="#8B0000"):
    """Create a solid color background"""
    return Image.new('RGB', (width, height), color)

def add_text_to_image(image, top_text, bottom_text):
    """
    Add meme-style text to image (white text, black outline)
    """
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    # Try to use Impact font, fallback to default
    try:
        font_size = int(height * 0.08)
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Impact.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(height * 0.06))
        except:
            font = ImageFont.load_default()
    
    # Function to draw text with outline
    def draw_text_with_outline(text, position, font):
        x, y = position
        # Black outline
        for offset_x in [-3, -2, -1, 0, 1, 2, 3]:
            for offset_y in [-3, -2, -1, 0, 1, 2, 3]:
                if offset_x != 0 or offset_y != 0:
                    draw.text((x + offset_x, y + offset_y), text, font=font, fill="black")
        # White text
        draw.text((x, y), text, font=font, fill="white")
    
    # Draw top text
    if top_text:
        # Get text size
        bbox = draw.textbbox((0, 0), top_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center horizontally, near top
        x = (width - text_width) // 2
        y = int(height * 0.05)
        draw_text_with_outline(top_text, (x, y), font)
    
    # Draw bottom text
    if bottom_text:
        bbox = draw.textbbox((0, 0), bottom_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center horizontally, near bottom
        x = (width - text_width) // 2
        y = height - text_height - int(height * 0.05)
        draw_text_with_outline(bottom_text, (x, y), font)
    
    return image

def generate_meme(template_path=None, quote=None):
    """
    Generate a meme
    If template_path is None, creates red background
    If quote is None, picks random quote
    """
    if quote is None:
        quote = random.choice(QUOTES)
    
    # Create or load image
    if template_path and os.path.exists(template_path):
        img = Image.open(template_path)
        img = img.resize((1080, 1080))
    else:
        # Create red background
        img = create_solid_background(1080, 1080, "#8B0000")
    
    # Add text
    img = add_text_to_image(img, quote["top"], quote["bottom"])
    
    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{quote['theme']}_{timestamp}.png"
    output_path = OUTPUT_DIR / filename
    
    img.save(output_path, quality=95)
    
    return {
        "success": True,
        "path": str(output_path),
        "filename": filename,
        "theme": quote["theme"],
        "top_text": quote["top"],
        "bottom_text": quote["bottom"]
    }

def generate_batch(count=10):
    """Generate a batch of random memes"""
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🚩 NM SOCIALISTS MEME GENERATOR                            ║
║  Generating {count} revolutionary memes                            ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    results = []
    
    for i in range(count):
        print(f"[{i+1}/{count}] Generating meme...")
        result = generate_meme()
        
        if result["success"]:
            print(f"  ✅ {result['theme']}: \"{result['top_text']}\"")
            results.append(result)
        else:
            print(f"  ❌ Failed")
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  ✅ GENERATION COMPLETE                                     ║
╚══════════════════════════════════════════════════════════════╝

Generated: {len(results)} memes
Location:  {OUTPUT_DIR}
View at:   http://localhost:8081/generated/

Themes: {', '.join(set(r['theme'] for r in results))}
""")
    
    return results

if __name__ == "__main__":
    import sys
    
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    generate_batch(count)
