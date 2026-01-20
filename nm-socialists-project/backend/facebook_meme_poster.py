#!/usr/bin/env python3
"""
Facebook Meme Poster - Automated meme posting to Facebook
==========================================================
Uses Facebook Graph API to post memes to your page.
"""

import requests
import json
from pathlib import Path
from typing import Dict, Optional
import time
from datetime import datetime


class FacebookMemePoster:
    """Post memes to Facebook using Graph API"""
    
    def __init__(self, page_access_token: str, page_id: str):
        self.access_token = page_access_token
        self.page_id = page_id
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def post_photo(self, image_path: Path, message: str = "") -> Dict:
        """
        Post a photo to Facebook page
        
        Args:
            image_path: Path to image file
            message: Caption/message for the post
            
        Returns:
            API response with post_id
        """
        print(f"📸 Posting meme: {image_path.name}")
        
        url = f"{self.base_url}/{self.page_id}/photos"
        
        # Read image
        with open(image_path, 'rb') as image_file:
            files = {
                'source': image_file
            }
            
            data = {
                'access_token': self.access_token,
                'message': message
            }
            
            response = requests.post(url, data=data, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Posted! ID: {result.get('id')}")
            print(f"   URL: https://facebook.com/{result.get('post_id', result.get('id'))}")
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return {'error': response.text}
    
    def post_link(self, link: str, message: str = "") -> Dict:
        """Post a link to Facebook page"""
        print(f"🔗 Posting link: {link}")
        
        url = f"{self.base_url}/{self.page_id}/feed"
        
        data = {
            'access_token': self.access_token,
            'message': message,
            'link': link
        }
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Posted! ID: {result.get('id')}")
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return {'error': response.text}
    
    def schedule_daily_meme(self, meme_dir: Path, schedule_time: str = "10:00"):
        """
        Schedule daily meme posting
        
        Args:
            meme_dir: Directory containing meme images
            schedule_time: Time to post (HH:MM format)
        """
        print("🗓️  Daily Meme Scheduler")
        print(f"   Time: {schedule_time}")
        print(f"   Memes: {meme_dir}")
        print()
        
        # Get all meme files
        meme_files = sorted(meme_dir.glob("meme_*.png"))
        
        if not meme_files:
            print("❌ No memes found!")
            return
        
        print(f"📚 Found {len(meme_files)} memes")
        print()
        
        # Post meme of the day (cycle through)
        day_of_year = datetime.now().timetuple().tm_yday
        meme_index = day_of_year % len(meme_files)
        meme_file = meme_files[meme_index]
        
        messages = [
            "🚩 ¡Solidaridad! Another world is possible. #Socialism #NewMexico",
            "✊ People over profit. La gente antes que las ganancias. #WorkersRights",
            "🌎 Land back, workers' rights, real democracy. Join us! #OrganizeNM",
            "📚 Read, organize, educate. The struggle continues! #PoliticalEducation",
            "🔥 From the Río Grande to the Sangre de Cristo, we organize! #NMSocialists"
        ]
        
        message = messages[meme_index % len(messages)]
        
        print(f"🎯 Today's meme: {meme_file.name}")
        print(f"💬 Message: {message}")
        print()
        
        result = self.post_photo(meme_file, message)
        return result


class MemeRotator:
    """Rotate through memes for daily posting"""
    
    def __init__(self, meme_dir: Path):
        self.meme_dir = meme_dir
        self.memes = sorted(meme_dir.glob("meme_*.png"))
        self.current_index = 0
    
    def get_meme_of_day(self) -> Path:
        """Get today's meme (rotates daily)"""
        day_of_year = datetime.now().timetuple().tm_yday
        index = day_of_year % len(self.memes)
        return self.memes[index]
    
    def get_next_meme(self) -> Path:
        """Get next meme in rotation"""
        meme = self.memes[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.memes)
        return meme
    
    def get_random_meme(self) -> Path:
        """Get a random meme"""
        import random
        return random.choice(self.memes)


def setup_facebook_config():
    """Interactive setup for Facebook credentials"""
    print("=" * 80)
    print("Facebook Meme Poster - Setup")
    print("=" * 80)
    print()
    print("You'll need:")
    print("  1. Facebook Page ID")
    print("  2. Page Access Token")
    print()
    print("Get these from: https://developers.facebook.com/tools/explorer/")
    print()
    
    page_id = input("Enter your Facebook Page ID: ").strip()
    access_token = input("Enter your Page Access Token: ").strip()
    
    config = {
        'page_id': page_id,
        'access_token': access_token,
        'created_at': datetime.now().isoformat()
    }
    
    config_file = Path.home() / 'queztl-core' / 'config' / 'facebook.json'
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print()
    print(f"✅ Config saved: {config_file}")
    print()
    
    return config


def load_facebook_config() -> Optional[Dict]:
    """Load Facebook config from file"""
    config_file = Path.home() / 'queztl-core' / 'config' / 'facebook.json'
    
    if not config_file.exists():
        return None
    
    with open(config_file, 'r') as f:
        return json.load(f)


def demo_facebook_posting():
    """Demo Facebook meme posting"""
    print("=" * 80)
    print("Facebook Meme Poster - Demo")
    print("=" * 80)
    print()
    
    # Load or create config
    config = load_facebook_config()
    
    if not config:
        print("⚠️  No Facebook config found. Let's set it up!")
        print()
        config = setup_facebook_config()
    
    # Initialize poster
    poster = FacebookMemePoster(
        page_access_token=config['access_token'],
        page_id=config['page_id']
    )
    
    # Initialize meme rotator
    meme_dir = Path.home() / 'queztl-core' / 'training_data' / 'nm_socialists_original' / 'assets' / 'img'
    
    if not meme_dir.exists():
        print(f"❌ Meme directory not found: {meme_dir}")
        return
    
    rotator = MemeRotator(meme_dir)
    
    # Get meme of the day
    meme = rotator.get_meme_of_day()
    
    print(f"🎨 Meme of the Day: {meme.name}")
    print()
    
    # Confirm before posting
    confirm = input("Post to Facebook? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        message = "🚩 Another world is possible! Join New Mexico Socialists.\n\nPeople over profit • La gente antes que las ganancias\n\n#NewMexico #Socialism #WorkersRights"
        result = poster.post_photo(meme, message)
        
        if 'error' not in result:
            print()
            print("🎉 Success! Your meme is now live on Facebook!")
        else:
            print()
            print("⚠️  There was an issue posting. Check your access token.")
    else:
        print()
        print("👍 Demo complete. No posts made.")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'setup':
        setup_facebook_config()
    elif len(sys.argv) > 1 and sys.argv[1] == 'post':
        demo_facebook_posting()
    else:
        print("Usage:")
        print("  python facebook_meme_poster.py setup   # Configure Facebook credentials")
        print("  python facebook_meme_poster.py post    # Post meme of the day")
        print()
        print("First time? Run 'setup' to configure your Facebook page.")
