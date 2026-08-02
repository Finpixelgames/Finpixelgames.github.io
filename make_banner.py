"""Generate Beyond Orbit feature graphic from landscape menu background."""
from PIL import Image, ImageDraw, ImageFont

# --- Config ---
OUTPUT_W, OUTPUT_H = 1024, 500
BG_PATH = r"C:\Users\Koti\Desktop\FinPixel\projects\beyond-orbit\assets\images\menu_bg_landscape.png"
OUT_PATH = r"C:\Users\Koti\Desktop\FinPixel\website\beyond-orbit\feature_graphic.png"
STORE_PATH = r"C:\Users\Koti\Desktop\FinPixel\projects\beyond-orbit\store\graphics\feature_graphic.png"

# --- Load and crop/resize background ---
bg = Image.open(BG_PATH).convert("RGBA")
# Crop off bottom-right watermark area, then resize to banner
# Crop bottom 80px and right 60px
bg = bg.crop((0, 0, bg.width - 60, bg.height - 80))
bg = bg.resize((OUTPUT_W, OUTPUT_H), Image.LANCZOS)

draw = ImageDraw.Draw(bg)

# --- Fonts ---
font_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 64)
font_sub = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 24)

title = "BEYOND ORBIT"
subtitle = "Explore. Trade. Fight. Survive."

# --- Measure text ---
title_bbox = draw.textbbox((0, 0), title, font=font_title)
title_w = title_bbox[2] - title_bbox[0]
title_h = title_bbox[3] - title_bbox[1]

sub_bbox = draw.textbbox((0, 0), subtitle, font=font_sub)
sub_w = sub_bbox[2] - sub_bbox[0]

# --- Position: center in right half ---
right_center_x = OUTPUT_W * 0.74
title_x = int(right_center_x - title_w / 2)
sub_x = int(right_center_x - sub_w / 2)

# Ensure right margin
margin = 28
title_x = min(title_x, OUTPUT_W - title_w - margin)
sub_x = min(sub_x, OUTPUT_W - sub_w - margin)

# Vertical center
total_h = title_h + 16 + 24
start_y = (OUTPUT_H - total_h) // 2

# --- Draw text shadows ---
for dx, dy in [(3,3), (2,2), (1,1)]:
    draw.text((title_x+dx, start_y+dy), title, font=font_title, fill=(0, 0, 0, 200))
    draw.text((sub_x+dx, start_y+title_h+16+dy), subtitle, font=font_sub, fill=(0, 0, 0, 180))

# --- Draw main text ---
draw.text((title_x, start_y), title, font=font_title, fill=(255, 255, 255, 245))
draw.text((sub_x, start_y + title_h + 16), subtitle, font=font_sub, fill=(200, 215, 255, 230))

# --- Save ---
final = bg.convert("RGB")
final.save(OUT_PATH, "PNG")
final.save(STORE_PATH, "PNG")
print(f"Saved: {OUT_PATH}")
