"""Combine decoded-BIN previews for review, without modifying dial pixels."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent


def sheet(files, target, columns=3):
    canvas = Image.new("RGB", (columns * 380, ((len(files)+columns-1)//columns)*400), (18,18,20))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(str(ROOT / "assets/fonts/Inter-Variable.ttf"), 14)
    for i, (label, path) in enumerate(files):
        x, y = (i % columns)*380, (i // columns)*400
        canvas.paste(Image.open(path).convert("RGB"), (x+10, y+28))
        draw.text((x+14, y+6), label, font=font, fill="white")
    canvas.save(ROOT / target)


if __name__ == "__main__":
    sheet([(n, ROOT / f"out/{p}.png") for n,p in [
        ("Siang 10:28", "preview"), ("Sebelum sunrise 05:20", "preview_sunrise"),
        ("Sesudah sunset 20:30", "preview_after_sunset"), ("Data maksimum", "preview_max"),
        ("Data minimum", "preview_zero"), ("Always-on 10:28", "preview_idle")]], "out/scenarios.png")
    sheet([(p.stem[:2]+":"+p.stem[2:], p) for p in sorted((ROOT/"out/stress").glob("*.png"))], "out/time-stress.png")
