#!/usr/bin/env python3
"""Generator asset watchface TEL-U untuk Amazfit T-Rex Pro (360x360).

Menghasilkan:
  assets/360x360/bg.png          - background hitam + ornamen ring TEL-U
  assets/360x360/branding.png    - teks "TELKOM UNIVERSITY"
  assets/360x360/ampm.png        - segitiga penanda AM/PM (merah Tel-U)
  assets/preview/preview_220.png - preview 220x220 (mockup layout penuh)

Palet warna resmi Telkom University (lihat docs/research/telu-colors.md).
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W = H = 360
PREVIEW = 220

# Palet resmi Telkom University
TELU_RED = (237, 30, 40)      # ED1E28
TELU_MAROON = (182, 37, 42)   # B6252A
GRAY_DARK = (85, 86, 91)      # 55565B
GRAY_LIGHT = (149, 149, 151)  # 959597
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ROOT = Path(__file__).resolve().parent.parent
OUT_BG = ROOT / "assets" / "360x360"
OUT_PREVIEW = ROOT / "assets" / "preview"


def load_font(size: int, bold: bool = False):
    """Coba beberapa font sistem umum (Windows/Linux), fallback ke default."""
    candidates = [
        "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_ring(draw, cx, cy, r, color, width, alpha):
    """Lingkaran dengan alpha (komposit ke layer RGBA terpisah)."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color + (alpha,), width=width)
    return layer


def make_background() -> Image.Image:
    """Background hitam AMOLED + ornamen ring ganda TEL-U + tick marker."""
    bg = Image.new("RGBA", (W, H), BLACK + (255,))
    cx = cy = W // 2

    # Ring ganda khas lingkaran logo TEL-U
    bg.alpha_composite(draw_ring(ImageDraw.Draw(bg), cx, cy, 170, TELU_MAROON, 1, 90))
    bg.alpha_composite(draw_ring(ImageDraw.Draw(bg), cx, cy, 163, TELU_RED, 1, 64))

    # Tick marker merah di jam 12/3/6/9 (di luar ring, mengikuti bezel)
    d = ImageDraw.Draw(bg)
    for angle, r_in, r_out in [(270, 172, 180), (0, 172, 180), (90, 172, 180), (180, 172, 180)]:
        import math
        rad = math.radians(angle)
        x1, y1 = cx + r_in * math.cos(rad), cy + r_in * math.sin(rad)
        x2, y2 = cx + r_out * math.cos(rad), cy + r_out * math.sin(rad)
        d.line([x1, y1, x2, y2], fill=TELU_RED + (255,), width=3)

    return bg


def make_branding() -> Image.Image:
    """Teks 'TELKOM UNIVERSITY' putih dengan tracking lebar + garis merah di kiri-kanan."""
    img = Image.new("RGBA", (200, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = load_font(13, bold=True)
    text = "TELKOM UNIVERSITY"
    # tracking manual: gambar per karakter dengan spasi ekstra
    x = 14
    for ch in text:
        d.text((x, 4), ch, font=font, fill=WHITE + (255,))
        bbox = d.textbbox((0, 0), ch, font=font)
        x += (bbox[2] - bbox[0]) + 3
    # aksen garis merah kiri & kanan
    d.line([2, 14, 10, 14], fill=TELU_RED + (255,), width=2)
    d.line([x + 4, 14, x + 12, 14], fill=TELU_RED + (255,), width=2)
    return img.crop(img.getbbox() if img.getbbox() else (0, 0, 200, 24))


def make_ampm(label: str = "AM") -> Image.Image:
    """Segitiga merah Tel-U dengan teks putih di dalamnya (tiruan panah rigger)."""
    img = Image.new("RGBA", (72, 56), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # segitiga mengarah kiri (seperti ►AM pada rigger asli, dibalik jadi ◄AM)
    d.polygon([(70, 4), (70, 52), (6, 28)], fill=TELU_RED + (255,))
    font = load_font(15, bold=True)
    d.text((40, 18), label, font=font, fill=WHITE + (255,), anchor="mm")
    return img.crop(img.getbbox())


def render_mockup(bg: Image.Image) -> Image.Image:
    """Mockup layout lengkap untuk preview (bukan asset final - hanya visualisasi)."""
    img = bg.copy()
    d = ImageDraw.Draw(img)

    f_big = load_font(64, bold=True)
    f_small = load_font(20, bold=True)
    f_label = load_font(16)
    f_tiny = load_font(14)

    # Jam kecil atas + titik aktivitas merah
    d.text((200, 14), "10:42", font=f_small, fill=WHITE + (255,))
    d.ellipse([176, 16, 190, 30], fill=TELU_RED + (255,))

    # Kolom kiri: KCAL / STEP / HR
    d.text((16, 48), "KCAL", font=f_label, fill=GRAY_LIGHT + (255,))
    d.text((16, 70), "29", font=f_small, fill=WHITE + (255,))
    d.line([16, 104, 126, 104], fill=GRAY_DARK + (255,), width=2)
    d.text((16, 114), "STEP", font=f_label, fill=TELU_RED + (255,))
    d.text((16, 136), "1115", font=f_small, fill=WHITE + (255,))
    d.line([16, 170, 126, 170], fill=GRAY_DARK + (255,), width=2)
    d.text((16, 180), "HR", font=f_label, fill=TELU_RED + (255,))
    d.text((16, 202), "97", font=f_small, fill=WHITE + (255,))
    # indikator baterai kecil (petir + persen)
    d.text((16, 238), "92%", font=f_tiny, fill=TELU_MAROON + (255,))

    # Jam besar 05:32
    d.text((172, 96), "05", font=f_big, fill=WHITE + (255,))
    d.text((172, 180), "32", font=f_big, fill=WHITE + (255,))

    # Segitiga AM
    ampm = make_ampm("AM")
    img.alpha_composite(ampm, (258, 158))

    # Tanggal
    d.text((172, 268), "SAB 12", font=f_small, fill=TELU_RED + (255,))

    # Branding
    branding = make_branding()
    img.alpha_composite(branding, ((W - branding.width) // 2, 326))

    return img


def main():
    OUT_BG.mkdir(parents=True, exist_ok=True)
    OUT_PREVIEW.mkdir(parents=True, exist_ok=True)

    bg = make_background()
    bg.save(OUT_BG / "bg.png")

    branding = make_branding()
    branding.save(OUT_BG / "branding.png")

    ampm = make_ampm("AM")
    ampm.save(OUT_BG / "ampm.png")

    mockup = render_mockup(bg)
    mockup.save(OUT_PREVIEW / "preview_360.png")
    mockup.resize((PREVIEW, PREVIEW), Image.LANCZOS).save(OUT_PREVIEW / "preview_220.png")

    print("Assets generated:")
    for p in sorted(OUT_BG.rglob("*.png")) + sorted(OUT_PREVIEW.rglob("*.png")):
        print(f"  {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
