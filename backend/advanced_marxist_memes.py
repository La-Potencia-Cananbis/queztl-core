#!/usr/bin/env python3
"""
Advanced Marxist Meme Generator - Radical Leftist Graphics
Inspired by historical socialist propaganda, revolutionary aesthetics,
and true Marxist-Leninist theory
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import random
from typing import Tuple, List, Optional
from datetime import datetime
import math


class AdvancedMarxistMemeGenerator:
    """Generate advanced Marxist propaganda-style memes with revolutionary aesthetics"""
    
    # Authentic revolutionary color palette
    COLORS = {
        'red': (204, 0, 0),              # Communist red
        'blood_red': (139, 0, 0),        # Deep revolutionary red
        'black': (0, 0, 0),              # Solidarity black
        'white': (255, 255, 255),        # Pure white
        'gold': (218, 165, 32),          # Soviet gold
        'cream': (245, 222, 179),        # Aged paper
        'sepia': (112, 66, 20),          # Historical brown
        'dark_grey': (40, 40, 40),       # Industrial grey
        'yellow': (255, 215, 0),         # Warning/struggle
        'orange': (255, 140, 0),         # Resistance
    }
    
    # 30 Advanced Marxist/Radical Leftist Slogans
    ADVANCED_SLOGANS = [
        # Classical Marxism
        ("THE HISTORY OF ALL HITHERTO EXISTING SOCIETY\nIS THE HISTORY OF CLASS STRUGGLES", 
         "LA HISTORIA DE TODAS LAS SOCIEDADES\nES LA HISTORIA DE LA LUCHA DE CLASES"),
        
        ("FROM EACH ACCORDING TO ABILITY\nTO EACH ACCORDING TO NEED",
         "DE CADA CUAL SEGÚN SU CAPACIDAD\nA CADA CUAL SEGÚN SU NECESIDAD"),
        
        ("THE RULING IDEAS ARE THE IDEAS\nOF THE RULING CLASS",
         "LAS IDEAS DOMINANTES SON LAS IDEAS\nDE LA CLASE DOMINANTE"),
        
        # Anti-Capitalism
        ("CAPITALISM: LEGALIZED THEFT\nOF SURPLUS VALUE",
         "CAPITALISMO: ROBO LEGALIZADO\nDEL VALOR EXCEDENTE"),
        
        ("PRIVATE PROPERTY IS THEFT\nCOLLECTIVE OWNERSHIP IS FREEDOM",
         "LA PROPIEDAD PRIVADA ES ROBO\nLA PROPIEDAD COLECTIVA ES LIBERTAD"),
        
        ("THE BOURGEOISIE CANNOT EXIST\nWITHOUT EXPLOITING LABOR",
         "LA BURGUESÍA NO PUEDE EXISTIR\nSIN EXPLOTAR EL TRABAJO"),
        
        # Revolutionary Action
        ("REVOLUTION IS NOT A DINNER PARTY\nIT IS AN ACT OF VIOLENCE",
         "LA REVOLUCIÓN NO ES UNA CENA\nES UN ACTO DE VIOLENCIA"),
        
        ("UNDER NO PRETEXT SHOULD ARMS\nBE SURRENDERED BY THE WORKERS",
         "BAJO NINGÚN PRETEXTO LAS ARMAS\nDEBEN SER ENTREGADAS POR LOS TRABAJADORES"),
        
        ("THE OPPRESSED ARE ALLOWED ONCE EVERY FEW YEARS\nTO DECIDE WHICH OPPRESSORS WILL REPRESENT THEM",
         "A LOS OPRIMIDOS SE LES PERMITE CADA POCOS AÑOS\nDECIDIR QUÉ OPRESORES LOS REPRESENTARÁN"),
        
        # Class Consciousness
        ("THERE IS NO ETHICAL CONSUMPTION\nUNDER CAPITALISM",
         "NO HAY CONSUMO ÉTICO\nBAJO EL CAPITALISMO"),
        
        ("YOUR CHAINS ARE NOT INEVITABLE\nTHEY ARE MANUFACTURED",
         "TUS CADENAS NO SON INEVITABLES\nSON FABRICADAS"),
        
        ("THE CAPITALISTS WILL SELL US THE ROPE\nWITH WHICH WE HANG THEM",
         "LOS CAPITALISTAS NOS VENDERÁN LA CUERDA\nCON LA QUE LOS AHORCAREMOS"),
        
        # Worker Power
        ("ALL POWER TO THE WORKERS' COUNCILS\nDICTATORSHIP OF THE PROLETARIAT",
         "TODO EL PODER A LOS CONSEJOS OBREROS\nDICTADURA DEL PROLETARIADO"),
        
        ("THE EMANCIPATION OF THE WORKING CLASS\nMUST BE THE ACT OF THE WORKERS THEMSELVES",
         "LA EMANCIPACIÓN DE LA CLASE TRABAJADORA\nDEBE SER EL ACTO DE LOS TRABAJADORES MISMOS"),
        
        ("SEIZE THE MEANS OF PRODUCTION\nABOLISH WAGE SLAVERY",
         "TOMAR LOS MEDIOS DE PRODUCCIÓN\nABOLIR LA ESCLAVITUD ASALARIADA"),
        
        # Imperialism
        ("IMPERIALISM IS THE HIGHEST STAGE\nOF CAPITALISM",
         "EL IMPERIALISMO ES LA ETAPA SUPERIOR\nDEL CAPITALISMO"),
        
        ("NO WAR BUT CLASS WAR\nWORKERS HAVE NO NATION",
         "NO HAY MÁS GUERRA QUE LA DE CLASES\nLOS TRABAJADORES NO TIENEN NACIÓN"),
        
        ("BEHIND EVERY FORTUNE\nLIES A GREAT CRIME",
         "DETRÁS DE CADA FORTUNA\nSE ESCONDE UN GRAN CRIMEN"),
        
        # Radical Demands
        ("ABOLISH RENT\nHOUSING IS A HUMAN RIGHT",
         "ABOLIR EL ALQUILER\nLA VIVIENDA ES UN DERECHO HUMANO"),
        
        ("ABOLISH PROFIT\nABOLISH EXPLOITATION",
         "ABOLIR LA GANANCIA\nABOLIR LA EXPLOTACIÓN"),
        
        ("GENERAL STRIKE\nSHUT DOWN THE SYSTEM",
         "HUELGA GENERAL\nCERRAR EL SISTEMA"),
        
        # Revolutionary Theory
        ("PRACTICE WITHOUT THEORY IS BLIND\nTHEORY WITHOUT PRACTICE IS STERILE",
         "LA PRÁCTICA SIN TEORÍA ES CIEGA\nLA TEORÍA SIN PRÁCTICA ES ESTÉRIL"),
        
        ("BE REALISTIC\nDEMAND THE IMPOSSIBLE",
         "SÉ REALISTA\nEXIGE LO IMPOSIBLE"),
        
        ("THE PHILOSOPHERS HAVE ONLY INTERPRETED THE WORLD\nTHE POINT IS TO CHANGE IT",
         "LOS FILÓSOFOS SOLO HAN INTERPRETADO EL MUNDO\nEL OBJETIVO ES CAMBIARLO"),
        
        # Solidarity
        ("AN INJURY TO ONE IS AN INJURY TO ALL\nSABOTAGE IS JUSTIFIED",
         "UNA INJUSTICIA CONTRA UNO ES CONTRA TODOS\nEL SABOTAJE ESTÁ JUSTIFICADO"),
        
        ("DIVERSITY IS OUR STRENGTH\nUNITY IS OUR WEAPON",
         "LA DIVERSIDAD ES NUESTRA FUERZA\nLA UNIDAD ES NUESTRA ARMA"),
        
        # Revolutionary Vision
        ("DARE TO STRUGGLE\nDARE TO WIN",
         "ATRÉVETE A LUCHAR\nATRÉVETE A GANAR"),
        
        ("WE HAVE NOTHING TO LOSE BUT OUR CHAINS\nWE HAVE A WORLD TO WIN",
         "NO TENEMOS NADA QUE PERDER EXCEPTO NUESTRAS CADENAS\nTENEMOS UN MUNDO QUE GANAR"),
        
        ("THE FUTURE IS UNWRITTEN\nWRITE IT IN RED",
         "EL FUTURO NO ESTÁ ESCRITO\nESCRÍBELO EN ROJO"),
        
        # Modern Struggles
        ("CLIMATE JUSTICE IS CLASS JUSTICE\nECO-SOCIALISM OR EXTINCTION",
         "JUSTICIA CLIMÁTICA ES JUSTICIA DE CLASE\nECO-SOCIALISMO O EXTINCIÓN"),
    ]
    
    # Revolutionary statistics
    RADICAL_STATISTICS = [
        ("3", "billionaires own more wealth\nthan bottom 50% of humanity"),
        ("$16T", "stolen from workers\nin unpaid wages since 2000"),
        ("1%", "of population causes\n50% of aviation emissions"),
        ("26", "people own as much wealth\nas poorest 3.8 billion"),
        ("89%", "of global inequality\ncaused by capitalism"),
        ("100", "corporations cause\n71% of emissions"),
        ("50%", "of food is wasted\nwhile millions starve"),
        ("$21T", "hidden in tax havens\nby the ultra-rich"),
        ("10x", "CEO pay vs worker pay\nin 1965, now 351x"),
        ("67%", "of new wealth goes\nto richest 1%"),
    ]
    
    def __init__(self, output_dir: Path = None, high_res: bool = True):
        """Initialize advanced generator"""
        self.output_dir = output_dir or Path("output/marxist_memes")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # High resolution for quality propaganda
        self.size = (2160, 2160) if high_res else (1080, 1080)
        self.quality = 98  # Maximum quality
        
    def get_font(self, size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
        """Get bold impactful fonts"""
        font_names = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/Library/Fonts/Arial Bold.ttf",
            "/System/Library/Fonts/HelveticaNeue.ttc",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]
        
        for font_name in font_names:
            try:
                return ImageFont.truetype(font_name, size)
            except:
                continue
        
        return ImageFont.load_default()
    
    def add_vignette(self, img: Image.Image) -> Image.Image:
        """Add vintage vignette effect"""
        width, height = img.size
        vignette = Image.new('L', (width, height), 255)
        draw = ImageDraw.Draw(vignette)
        
        for i in range(min(width, height) // 4):
            alpha = int(255 * (1 - (i / (min(width, height) / 4)) ** 2))
            draw.rectangle([i, i, width-i, height-i], outline=alpha)
        
        vignette = vignette.filter(ImageFilter.GaussianBlur(radius=50))
        img.putalpha(vignette)
        return img
    
    def add_texture(self, img: Image.Image) -> Image.Image:
        """Add paper/grain texture"""
        try:
            noise = Image.effect_noise(img.size, 10)
            img_rgb = img.convert('RGB')
            noise_rgb = noise.convert('RGB')
            img = Image.blend(img_rgb, noise_rgb, 0.03)
        except:
            # Skip texture if it fails
            pass
        return img
    
    def add_text_with_shadow(
        self,
        draw: ImageDraw.ImageDraw,
        position: Tuple[int, int],
        text: str,
        font: ImageFont.FreeTypeFont,
        fill_color: Tuple[int, int, int],
        shadow_color: Tuple[int, int, int] = (0, 0, 0),
        shadow_offset: int = 6,
        align: str = "center"
    ):
        """Add text with drop shadow for impact"""
        x, y = position
        anchor = "mm" if align == "center" else "lm"
        
        # Shadow
        draw.text(
            (x + shadow_offset, y + shadow_offset),
            text,
            font=font,
            fill=shadow_color,
            anchor=anchor
        )
        
        # Main text
        draw.text(
            position,
            text,
            font=font,
            fill=fill_color,
            anchor=anchor
        )
    
    def wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
        """Wrap text intelligently"""
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
    
    def generate_constructivist_meme(
        self,
        slogan: Tuple[str, str] = None
    ) -> Image.Image:
        """Soviet constructivist style with geometric shapes"""
        img = Image.new('RGB', self.size, self.COLORS['cream'])
        draw = ImageDraw.Draw(img)
        
        # Select slogan
        if slogan is None:
            slogan = random.choice(self.ADVANCED_SLOGANS)
        
        slogan_en, slogan_es = slogan
        
        # Geometric red shapes (constructivist style)
        # Large red triangle
        points = [
            (0, 0),
            (self.size[0] // 2, 0),
            (0, self.size[1] // 2)
        ]
        draw.polygon(points, fill=self.COLORS['red'])
        
        # Red diagonal stripe
        stripe_width = self.size[0] // 8
        points = [
            (self.size[0], 0),
            (self.size[0], stripe_width),
            (self.size[0] - self.size[0]//3, self.size[1]),
            (self.size[0] - self.size[0]//3 - stripe_width, self.size[1])
        ]
        draw.polygon(points, fill=self.COLORS['blood_red'])
        
        # Black accent bar
        bar_height = self.size[1] // 10
        draw.rectangle(
            [(0, self.size[1] - bar_height), (self.size[0], self.size[1])],
            fill=self.COLORS['black']
        )
        
        # Main slogan (English) - large and bold
        font_large = self.get_font(self.size[0] // 18, bold=True)
        lines = slogan_en.split('\n')
        
        y_pos = self.size[1] // 2 - (len(lines) * self.size[0] // 24) // 2
        for line in lines:
            wrapped = self.wrap_text(line, font_large, self.size[0] - 200)
            for wrapped_line in wrapped:
                self.add_text_with_shadow(
                    draw,
                    (self.size[0] // 2, y_pos),
                    wrapped_line,
                    font_large,
                    self.COLORS['black'],
                    shadow_color=(100, 100, 100),
                    shadow_offset=8
                )
                y_pos += self.size[0] // 20
        
        # Spanish translation - smaller
        font_medium = self.get_font(self.size[0] // 35, bold=True)
        y_pos += self.size[0] // 25
        for line in slogan_es.split('\n'):
            self.add_text_with_shadow(
                draw,
                (self.size[0] // 2, y_pos),
                line,
                font_medium,
                self.COLORS['blood_red'],
                shadow_offset=4
            )
            y_pos += self.size[0] // 32
        
        # Revolutionary star or fist icon placeholder
        # Add "NM SOCIALISTS" in black bar
        font_small = self.get_font(self.size[0] // 40)
        draw.text(
            (self.size[0] // 2, self.size[1] - bar_height // 2),
            "NM SOCIALISTS • ORGANIZE • AGITATE • EDUCATE",
            font=font_small,
            fill=self.COLORS['white'],
            anchor="mm"
        )
        
        # Add texture
        img = self.add_texture(img)
        
        return img
    
    def generate_agitprop_poster(
        self,
        slogan: Tuple[str, str] = None
    ) -> Image.Image:
        """Revolutionary agitprop poster style"""
        img = Image.new('RGB', self.size, self.COLORS['black'])
        draw = ImageDraw.Draw(img)
        
        # Select slogan
        if slogan is None:
            slogan = random.choice(self.ADVANCED_SLOGANS)
        
        slogan_en, slogan_es = slogan
        
        # Bold red banner across top
        banner_height = self.size[1] // 6
        draw.rectangle(
            [(0, 0), (self.size[0], banner_height)],
            fill=self.COLORS['red']
        )
        
        # Gold accent stripe
        accent_height = 20
        draw.rectangle(
            [(0, banner_height - accent_height), (self.size[0], banner_height)],
            fill=self.COLORS['gold']
        )
        
        # Large centered text on black
        font_huge = self.get_font(self.size[0] // 15, bold=True)
        
        # Main message
        y_pos = self.size[1] // 2 - 100
        for line in slogan_en.split('\n'):
            wrapped = self.wrap_text(line, font_huge, self.size[0] - 200)
            for wrapped_line in wrapped:
                self.add_text_with_shadow(
                    draw,
                    (self.size[0] // 2, y_pos),
                    wrapped_line,
                    font_huge,
                    self.COLORS['white'],
                    shadow_color=self.COLORS['red'],
                    shadow_offset=10
                )
                y_pos += self.size[0] // 18
        
        # Spanish below
        font_large = self.get_font(self.size[0] // 28, bold=True)
        y_pos += self.size[0] // 20
        for line in slogan_es.split('\n'):
            draw.text(
                (self.size[0] // 2, y_pos),
                line,
                font=font_large,
                fill=self.COLORS['yellow'],
                anchor="mm"
            )
            y_pos += self.size[0] // 25
        
        # Bottom red stripe with call to action
        bottom_height = self.size[1] // 8
        draw.rectangle(
            [(0, self.size[1] - bottom_height), (self.size[0], self.size[1])],
            fill=self.COLORS['red']
        )
        
        font_medium = self.get_font(self.size[0] // 35)
        draw.text(
            (self.size[0] // 2, self.size[1] - bottom_height // 2),
            "JOIN THE STRUGGLE • NMSOCIALISTS.ORG",
            font=font_medium,
            fill=self.COLORS['white'],
            anchor="mm"
        )
        
        return img
    
    def generate_radical_statistic(
        self,
        statistic: Tuple[str, str] = None
    ) -> Image.Image:
        """Shocking statistics about capitalism"""
        img = Image.new('RGB', self.size, self.COLORS['dark_grey'])
        draw = ImageDraw.Draw(img)
        
        # Select statistic
        if statistic is None:
            statistic = random.choice(self.RADICAL_STATISTICS)
        
        number, description = statistic
        
        # Blood red diagonal background
        points = [
            (0, 0),
            (self.size[0], self.size[1] // 3),
            (self.size[0], self.size[1]),
            (0, self.size[1])
        ]
        draw.polygon(points, fill=self.COLORS['blood_red'])
        
        # Massive number
        font_massive = self.get_font(self.size[0] // 6, bold=True)
        self.add_text_with_shadow(
            draw,
            (self.size[0] // 2, self.size[1] // 3),
            number,
            font_massive,
            self.COLORS['white'],
            shadow_color=self.COLORS['black'],
            shadow_offset=15
        )
        
        # Description
        font_large = self.get_font(self.size[0] // 24, bold=True)
        y_pos = self.size[1] // 2 + 100
        for line in description.split('\n'):
            draw.text(
                (self.size[0] // 2, y_pos),
                line,
                font=font_large,
                fill=self.COLORS['white'],
                anchor="mm"
            )
            y_pos += self.size[0] // 22
        
        # Revolutionary call
        font_medium = self.get_font(self.size[0] // 32, bold=True)
        draw.text(
            (self.size[0] // 2, self.size[1] - 150),
            "THIS IS WHY WE FIGHT",
            font=font_medium,
            fill=self.COLORS['gold'],
            anchor="mm"
        )
        
        draw.text(
            (self.size[0] // 2, self.size[1] - 80),
            "CAPITALISM CANNOT BE REFORMED",
            font=font_medium,
            fill=self.COLORS['white'],
            anchor="mm"
        )
        
        return img
    
    def generate_vintage_propaganda(
        self,
        slogan: Tuple[str, str] = None
    ) -> Image.Image:
        """Vintage 1917-1940s propaganda poster style"""
        img = Image.new('RGB', self.size, self.COLORS['sepia'])
        draw = ImageDraw.Draw(img)
        
        # Select slogan
        if slogan is None:
            slogan = random.choice(self.ADVANCED_SLOGANS)
        
        slogan_en, slogan_es = slogan
        
        # Aged paper texture
        img = self.add_texture(img)
        
        # Large red star or hammer & sickle inspired shape
        # Red vertical bar on left
        bar_width = self.size[0] // 8
        draw.rectangle(
            [(0, 0), (bar_width, self.size[1])],
            fill=self.COLORS['red']
        )
        
        # Black border
        border = 30
        draw.rectangle(
            [(border, border), (self.size[0] - border, self.size[1] - border)],
            outline=self.COLORS['black'],
            width=15
        )
        
        # Centered bold text
        font_large = self.get_font(self.size[0] // 20, bold=True)
        
        y_pos = self.size[1] // 3
        for line in slogan_en.split('\n'):
            wrapped = self.wrap_text(line, font_large, self.size[0] - bar_width - 300)
            for wrapped_line in wrapped:
                draw.text(
                    (self.size[0] // 2 + bar_width // 2, y_pos),
                    wrapped_line,
                    font=font_large,
                    fill=self.COLORS['black'],
                    anchor="mm"
                )
                y_pos += self.size[0] // 19
        
        # Spanish
        font_medium = self.get_font(self.size[0] // 35, bold=True)
        y_pos += 80
        for line in slogan_es.split('\n'):
            draw.text(
                (self.size[0] // 2 + bar_width // 2, y_pos),
                line,
                font=font_medium,
                fill=self.COLORS['blood_red'],
                anchor="mm"
            )
            y_pos += self.size[0] // 30
        
        # Vintage effect
        img = img.filter(ImageFilter.EDGE_ENHANCE)
        
        return img
    
    def generate_random_advanced_meme(self, meme_type: str = None) -> Image.Image:
        """Generate random advanced meme"""
        if meme_type is None:
            meme_type = random.choice([
                'constructivist',
                'agitprop',
                'radical_statistic',
                'vintage_propaganda'
            ])
        
        if meme_type == 'constructivist':
            return self.generate_constructivist_meme()
        elif meme_type == 'agitprop':
            return self.generate_agitprop_poster()
        elif meme_type == 'radical_statistic':
            return self.generate_radical_statistic()
        elif meme_type == 'vintage_propaganda':
            return self.generate_vintage_propaganda()
        else:
            raise ValueError(f"Unknown meme type: {meme_type}")
    
    def save_meme(self, img: Image.Image, filename: str = None) -> Path:
        """Save high quality meme"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"marxist_meme_{timestamp}.png"
        
        filepath = self.output_dir / filename
        img.save(filepath, "PNG", quality=self.quality, optimize=False)
        print(f"✓ Saved: {filepath.name}")
        return filepath
    
    def generate_batch(self, count: int = 30) -> List[Path]:
        """Generate batch of advanced memes"""
        print(f"🚩 Generating {count} advanced Marxist memes (high-res)...")
        filepaths = []
        
        types = ['constructivist', 'agitprop', 'radical_statistic', 'vintage_propaganda']
        
        for i in range(count):
            meme_type = types[i % len(types)]
            img = self.generate_random_advanced_meme(meme_type)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"advanced_{meme_type}_{timestamp}_{i+1:02d}.png"
            filepath = self.save_meme(img, filename)
            filepaths.append(filepath)
        
        print(f"✓ Generated {count} memes in {self.output_dir}")
        return filepaths


def main():
    """CLI interface"""
    import sys
    
    generator = AdvancedMarxistMemeGenerator(high_res=True)
    
    if len(sys.argv) > 1:
        count = int(sys.argv[1])
        generator.generate_batch(count)
    else:
        # Generate 30 by default
        generator.generate_batch(30)


if __name__ == "__main__":
    main()
