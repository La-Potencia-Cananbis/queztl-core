#!/usr/bin/env python3
"""
Socialist Meme Generator - AI-powered meme creation matching NM Socialists style
Creates bold, bilingual memes with workers' rights themes
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random
from typing import Tuple, List, Optional
from datetime import datetime


class SocialistMemeGenerator:
    """Generate socialist memes matching the NM Socialists aesthetic"""
    
    # Color palette from NM Socialists site
    COLORS = {
        'red': (230, 57, 70),          # Primary red
        'black': (27, 18, 15),         # Deep black
        'white': (255, 255, 255),       # Pure white
        'cream': (244, 225, 198),       # Warm cream background
        'gold': (246, 199, 69),         # Accent gold
        'dark_red': (180, 30, 40),      # Darker red for contrast
    }
    
    # Bold socialist slogans (English)
    SLOGANS_EN = [
        "WORKERS OF THE WORLD, UNITE!",
        "PEOPLE OVER PROFIT",
        "SOLIDARITY FOREVER",
        "AN INJURY TO ONE IS AN INJURY TO ALL",
        "WORKERS' RIGHTS ARE HUMAN RIGHTS",
        "ORGANIZE. EDUCATE. AGITATE.",
        "THE PEOPLE, UNITED, WILL NEVER BE DEFEATED",
        "ANOTHER WORLD IS POSSIBLE",
        "POWER TO THE WORKERS",
        "CAPITALISM ISN'T WORKING",
        "WORKERS CREATE ALL WEALTH",
        "HEALTHCARE IS A HUMAN RIGHT",
        "HOUSING IS A HUMAN RIGHT",
        "EDUCATION IS A HUMAN RIGHT",
        "NO WAR BUT CLASS WAR",
        "UNITE AND FIGHT",
        "LABOR CREATES ALL WEALTH",
        "SEIZE THE MEANS",
        "WORKERS' DEMOCRACY NOW",
        "END WAGE SLAVERY"
    ]
    
    # Bold socialist slogans (Spanish)
    SLOGANS_ES = [
        "¡TRABAJADORES DEL MUNDO, ÚNANSE!",
        "LA GENTE ANTES QUE LAS GANANCIAS",
        "SOLIDARIDAD PARA SIEMPRE",
        "UNA INJUSTICIA CONTRA UNO ES UNA INJUSTICIA CONTRA TODOS",
        "LOS DERECHOS LABORALES SON DERECHOS HUMANOS",
        "ORGANIZAR. EDUCAR. AGITAR.",
        "EL PUEBLO UNIDO JAMÁS SERÁ VENCIDO",
        "OTRO MUNDO ES POSIBLE",
        "PODER PARA LOS TRABAJADORES",
        "EL CAPITALISMO NO FUNCIONA",
        "LOS TRABAJADORES CREAN TODA LA RIQUEZA",
        "LA SALUD ES UN DERECHO HUMANO",
        "LA VIVIENDA ES UN DERECHO HUMANO",
        "LA EDUCACIÓN ES UN DERECHO HUMANO",
        "NO HAY MÁS GUERRA QUE LA DE CLASES",
        "UNIR Y LUCHAR",
        "EL TRABAJO CREA TODA LA RIQUEZA",
        "TOMAR LOS MEDIOS DE PRODUCCIÓN",
        "DEMOCRACIA OBRERA AHORA",
        "FIN A LA ESCLAVITUD ASALARIADA"
    ]
    
    # Statistics and facts
    STATISTICS = [
        ("40%", "of workers live\npaycheck to paycheck"),
        ("$7.25", "minimum wage hasn't\nincreased since 2009"),
        ("50%", "of bankruptcies are\ndue to medical bills"),
        ("1%", "of people own 32%\nof all wealth"),
        ("60%", "of Americans can't\nafford a $1000 emergency"),
        ("32", "hours could be full-time\nwith better productivity"),
        ("$15", "minimum wage would lift\n27M out of poverty"),
        ("70%", "support Medicare for All"),
    ]
    
    def __init__(self, output_dir: Path = None):
        """Initialize meme generator"""
        self.output_dir = output_dir or Path("output/generated_memes")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Standard meme size
        self.size = (1080, 1080)
        
    def get_font(self, size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
        """Get font (try common system fonts)"""
        font_names = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/HelveticaNeue.ttc",
            "/Library/Fonts/Arial Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
        
        for font_name in font_names:
            try:
                return ImageFont.truetype(font_name, size)
            except:
                continue
        
        # Fallback to default
        return ImageFont.load_default()
    
    def add_text_with_stroke(
        self, 
        draw: ImageDraw.ImageDraw, 
        position: Tuple[int, int],
        text: str,
        font: ImageFont.FreeTypeFont,
        fill_color: Tuple[int, int, int],
        stroke_color: Tuple[int, int, int],
        stroke_width: int = 3,
        align: str = "center"
    ):
        """Add text with stroke for better visibility"""
        x, y = position
        
        # Draw stroke
        for adj_x in range(-stroke_width, stroke_width + 1):
            for adj_y in range(-stroke_width, stroke_width + 1):
                draw.text(
                    (x + adj_x, y + adj_y), 
                    text, 
                    font=font, 
                    fill=stroke_color,
                    anchor="mm" if align == "center" else "lm"
                )
        
        # Draw main text
        draw.text(
            position, 
            text, 
            font=font, 
            fill=fill_color,
            anchor="mm" if align == "center" else "lm"
        )
    
    def wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def generate_text_only_meme(
        self, 
        slogan_en: str = None,
        slogan_es: str = None
    ) -> Image.Image:
        """Generate a bold text-only meme"""
        # Create image with cream background
        img = Image.new('RGB', self.size, self.COLORS['cream'])
        draw = ImageDraw.Draw(img)
        
        # Add red stripe at top and bottom
        stripe_height = 120
        draw.rectangle([(0, 0), (self.size[0], stripe_height)], fill=self.COLORS['red'])
        draw.rectangle(
            [(0, self.size[1] - stripe_height), (self.size[0], self.size[1])], 
            fill=self.COLORS['red']
        )
        
        # Select slogans
        slogan_en = slogan_en or random.choice(self.SLOGANS_EN)
        slogan_es = slogan_es or random.choice(self.SLOGANS_ES)
        
        # Main slogan (English)
        font_large = self.get_font(90, bold=True)
        lines_en = self.wrap_text(slogan_en, font_large, self.size[0] - 100)
        
        y_pos = self.size[1] // 2 - (len(lines_en) * 100) // 2
        for line in lines_en:
            self.add_text_with_stroke(
                draw,
                (self.size[0] // 2, y_pos),
                line,
                font_large,
                self.COLORS['black'],
                self.COLORS['white'],
                stroke_width=4
            )
            y_pos += 100
        
        # Spanish translation below
        font_medium = self.get_font(50, bold=True)
        y_pos += 40
        self.add_text_with_stroke(
            draw,
            (self.size[0] // 2, y_pos),
            slogan_es,
            font_medium,
            self.COLORS['dark_red'],
            self.COLORS['white'],
            stroke_width=3
        )
        
        # Footer text
        font_small = self.get_font(32)
        self.add_text_with_stroke(
            draw,
            (self.size[0] // 2, self.size[1] - 60),
            "NM SOCIALISTS",
            font_small,
            self.COLORS['white'],
            self.COLORS['black'],
            stroke_width=2
        )
        
        return img
    
    def generate_statistic_meme(
        self,
        statistic: Tuple[str, str] = None
    ) -> Image.Image:
        """Generate a statistic-focused meme"""
        # Create image with black background
        img = Image.new('RGB', self.size, self.COLORS['black'])
        draw = ImageDraw.Draw(img)
        
        # Red diagonal stripe
        points = [(0, 0), (self.size[0], 0), (self.size[0], 200), (0, 400)]
        draw.polygon(points, fill=self.COLORS['red'])
        
        # Select statistic
        if statistic is None:
            statistic = random.choice(self.STATISTICS)
        
        number, description = statistic
        
        # Giant number
        font_huge = self.get_font(280, bold=True)
        self.add_text_with_stroke(
            draw,
            (self.size[0] // 2, self.size[1] // 2 - 100),
            number,
            font_huge,
            self.COLORS['red'],
            self.COLORS['white'],
            stroke_width=6
        )
        
        # Description
        font_large = self.get_font(65, bold=True)
        lines = description.split('\n')
        y_pos = self.size[1] // 2 + 180
        for line in lines:
            self.add_text_with_stroke(
                draw,
                (self.size[0] // 2, y_pos),
                line,
                font_large,
                self.COLORS['white'],
                self.COLORS['black'],
                stroke_width=4
            )
            y_pos += 75
        
        # Footer
        font_small = self.get_font(36)
        self.add_text_with_stroke(
            draw,
            (self.size[0] // 2, self.size[1] - 80),
            "ORGANIZE WITH NM SOCIALISTS",
            font_small,
            self.COLORS['cream'],
            self.COLORS['black'],
            stroke_width=2
        )
        
        return img
    
    def generate_call_to_action(
        self,
        title: str = None,
        action: str = None,
        contact: str = "nmsocialists.org"
    ) -> Image.Image:
        """Generate a call-to-action meme"""
        # Create split design
        img = Image.new('RGB', self.size, self.COLORS['cream'])
        draw = ImageDraw.Draw(img)
        
        # Red top half
        draw.rectangle([(0, 0), (self.size[0], self.size[1] // 2)], fill=self.COLORS['red'])
        
        # Select content
        title = title or random.choice([
            "JOIN THE STRUGGLE",
            "ORGANIZE YOUR WORKPLACE",
            "FIGHT FOR WORKERS' RIGHTS",
            "DEMAND BETTER",
            "UNITE AND RESIST",
        ])
        
        action = action or random.choice([
            "EVERY WORKER DESERVES DIGNITY",
            "SOLIDARITY IS OUR STRENGTH",
            "TOGETHER WE WIN",
            "YOUR POWER IS IN YOUR UNITY",
        ])
        
        # Title in top half
        font_large = self.get_font(95, bold=True)
        lines = self.wrap_text(title, font_large, self.size[0] - 100)
        y_pos = 180
        for line in lines:
            self.add_text_with_stroke(
                draw,
                (self.size[0] // 2, y_pos),
                line,
                font_large,
                self.COLORS['white'],
                self.COLORS['black'],
                stroke_width=5
            )
            y_pos += 110
        
        # Action text in bottom half
        font_medium = self.get_font(60, bold=True)
        lines = self.wrap_text(action, font_medium, self.size[0] - 120)
        y_pos = self.size[1] // 2 + 120
        for line in lines:
            self.add_text_with_stroke(
                draw,
                (self.size[0] // 2, y_pos),
                line,
                font_medium,
                self.COLORS['black'],
                self.COLORS['white'],
                stroke_width=3
            )
            y_pos += 75
        
        # Contact info
        font_small = self.get_font(42)
        self.add_text_with_stroke(
            draw,
            (self.size[0] // 2, self.size[1] - 100),
            contact,
            font_small,
            self.COLORS['red'],
            self.COLORS['white'],
            stroke_width=3
        )
        
        return img
    
    def generate_random_meme(self, meme_type: str = None) -> Image.Image:
        """Generate a random meme of specified or random type"""
        if meme_type is None:
            meme_type = random.choice(['text_only', 'statistic', 'call_to_action'])
        
        if meme_type == 'text_only':
            return self.generate_text_only_meme()
        elif meme_type == 'statistic':
            return self.generate_statistic_meme()
        elif meme_type == 'call_to_action':
            return self.generate_call_to_action()
        else:
            raise ValueError(f"Unknown meme type: {meme_type}")
    
    def save_meme(self, img: Image.Image, filename: str = None) -> Path:
        """Save meme to output directory"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"socialist_meme_{timestamp}.png"
        
        filepath = self.output_dir / filename
        img.save(filepath, "PNG", quality=95)
        print(f"✓ Saved meme: {filepath}")
        return filepath
    
    def generate_batch(self, count: int = 5) -> List[Path]:
        """Generate a batch of random memes"""
        print(f"🎨 Generating {count} socialist memes...")
        filepaths = []
        
        for i in range(count):
            meme_type = random.choice(['text_only', 'statistic', 'call_to_action'])
            img = self.generate_random_meme(meme_type)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"meme_{meme_type}_{timestamp}_{i+1}.png"
            filepath = self.save_meme(img, filename)
            filepaths.append(filepath)
        
        print(f"✓ Generated {count} memes in {self.output_dir}")
        return filepaths


def main():
    """CLI interface"""
    import sys
    
    generator = SocialistMemeGenerator()
    
    if len(sys.argv) > 1:
        count = int(sys.argv[1])
        generator.generate_batch(count)
    else:
        # Generate one of each type as demo
        print("🎨 Generating demo memes (one of each type)...")
        
        img1 = generator.generate_text_only_meme()
        generator.save_meme(img1, "demo_text_only.png")
        
        img2 = generator.generate_statistic_meme()
        generator.save_meme(img2, "demo_statistic.png")
        
        img3 = generator.generate_call_to_action()
        generator.save_meme(img3, "demo_call_to_action.png")
        
        print("\n✓ Demo memes generated!")
        print(f"📂 Check: {generator.output_dir}")


if __name__ == "__main__":
    main()
