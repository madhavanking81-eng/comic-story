import os
import time
import requests
import logging
from PIL import Image, ImageDraw, ImageFont, ImageFilter

logger = logging.getLogger("comiccraft")

def generate_image(prompt: str, panel_num: int, art_style: str = "comic book") -> str:
    """
    Generates a comic illustration image based on prompt and art style.
    Saves to static/panels directory and returns relative image path.
    """
    output_dir = os.path.join("static", "panels")
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"panel_{panel_num}_{int(time.time() * 1000)}.png"
    filepath = os.path.join(output_dir, filename)
    relative_path = f"/static/panels/{filename}"
    
    # Attempt 1: Fetch via AI image service (Pollinations / HuggingFace API if available)
    try:
        sanitized_prompt = requests.utils.quote(f"{prompt}, {art_style} comic style, vibrant colors, detailed, trending on artstation")
        url = f"https://image.pollinations.ai/prompt/{sanitized_prompt}?width=600&height=400&nologo=true&seed={panel_num * 42}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and len(response.content) > 1000:
            with open(filepath, "wb") as f:
                f.write(response.content)
            logger.info(f"Generated panel image via AI service: {filepath}")
            return relative_path
    except Exception as e:
        logger.info(f"AI image service fallback triggered for panel {panel_num}: {e}")

    # Attempt 2: High quality stylized Pillow Canvas Generator
    try:
        width, height = 600, 400
        image = Image.new("RGB", (width, height), color=(20, 20, 30))
        draw = ImageDraw.Draw(image)
        
        # Color palettes based on panel index & art style
        palettes = [
            ((15, 32, 67), (44, 83, 100), (255, 107, 107), (78, 205, 196)),    # Panel 1: Deep Navy/Teal
            ((40, 20, 60), (100, 40, 120), (255, 217, 61), (106, 176, 76)),   # Panel 2: Mystic Purple/Gold
            ((60, 20, 20), (140, 40, 40), (255, 71, 87), (255, 165, 2)),      # Panel 3: Crimson Action Red
            ((20, 50, 40), (40, 120, 90), (0, 210, 211), (255, 159, 243)),   # Panel 4: Cosmic Jade/Magenta
            ((50, 35, 15), (130, 85, 30), (255, 159, 67), (254, 202, 87))    # Panel 5: Golden Horizon Sunset
        ]
        
        p_idx = (panel_num - 1) % len(palettes)
        bg_dark, bg_light, accent1, accent2 = palettes[p_idx]
        
        # Draw gradient background
        for y in range(height):
            r = int(bg_dark[0] + (bg_light[0] - bg_dark[0]) * (y / height))
            g = int(bg_dark[1] + (bg_light[1] - bg_dark[1]) * (y / height))
            b = int(bg_dark[2] + (bg_light[2] - bg_dark[2]) * (y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
            
        # Draw comic halftone / radial aura elements
        center_x, center_y = width // 2, height // 2 - 20
        for radius in range(180, 20, -20):
            alpha_color = (
                accent1[0] if radius % 40 == 0 else accent2[0],
                accent1[1] if radius % 40 == 0 else accent2[1],
                accent1[2] if radius % 40 == 0 else accent2[2]
            )
            draw.ellipse(
                [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
                outline=alpha_color,
                width=3
            )
            
        # Draw stylized hero silhouette / geometric comic focal point
        draw.polygon(
            [(center_x, center_y - 70), (center_x + 60, center_y + 50), (center_x - 60, center_y + 50)],
            fill=accent1,
            outline=(255, 255, 255),
            width=3
        )
        draw.ellipse(
            [center_x - 30, center_y - 110, center_x + 30, center_y - 50],
            fill=accent2,
            outline=(255, 255, 255),
            width=3
        )
        
        # Draw comic action burst rays
        for angle in range(0, 360, 45):
            import math
            rad = math.radians(angle)
            x2 = center_x + int(260 * math.cos(rad))
            y2 = center_y + int(260 * math.sin(rad))
            draw.line([(center_x, center_y), (x2, y2)], fill=(255, 255, 255, 80), width=2)
            
        # Draw thick black comic panel frame
        frame_width = 8
        draw.rectangle([0, 0, width, height], outline=(10, 10, 15), width=frame_width)
        
        # Overlay Panel Number Badge
        draw.rectangle([15, 15, 130, 50], fill=(10, 10, 15, 200), outline=accent1, width=2)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()
            
        draw.text((25, 22), f"PANEL {panel_num}", fill=(255, 255, 255), font=font)
        
        # Overlay Art Style Stamp
        draw.rectangle([width - 160, height - 40, width - 15, height - 12], fill=(10, 10, 15, 220))
        draw.text((width - 150, height - 35), f"STYLE: {art_style.upper()}", fill=accent2, font=font)
        
        image.save(filepath, "PNG")
        logger.info(f"Generated fallback stylized image for panel {panel_num}: {filepath}")
        return relative_path
    except Exception as e:
        logger.error(f"Error building fallback image: {e}")
        return "/static/panels/placeholder.png"
