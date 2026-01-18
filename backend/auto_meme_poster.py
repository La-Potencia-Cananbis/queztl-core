#!/usr/bin/env python3
"""
Automatic Meme Generator + Facebook Poster
Generates AI socialist memes and posts them to Facebook automatically
"""

from pathlib import Path
import sys
import json
from datetime import datetime
import random

# Import our modules
from meme_generator import SocialistMemeGenerator
from facebook_meme_poster import FacebookMemePoster


class AutoMemePoster:
    """Automatically generate and post memes to Facebook"""
    
    def __init__(self, config_path: Path = None):
        """Initialize auto poster"""
        if config_path is None:
            config_path = Path.home() / "queztl-core/config/facebook.json"
        
        self.config_path = config_path
        self.generator = SocialistMemeGenerator()
        self.config = self.load_config()
        
        if self.config:
            self.poster = FacebookMemePoster(
                page_id=self.config['page_id'],
                access_token=self.config['access_token']
            )
        else:
            self.poster = None
    
    def load_config(self) -> dict:
        """Load Facebook config if exists"""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return None
    
    def has_credentials(self) -> bool:
        """Check if Facebook credentials are configured"""
        return self.config is not None
    
    def generate_and_save(self, meme_type: str = None) -> Path:
        """Generate a new meme and save it"""
        print("🎨 Generating new socialist meme...")
        
        if meme_type is None:
            meme_type = random.choice(['text_only', 'statistic', 'call_to_action'])
        
        img = self.generator.generate_random_meme(meme_type)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"auto_meme_{meme_type}_{timestamp}.png"
        filepath = self.generator.save_meme(img, filename)
        
        print(f"✓ Generated {meme_type} meme: {filepath.name}")
        return filepath
    
    def post_generated_meme(self, filepath: Path) -> bool:
        """Post a generated meme to Facebook"""
        if not self.has_credentials():
            print("⚠️  No Facebook credentials configured")
            print("   Run: python backend/facebook_meme_poster.py setup")
            return False
        
        # Bilingual captions
        captions = [
            "Another world is possible. / Otro mundo es posible. #WorkersRights #NMSocialists",
            "Solidarity forever! / ¡Solidaridad para siempre! #Socialism #NewMexico",
            "Workers of the world, unite! / ¡Trabajadores del mundo, únanse! #LaborRights",
            "People over profit. / La gente antes que las ganancias. #SocialistAction",
            "Your power is in your unity. / Tu poder está en tu unidad. #Organize",
            "Every worker deserves dignity. / Cada trabajador merece dignidad. #WorkersUnited",
            "Fight for workers' rights! / ¡Lucha por los derechos de los trabajadores! #Solidarity",
            "Together we win. / Juntos ganamos. #PeoplesPower",
        ]
        
        caption = random.choice(captions)
        
        print(f"\n📤 Posting to Facebook...")
        print(f"   Caption: {caption}")
        
        result = self.poster.post_photo(filepath, caption)
        
        if result and result.get('id'):
            print(f"✓ Posted successfully! Post ID: {result['id']}")
            return True
        else:
            print(f"✗ Failed to post: {result}")
            return False
    
    def generate_and_post(self, meme_type: str = None) -> bool:
        """Generate a new meme and post it to Facebook"""
        filepath = self.generate_and_save(meme_type)
        
        if self.has_credentials():
            return self.post_generated_meme(filepath)
        else:
            print("\n✓ Meme generated successfully!")
            print("   Configure Facebook credentials to auto-post:")
            print("   python backend/facebook_meme_poster.py setup")
            return True
    
    def generate_batch(self, count: int = 5, post: bool = False) -> None:
        """Generate a batch of memes and optionally post them"""
        print(f"🎨 Generating {count} socialist memes...")
        
        for i in range(count):
            print(f"\n--- Meme {i+1}/{count} ---")
            
            if post and self.has_credentials():
                self.generate_and_post()
            else:
                self.generate_and_save()
        
        print(f"\n✓ Generated {count} memes!")
        print(f"📂 Check: {self.generator.output_dir}")


def main():
    """CLI interface"""
    poster = AutoMemePoster()
    
    if len(sys.argv) < 2:
        print("📋 Auto Meme Poster - Generate & Post Socialist Memes")
        print()
        print("Usage:")
        print("  python backend/auto_meme_poster.py generate         - Generate 1 meme")
        print("  python backend/auto_meme_poster.py generate 5       - Generate 5 memes")
        print("  python backend/auto_meme_poster.py post             - Generate & post 1 meme")
        print("  python backend/auto_meme_poster.py post 5           - Generate & post 5 memes")
        print("  python backend/auto_meme_poster.py daily            - Daily auto-post (for cron)")
        print()
        
        if poster.has_credentials():
            print("✓ Facebook credentials configured")
        else:
            print("⚠️  Facebook credentials not configured")
            print("   Run: python backend/facebook_meme_poster.py setup")
        
        return
    
    command = sys.argv[1]
    
    if command == "generate":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        if count == 1:
            poster.generate_and_save()
        else:
            poster.generate_batch(count, post=False)
    
    elif command == "post":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        if not poster.has_credentials():
            print("⚠️  Please configure Facebook credentials first:")
            print("   python backend/facebook_meme_poster.py setup")
            return
        
        if count == 1:
            poster.generate_and_post()
        else:
            poster.generate_batch(count, post=True)
    
    elif command == "daily":
        # For cron job - generate and post one meme per day
        print(f"📅 Daily auto-post: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        poster.generate_and_post()
    
    else:
        print(f"Unknown command: {command}")
        print("Use: generate, post, or daily")


if __name__ == "__main__":
    main()
