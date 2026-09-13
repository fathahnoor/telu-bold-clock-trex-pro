#!/usr/bin/env python3
"""Generator digit PNG 0-9 untuk jam besar (tinggi 72px, putih, font tebal).

Digit ini siap dipakai untuk widget TEXT_IMG / digit-image pada editor
watchface T-Rex Pro legacy (font_array 0.png .. 9.png).
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_assets import WHITE, load_font

OUT = Path(__file__).resolve().parent.parent / "assets" / "360x360" / "digits"
DIGIT_H = 72


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    font = load_font(84, bold=True)
    for d in "0123456789":
        img = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
        dr = ImageDraw.Draw(img)
        dr.text((60, 60), d, font=font, fill=WHITE + (255,), anchor="mm")
        bbox = img.getbbox()
        img = img.crop(bbox)
        # resize proporsional agar tinggi konsisten 72px
        w = round(img.width * DIGIT_H / img.height)
        img = img.resize((w, DIGIT_H), Image.LANCZOS)
        img.save(OUT / f"{d}.png")
        print(f"  digits/{d}.png  ({img.width}x{img.height})")


if __name__ == "__main__":
    main()
