"""Regenerate the install icons from the library's simple monogram."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "icons"
OUT.mkdir(exist_ok=True)

for size in (192, 512):
    image = Image.new("RGB", (size, size), "#f6f2e9")
    draw = ImageDraw.Draw(image)
    margin = round(size * 0.15)
    draw.rounded_rectangle((margin, margin, size - margin, size - margin), radius=round(size * 0.16), fill="#2e5141")
    font_path = Path("C:/Windows/Fonts/georgia.ttf")
    font = ImageFont.truetype(str(font_path), round(size * 0.36)) if font_path.exists() else ImageFont.load_default()
    draw.text((size * 0.49, size * 0.50), "IL", font=font, anchor="mm", fill="#f6f2e9")
    draw.line((size * 0.72, size * 0.19, size * 0.72, size * 0.31), fill="#d6e4a6", width=round(size * 0.025))
    draw.line((size * 0.66, size * 0.25, size * 0.78, size * 0.25), fill="#d6e4a6", width=round(size * 0.025))
    image.save(OUT / f"icon-{size}.png", optimize=True)
