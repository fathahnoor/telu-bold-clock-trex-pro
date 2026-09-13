#!/usr/bin/env python3
"""Generator aset + watchface.json v5 "TELKOM UNIVERSITY" (T-Rex Pro, 360x360).

Revisi besar mengikuti v5/telkom_trex_pro_watchface_spec.md dan
v5/v5_preview-reference.png:

- Latar hitam bersih dengan cincin dan dekorasi vektor. Hanya ilustrasi
  kampus di bawah yang diekstrak dari referensi.
- Logo resmi Telkom University (Wikimedia Commons) dengan wordmark putih.
- Waktu utama: angka jam dan menit putih, dengan titik dua merah.
- Tanggal "Fri, 12 Sep": satu font monospace dan baris yang terpusat.
- Empat gauge melingkar: STEPS, BPM, POWER, KCAL (busur CircleScale).
- Modul solar dinamis "SUNRISE/SUNSET terdekat" (data Sunrise, tipe 12):
  pasangan gambar ikon+label dengan pita tengah transparan untuk angka
  waktu, sehingga hanya satu event tampil.
- Cuaca: suhu + 29 banner kondisi (piktogram + label tertanam).
- Always-on sama dengan mode normal: seluruh elemen tetap tampil.

Output ke build/telu/: 0..N PNG + preview.png 220x220 + watchface.json.
"""

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

W = H = 360
CX = CY = 180
SAFE_R = 174

# ---------------------------------------------------------------------------
# Palet (spesifikasi v5)
# ---------------------------------------------------------------------------
RED = (255, 32, 41)           # Telkom red utama (#FF2029)
WHITE = (255, 255, 255)
WHITE_SOFT = (241, 241, 241)
GRAY_LABEL = (154, 154, 156)
GRAY_RING = (58, 58, 60)
GRAY_RIM = (88, 88, 92)
YELLOW = (255, 210, 26)
HEART = (255, 34, 78)
BLACK = (0, 0, 0)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "telu"
FONTS = ROOT / "assets" / "fonts"
REFERENCE = ROOT / "v5" / "v5_preview-reference.png"
LOGO = ROOT / "assets" / "telkom-university-logo.png"

F_INTER = str(FONTS / "Inter-Variable.ttf")
F_MS = str(FONTS / "Montserrat-SemiBold.ttf")
F_MB = str(FONTS / "Montserrat-Bold.ttf")
F_MM = str(FONTS / "Montserrat-Medium.ttf")
F_DATE = str(FONTS / "CascadiaMono.ttf")
DATE_CELL = (8, 18)

SS = 4  # supersampling teks/angka

# ---------------------------------------------------------------------------
# Geometri gauge, dengan ruang terpisah untuk waktu dan angka maksimum
# ---------------------------------------------------------------------------
GAUGES = {
    "steps": dict(cx=60, cy=158, r=37, icon_cy=138, value_cy=163, label_cy=183),
    "bpm": dict(cx=300, cy=158, r=37, icon_cy=138, value_cy=163, label_cy=183),
    "power": dict(cx=90, cy=239, r=36, icon_cy=221, value_cy=243, label_cy=262),
    "kcal": dict(cx=270, cy=239, r=36, icon_cy=219, value_cy=243, label_cy=262),
}

# Waktu utama
TIME_Y = 143
TIME_CELL = (34, 52)
HOUR_X = 105
MINUTE_X = 187
COLON_DOTS = [(176, 157, 183, 164), (176, 177, 183, 184)]

# Tanggal
DATE_Y = 116

# Nilai metrik (sel + lebar maksimum untuk menghitung X rata tengah)
METRIC_CELL = (10, 17)
WEATHER_CELL = (11, 16)
SOLAR_CELL = (9, 12)

# Modul solar
SOLAR_ICON_XY = (146, 218)
SOLAR_ICON_SIZE = (68, 52)
SOLAR_LABEL_Y = 43
VALUE_SOLAR_CY = 250

# Modul cuaca
WEATHER_BANNER_XY = (239, 61)
WEATHER_BANNER_SIZE = (76, 43)
WEATHER_LABEL_Y = 31
WEATHER_LABEL_CX = 35
WEATHER_ICON_LOCAL = (0, 4)
VALUE_TEMP = (265, 68)

# AM/PM
AMPM_XY = (168, 202)

# AOD
AOD_TIME_Y = 152
AOD_DATE_Y = 240
AOD_BATTERY_Y = 288

# ---------------------------------------------------------------------------
# Util gambar
# ---------------------------------------------------------------------------

def font(path, size, variation=None):
    fnt = ImageFont.truetype(path, size)
    if variation:
        try:
            fnt.set_variation_by_name(variation)
        except Exception:
            pass
    return fnt


def text_size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def render_text(text, fnt, fill, tracking=0.0, pad=2):
    """Render teks (str) dengan letter-spacing, hasil crop rapat."""
    probe = Image.new("RGBA", (8, 8))
    pd = ImageDraw.Draw(probe)
    widths, heights = [], []
    for ch in text:
        box = pd.textbbox((0, 0), ch, font=fnt)
        widths.append(box[2] - box[0])
        heights.append(box[3] - box[1])
    total_w = sum(widths) + tracking * SS * max(0, len(text) - 1) + pad * SS * 2
    h = pd.textbbox((0, 0), text, font=fnt)[3] + pad * SS * 2
    img = Image.new("RGBA", (int(total_w) + 8, int(h) + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = pad * SS
    y = pad * SS
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill + (255,))
        cw, _ = text_size(d, ch, fnt)
        x += cw + tracking * SS
    img = img.resize((max(1, img.width // SS), max(1, img.height // SS)),
                     Image.LANCZOS)
    box = img.getbbox()
    return img.crop(box) if box else img


def make_digit(ch, cell_w, cell_h, font_path, font_size, fill=WHITE,
               variation=None, stretch=1.0):
    """Digit terpusat di sel tetap agar layout firmware deterministik.

    Glyph dirender pada kanvas besar, dipangkas ke bbox tinta, lalu diskalakan
    agar tinggi tinta = tinggi sel dan (opsional) diregangkan horizontal.
    """
    ss = 3
    big = Image.new("RGBA", (font_size * ss * 2, font_size * ss * 2),
                    (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    fnt = font(font_path, font_size * ss, variation)
    box = d.textbbox((0, 0), ch, font=fnt)
    d.text((-box[0], -box[1]), ch, font=fnt, fill=fill + (255,))
    glyph = big.crop((0, 0, box[2] - box[0], box[3] - box[1]))
    if stretch != 1.0:
        glyph = glyph.resize((max(1, int(glyph.width * stretch)),
                              glyph.height), Image.LANCZOS)
    scale = (cell_h * ss) / glyph.height
    glyph = glyph.resize((max(1, int(glyph.width * scale)), cell_h * ss),
                         Image.LANCZOS)
    if glyph.width > cell_w * ss:
        glyph = glyph.resize((cell_w * ss, glyph.height), Image.LANCZOS)
    img = Image.new("RGBA", (cell_w * ss, cell_h * ss), (0, 0, 0, 0))
    img.alpha_composite(glyph, ((img.width - glyph.width) // 2,
                                (img.height - glyph.height) // 2))
    return img.resize((cell_w, cell_h), Image.LANCZOS)


def watch_angle_xy(cx, cy, r, deg):
    rad = math.radians(deg)
    return cx + r * math.sin(rad), cy - r * math.cos(rad)


def arc_pts(cx, cy, r, a0, a1, step=2.0):
    pts = []
    a = a0
    while a <= a1:
        pts.append(watch_angle_xy(cx, cy, r, a))
        a += step
    return pts


def svg_icon(path, width, fill=None):
    """Raster akar SVG (MDI) lalu pewarnaan ulang opsional."""
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    # renderPM menghasilkan RGB berlatar putih. Ambil mask tinta dahulu,
    # baru beri warna, agar latar putih tidak menjadi persegi merah.
    drawing = svg2rlg(str(path))
    raster = renderPM.drawToPIL(drawing, dpi=600, bg=0xFFFFFF)
    mask = ImageOps.invert(raster.convert("L"))
    img = Image.new("RGBA", raster.size, (fill or WHITE) + (255,))
    img.putalpha(mask)
    box = img.getbbox()
    if box:
        img = img.crop(box)
    ratio = width / img.width
    return img.resize((width, max(1, int(img.height * ratio))), Image.LANCZOS)


def icon_battery(width=40, height=22, color=WHITE):
    img = Image.new("RGBA", (width + 10, height + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([5, 10, 5 + width, 10 + height], radius=5,
                        outline=color + (255,), width=3)
    d.rounded_rectangle([5 + width - 14, 4, 5 + width - 4, 12], radius=2,
                        fill=color + (255,))
    return img


def icon_solar(kind="sunset", w=44, h=22):
    """Ikon horizon matahari bergaya referensi."""
    img = Image.new("RGBA", (w, h + 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    horizon = h
    rr = 8
    dome = Image.new("RGBA", (w, h + 10), (0, 0, 0, 0))
    ImageDraw.Draw(dome).ellipse([w // 2 - rr, horizon - rr,
                                  w // 2 + rr, horizon + rr],
                                 fill=RED + (255,))
    img.alpha_composite(dome.crop((0, 0, w, horizon)), (0, 0))
    d.line([3, horizon, w - 3, horizon], fill=RED + (255,), width=3)
    d.line([w // 2 - 9, horizon + 6, w // 2 + 9, horizon + 6],
           fill=RED + (255,), width=3)
    for deg in (-55, -28, 0, 28, 55):
        x1, y1 = watch_angle_xy(w // 2, horizon + 1, rr + 3, deg)
        x2, y2 = watch_angle_xy(w // 2, horizon + 1, rr + 8, deg)
        d.line([x1, y1, x2, y2], fill=RED + (255,), width=2)
    return img


# --- piktogram cuaca -------------------------------------------------------

def pg_sun(d, x, y, s):
    d.ellipse([x + s * 0.30, y + s * 0.30, x + s * 0.70, y + s * 0.70],
              fill=YELLOW + (255,))
    for deg in range(0, 360, 45):
        p1 = watch_angle_xy(x + s / 2, y + s / 2, s * 0.37, deg)
        p2 = watch_angle_xy(x + s / 2, y + s / 2, s * 0.48, deg)
        d.line([p1, p2], fill=YELLOW + (255,), width=max(1, s // 14))


def pg_moon(d, x, y, s):
    d.ellipse([x + s * 0.28, y + s * 0.24, x + s * 0.76, y + s * 0.72],
              fill=(250, 244, 210, 255))
    d.ellipse([x + s * 0.16, y + s * 0.12, x + s * 0.60, y + s * 0.56],
              fill=(0, 0, 0, 255))


def pg_cloud(d, x, y, s, color=(255, 255, 255)):
    c = color + (255,)
    d.ellipse([x + s * 0.10, y + s * 0.42, x + s * 0.46, y + s * 0.80], fill=c)
    d.ellipse([x + s * 0.30, y + s * 0.26, x + s * 0.68, y + s * 0.76], fill=c)
    d.ellipse([x + s * 0.50, y + s * 0.44, x + s * 0.90, y + s * 0.80], fill=c)
    d.rectangle([x + s * 0.18, y + s * 0.62, x + s * 0.82, y + s * 0.80], fill=c)


def pg_rain(d, x, y, s, n=3, color=(255, 255, 255)):
    for i in range(n):
        px = x + s * (0.30 + i * 0.18)
        d.line([px + 2, y + s * 0.74, px - 2, y + s * 0.96],
               fill=color + (255,), width=max(1, s // 12))


def pg_snow(d, x, y, s, n=3, color=(255, 255, 255)):
    for i in range(n):
        px = x + s * (0.30 + i * 0.18)
        d.ellipse([px - 2, y + s * 0.80, px + 2, y + s * 0.94],
                  fill=color + (255,))


def pg_bolt(d, x, y, s, color=YELLOW):
    d.polygon([(x + s * 0.54, y + s * 0.58), (x + s * 0.42, y + s * 0.84),
               (x + s * 0.52, y + s * 0.84), (x + s * 0.44, y + s * 1.02),
               (x + s * 0.68, y + s * 0.74), (x + s * 0.56, y + s * 0.74),
               (x + s * 0.64, y + s * 0.58)], fill=color + (255,))


def pg_fog(d, x, y, s):
    for i in range(3):
        yy = y + s * (0.44 + i * 0.16)
        d.line([x + s * 0.14, yy, x + s * 0.88 - (i % 2) * s * 0.18, yy],
               fill=(255, 255, 255, 255), width=max(2, s // 11))


def pg_wind(d, x, y, s):
    for i in range(3):
        yy = y + s * (0.40 + i * 0.18)
        pts = arc_pts(x + s * 0.28, yy, s * 0.24, -80, 80, 12)
        d.line(pts, fill=(255, 255, 255, 255), width=max(1, s // 12),
               joint="curve")


def pg_sand(d, x, y, s):
    d.polygon([(x + s * 0.5, y + s * 0.30), (x + s * 0.78, y + s * 0.86),
               (x + s * 0.22, y + s * 0.86)], outline=(255, 255, 255, 255),
              width=max(2, s // 12))


CONDITIONS = [
    ("SUNNY", ["sun"]),
    ("PARTLY", ["sun", "cloud"]),
    ("CLOUDY", ["sun", "cloud"]),
    ("OVERCAST", ["cloud"]),
    ("SHOWER", ["cloud", "rain1"]),
    ("RAIN", ["cloud", "rain2"]),
    ("DOWNPOUR", ["cloud", "rain3"]),
    ("STORM", ["cloud", "bolt"]),
    ("SLEET", ["cloud", "sleet"]),
    ("FLURRY", ["cloud", "snow1"]),
    ("SNOW", ["cloud", "snow2"]),
    ("BLIZZARD", ["cloud", "snow3"]),
    ("FOG", ["fog"]),
    ("HAZE", ["fog2"]),
    ("SANDSTORM", ["sand"]),
    ("WINDY", ["wind"]),
    ("CLEAR", ["moon"]),
    ("MOONCLOUD", ["moon", "cloud"]),
    ("NIGHT", ["moon", "cloud2"]),
    ("N SHOWER", ["moon", "cloud", "rain1"]),
    ("N RAIN", ["moon", "cloud", "rain2"]),
    ("N STORM", ["moon", "cloud", "bolt"]),
    ("N SNOW", ["moon", "cloud", "snow2"]),
    ("N FOG", ["moon", "fog"]),
    ("CLOUDY-2", ["cloud"]),
    ("RAIN-2", ["cloud", "rain2"]),
    ("SUNNY-2", ["sun"]),
    ("CLOUDY-3", ["cloud"]),
    ("WEATHER", ["cloud"]),
]


def render_weather_icon(tokens, size=30):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for t in tokens:
        if t == "sun":
            pg_sun(d, 0, 0, size)
        elif t == "moon":
            pg_moon(d, 0, 0, size)
        elif t in ("cloud", "cloud2"):
            pg_cloud(d, 0, size * 0.16, size * 0.92)
        elif t == "rain1":
            pg_rain(d, 0, size * 0.60, size * 0.72, n=1)
        elif t == "rain2":
            pg_rain(d, 0, size * 0.60, size * 0.72, n=2)
        elif t == "rain3":
            pg_rain(d, 0, size * 0.60, size * 0.72, n=3)
        elif t == "bolt":
            pg_bolt(d, 0, size * 0.52, size * 0.76)
        elif t == "snow1":
            pg_snow(d, 0, size * 0.60, size * 0.72, n=1)
        elif t == "snow2":
            pg_snow(d, 0, size * 0.60, size * 0.72, n=2)
        elif t == "snow3":
            pg_snow(d, 0, size * 0.60, size * 0.72, n=3)
        elif t == "sleet":
            pg_rain(d, 0, size * 0.60, size * 0.72, n=2)
            pg_snow(d, 0, size * 0.66, size * 0.72, n=1)
        elif t in ("fog", "fog2"):
            pg_fog(d, 0, size * 0.08, size)
        elif t == "wind":
            pg_wind(d, 0, size * 0.08, size)
        elif t == "sand":
            pg_sand(d, 0, size * 0.02, size)
    return img


def make_weather_banners():
    w, h = WEATHER_BANNER_SIZE
    banners = []
    fnt = font(F_MS, 7 * SS)
    for label, tokens in CONDITIONS:
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        img.alpha_composite(render_weather_icon(tokens, size=23),
                            WEATHER_ICON_LOCAL)
        txt = render_text(label, fnt, GRAY_LABEL, tracking=0.3)
        img.alpha_composite(txt, (WEATHER_LABEL_CX - txt.width // 2,
                                  WEATHER_LABEL_Y))
        banners.append(img)
    return banners


def make_solar_banners():
    w, h = SOLAR_ICON_SIZE
    out = []
    fnt = font(F_MS, 8 * SS)
    for kind, label in (("sunrise", "SUNRISE"), ("sunset", "SUNSET")):
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ic = icon_solar(kind, w=44, h=20).resize((34, 23), Image.LANCZOS)
        img.alpha_composite(ic, ((w - ic.width) // 2, 0))
        txt = render_text(label, fnt, GRAY_LABEL, tracking=1.2)
        img.alpha_composite(txt, ((w - txt.width) // 2, SOLAR_LABEL_Y))
        out.append(img)
    return out


# ---------------------------------------------------------------------------
# Set teks
# ---------------------------------------------------------------------------
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS_FULL = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
             "Saturday", "Sunday"]
DAYS_SHORT = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


def make_month_images():
    return [date_text(m) for m in MONTHS]


def make_weekday_images():
    return [date_text(d.title() + ",") for d in DAYS_SHORT]


def date_text(text):
    """Shared font, advance, color and baseline for every date character."""
    cw, ch = DATE_CELL
    image = Image.new("RGBA", (cw * len(text) * SS, ch * SS))
    draw = ImageDraw.Draw(image)
    fnt = font(F_DATE, 13 * SS, "Bold")
    for i, char in enumerate(text):
        x = i * cw * SS + (cw * SS - fnt.getlength(char)) / 2
        draw.text((x, 14 * SS), char, font=fnt, fill=WHITE + (255,), anchor="ls")
    return image.resize((cw * len(text), ch), Image.LANCZOS)


def make_weekday_short_images():
    fnt = font(F_MS, 12 * SS)
    return [render_text(d, fnt, WHITE, tracking=1.4) for d in DAYS_SHORT]


def make_cell_image(text, font_path, size, fill, cell_h=24, baseline=21,
                    variation=None, tracking=0.0):
    """Teks kecil dengan tinggi sel seragam (untuk suffix/delimiter)."""
    glyph = render_text(text, font(font_path, size * SS, variation), fill,
                        tracking=tracking)
    img = Image.new("RGBA", (max(1, glyph.width), cell_h), (0, 0, 0, 0))
    top = max(0, baseline - glyph.height)
    img.alpha_composite(glyph, (0, top))
    return img


# ---------------------------------------------------------------------------
# Latar bersih dan elemen statis
# ---------------------------------------------------------------------------

def build_background():
    # Hanya ilustrasi kampus diambil dari referensi. Semua area data dibuat
    # dari kanvas bersih sehingga angka, cincin, dan tambalan lama tidak ikut.
    bg = Image.new("RGBA", (W, H), BLACK + (255,))
    reference = Image.open(REFERENCE).convert("RGBA").resize((W, H), Image.LANCZOS)
    campus = reference.crop((35, 278, 325, 341))
    mask = Image.new("L", campus.size, 0)
    md = ImageDraw.Draw(mask)
    for y in range(campus.height):
        md.line((0, y, campus.width, y), fill=min(255, y * 32))
    campus.putalpha(mask)
    bg.alpha_composite(campus, (35, 278))

    # Dekorasi vektor pada resolusi tinggi, konsisten dengan posisi gauge.
    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    def ellipse(box, **kwargs):
        d.ellipse(tuple(round(v * SS) for v in box), **kwargs)

    ellipse((8, 8, 352, 352), outline=GRAY_RIM, width=SS)
    for start, end in ((-140, -116), (-64, -40), (63, 76), (104, 117)):
        d.arc((10 * SS, 10 * SS, 350 * SS, 350 * SS),
              start, end, fill=RED, width=3 * SS)
    for g in GAUGES.values():
        cx, cy, r = g["cx"], g["cy"], g["r"]
        ellipse((cx-r, cy-r, cx+r, cy+r), outline=GRAY_RING, width=5 * SS)
    for box in COLON_DOTS:
        d.rounded_rectangle(tuple(v * SS for v in box), radius=2 * SS, fill=RED)
    for x0, x1 in ((110, 158), (201, 250)):
        d.line((x0 * SS, 207 * SS, x1 * SS, 207 * SS), fill=GRAY_RING, width=SS)
    bg.alpha_composite(layer.resize((W, H), Image.LANCZOS))

    for row, text in enumerate(("HARMONY", "EXCELLENCE", "INTEGRITY")):
        label = render_text(text, font(F_MM, 6 * SS), GRAY_LABEL, tracking=1.0)
        bg.alpha_composite(label, (80 - label.width // 2, 65 + row * 11))
    icons = {
        "steps": svg_icon(ROOT / "assets" / "shoe-sneaker.svg", 24),
        "bpm": svg_icon(ROOT / "assets" / "heart.svg", 22, fill=HEART),
        "kcal": svg_icon(ROOT / "assets" / "fire.svg", 15, fill=RED),
        "power": icon_battery().resize((28, 19), Image.LANCZOS),
    }
    for name, ic in icons.items():
        g = GAUGES[name]
        bg.alpha_composite(ic, (g["cx"] - ic.width // 2,
                                g["icon_cy"] - ic.height // 2))
    for name, text in (("steps", "STEPS"), ("bpm", "BPM"),
                       ("power", "POWER"), ("kcal", "KCAL")):
        g = GAUGES[name]
        label = render_text(text, font(F_MM, 7 * SS), GRAY_LABEL, tracking=1.2)
        bg.alpha_composite(label, (g["cx"] - label.width // 2,
                                   g["label_cy"] - label.height // 2))
    return bg


def logo_image():
    """Logo resmi: wordmark diputihkan, mark buku+U tetap."""
    logo = Image.open(LOGO).convert("RGBA")
    px = logo.load()
    split = int(logo.height * 0.63)
    for y in range(split, logo.height):
        for x in range(logo.width):
            r, g, b, al = px[x, y]
            if al > 0 and max(r, g, b) < 150:
                v = 245 if y < int(logo.height * 0.86) else 225
                px[x, y] = (v, v, v, al)
    target_w = 74
    ratio = target_w / logo.width
    return logo.resize((target_w, int(logo.height * ratio)), Image.LANCZOS)


def build_aod_background():
    aod = Image.new("RGBA", (W, H), BLACK + (255,))
    u_only = Image.open(LOGO).convert("RGBA")
    u_only = u_only.crop((0, 520, u_only.width, 1460))
    box = u_only.getbbox()
    u_only = u_only.crop(box)
    ratio = 30 / u_only.width
    u_only = u_only.resize((30, max(1, int(u_only.height * ratio))),
                           Image.LANCZOS)
    px = u_only.load()
    for y in range(u_only.height):
        for x in range(u_only.width):
            r, g, b, al = px[x, y]
            if al > 0:
                v = int(0.42 * (r + g + b) / 3) + 30
                px[x, y] = (v, v, v, al)
    aod.alpha_composite(u_only, (CX - 15, 58))
    d = ImageDraw.Draw(aod)
    for box in COLON_DOTS:
        d.rounded_rectangle((box[0], box[1] + AOD_TIME_Y - TIME_Y,
                             box[2], box[3] + AOD_TIME_Y - TIME_Y),
                            radius=3, fill=RED + (255,))
    return aod


# ---------------------------------------------------------------------------
# Parameter
# ---------------------------------------------------------------------------

def gauge_circle_scale(g, color="0xFFFF2029", width=5):
    return {
        "Angle": {"X": g["cx"], "Y": g["cy"], "StartAngle": 0.0,
                  "EndAngle": 360.0, "Radius": float(g["r"])},
        "Color": color, "Width": width, "Flatness": 180,
    }


def number_text(x, y, index, count, align="Left", spacing=0, zeropad=0,
                nodata=None, suffix=None, decimal=None, delimiter=None,
                unknown6=0):
    node = {"X": x, "Y": y,
            "ImageRange": {"Language": 2,
                           "ImageRange": {"ImageIndex": index,
                                          "ImagesCount": count}}}
    if nodata is not None:
        node["NoDataImageIndex"] = nodata
    if suffix is not None:
        node["SuffixImage"] = {"Language": 2,
                               "ImageRange": {"ImageIndex": suffix,
                                              "ImagesCount": 1}}
    if decimal is not None:
        node["DecimalPointImageIndex"] = decimal
    if delimiter is not None:
        node["DelimiterImageIndex"] = delimiter
    return {"Image": node, "Alignment": align, "Spacing": spacing,
            "ZeroPadding": zeropad, "Unknown6": unknown6}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    written = []
    state = {"i": 0}

    def save(img, name):
        img.save(OUT / f"{state['i']}.png")
        written.append((state['i'], name))
        state["i"] += 1

    bg = build_background()
    bg.alpha_composite(logo_image(), (143, 17))
    save(bg, "background")
    save(build_aod_background(), "background AOD")
    save(logo_image(), "logo (cadangan)")

    # AM / PM
    for txt in ("AM", "PM"):
        img = render_text(txt, font(F_MS, 11 * SS), GRAY_LABEL, tracking=1.0)
        save(img, f"badge {txt}")

    # Waktu: kedua set digit putih untuk jam dan menit.
    for fill in (WHITE, WHITE):
        for dch in "0123456789":
            save(make_digit(dch, TIME_CELL[0], TIME_CELL[1], F_INTER, 96,
                            fill=fill, variation="Black", stretch=0.71),
                 f"time digit {dch}")
    # Digit nilai metrik.
    for dch in "0123456789":
        save(make_digit(dch, METRIC_CELL[0], METRIC_CELL[1], F_INTER, 27,
                        fill=WHITE, variation="Black", stretch=0.55),
             f"metric digit {dch}")    # Digit waktu solar.
    for dch in "0123456789":
        save(make_digit(dch, SOLAR_CELL[0], SOLAR_CELL[1], F_INTER, 19,
                        fill=WHITE, variation="Black", stretch=0.78),
             f"solar digit {dch}")
    # Digit suhu cuaca.
    for dch in "0123456789":
        save(make_digit(dch, WEATHER_CELL[0], WEATHER_CELL[1], F_INTER, 25,
                        fill=WHITE, variation="Black", stretch=0.80),
             f"weather digit {dch}")

    # Titik dua solar + nodata + suffix/delimiter.
    colon = Image.new("RGBA", (7, 14), (0, 0, 0, 0))
    dc = ImageDraw.Draw(colon)
    dc.rounded_rectangle([1, 1, 6, 5], radius=2, fill=WHITE + (255,))
    dc.rounded_rectangle([1, 9, 6, 13], radius=2, fill=WHITE + (255,))
    save(colon, "solar colon")
    save(render_text("--:--", font(F_INTER, 18 * SS, "Black"), WHITE,
                     tracking=0.5), "solar nodata")
    save(make_cell_image("%", F_INTER, 18, WHITE_SOFT, cell_h=17,
                         baseline=15, variation="Black", tracking=0),
         "percent")
    save(make_cell_image(",", F_INTER, 18, WHITE, cell_h=17, baseline=17,
                         variation="Black"), "comma")
    save(make_cell_image("\u00b0C", F_INTER, 13, WHITE, cell_h=16,
                         baseline=15, variation="Black"), "degree")
    save(render_text("--", font(F_INTER, 22 * SS, "Black"), WHITE), "nodata")

    # Bulan & hari.
    for m, img in zip(MONTHS, make_month_images()):
        save(img, f"month {m}")
    for dname, img in zip(DAYS_FULL, make_weekday_images()):
        save(img, f"day {dname}")
    for dname, img in zip(DAYS_SHORT, make_weekday_short_images()):
        save(img, f"AOD day {dname}")

    # Banner cuaca (29) + ikon solar (2).
    for (label, _), img in zip(CONDITIONS, make_weather_banners()):
        save(img, f"weather {label}")
    for kind, img in zip(("sunrise", "sunset"), make_solar_banners()):
        save(img, f"solar {kind}")
    for digit in "0123456789":
        save(date_text(digit), f"date digit {digit}")

    # ------------------------- indeks aset --------------------------------
    I_BG = 0
    I_AOD = 1
    I_LOGO = 2
    I_AM, I_PM = 3, 4
    I_TIME_H, I_TIME_M = 5, 15
    I_METRIC = 25
    I_SOLAR_D = 35
    I_WEATHER_D = 45
    I_SOLAR_COLON = 55
    I_SOLAR_NODATA = 56
    I_PCT = 57
    I_COMMA = 58
    I_DEG = 59
    I_NODATA = 60
    I_MONTH = 61
    I_DAYFULL = 73
    I_DAYSHORT = 80
    I_WEATHER = 87
    I_SOLAR_ICON = 116
    I_DATE_D = 118
    assert state["i"] == 128, f"jumlah aset tak terduga: {state['i']}"

    # ------------------------- parameter ----------------------------------
    time_digital = {
        "HoursMinutesSeconds": [
            {"Type": 0, "Independent": True,
             "Text": number_text(HOUR_X, TIME_Y, I_TIME_H, 10, zeropad=1)},
            {"Type": 1, "Independent": True,
             "Text": number_text(MINUTE_X, TIME_Y, I_TIME_M, 10, zeropad=1)},
        ],
        "AM": {"Coordinates": {"X": AMPM_XY[0], "Y": AMPM_XY[1]},
               "ImageRange": {"Language": 2,
                              "ImageRange": {"ImageIndex": I_AM,
                                             "ImagesCount": 1}}},
        "PM": {"Coordinates": {"X": AMPM_XY[0], "Y": AMPM_XY[1]},
               "ImageRange": {"Language": 2,
                              "ImageRange": {"ImageIndex": I_PM,
                                             "ImagesCount": 1}}},
    }

    # Eleven fixed advances: "Fri, 12 Sep". Every date has the same width,
    # so the complete line stays centered without runtime repositioning.
    week_x = CX - 11 * DATE_CELL[0] // 2
    day_x = week_x + 5 * DATE_CELL[0]
    month_x = week_x + 8 * DATE_CELL[0]

    date_system = {
        "YearMonthDay": [
            {"Type": 2, "Independent": True,
             "Text": number_text(day_x, DATE_Y, I_DATE_D, 10, zeropad=1)},
            {"Type": 1, "Independent": True,
             "Text": number_text(month_x, DATE_Y, I_MONTH, 12, zeropad=0,
                                 unknown6=1)},
        ],
        "Week": {"Independent": True,
                 "Text": number_text(week_x, DATE_Y, I_DAYFULL, 7,
                                     zeropad=0, unknown6=1)},
    }

    def value_text(center_x, max_digits, y, extra=None):
        suffix_width = percent_width if extra and "suffix" in extra else 0
        # Firmware centers the number within its maximum-digit box and
        # appends the unit afterward. Compensate for the unit as a group.
        x = center_x - (max_digits * METRIC_CELL[0] + 1) // 2 - suffix_width // 2
        return number_text(x, y, I_METRIC, 10, nodata=I_NODATA,
                           align="Center", **(extra or {}))

    percent_width = Image.open(OUT / f"{I_PCT}.png").width

    data_system = [
        {"Type": "Battery",
         "CircleScale": gauge_circle_scale(GAUGES["power"]),
         "NumberSequence": {"Independent": True,
                            "Text": value_text(GAUGES["power"]["cx"], 3,
                                               GAUGES["power"]["value_cy"] - 8,
                                               {"suffix": I_PCT})}},
        {"Type": "Steps",
         "CircleScale": gauge_circle_scale(GAUGES["steps"]),
         "NumberSequence": {"Independent": True,
                            "Text": value_text(GAUGES["steps"]["cx"], 5,
                                               GAUGES["steps"]["value_cy"] - 8,
                                               {"delimiter": I_COMMA})}},
        {"Type": "Calories",
         "CircleScale": gauge_circle_scale(GAUGES["kcal"]),
         "NumberSequence": {"Independent": True,
                            "Text": value_text(GAUGES["kcal"]["cx"], 4,
                                               GAUGES["kcal"]["value_cy"] - 8)}},
        {"Type": "HeartRate",
         "CircleScale": gauge_circle_scale(GAUGES["bpm"]),
         "NumberSequence": {"Independent": True,
                            "Text": value_text(GAUGES["bpm"]["cx"], 3,
                                               GAUGES["bpm"]["value_cy"] - 8)}},
        {"Type": "Weather",
         "NumberSequence": {"Independent": True,
                            "Text": number_text(VALUE_TEMP[0], VALUE_TEMP[1],
                                                I_WEATHER_D, 10, nodata=I_NODATA,
                                                suffix=I_DEG)}},
        {"Type": "Weather",
         "Linear": {"Segments": {"X": WEATHER_BANNER_XY[0],
                                 "Y": WEATHER_BANNER_XY[1]},
                    "ImageRange": {"ImageIndex": I_WEATHER,
                                   "ImagesCount": 29}}},
        {"Type": "Sunrise",
         "NumberSequence": {"Independent": True,
                            "Text": number_text(0, 0, I_SOLAR_D, 10,
                                                zeropad=1,
                                                decimal=I_SOLAR_COLON,
                                                nodata=I_SOLAR_NODATA)}},
        {"Type": "Sunrise",
         "Linear": {"Segments": {"X": SOLAR_ICON_XY[0],
                                 "Y": SOLAR_ICON_XY[1]},
                    "ImageRange": {"ImageIndex": I_SOLAR_ICON,
                                   "ImagesCount": 2}}},
    ]
    solar_w = 4 * SOLAR_CELL[0] + 7
    data_system[6]["NumberSequence"]["Text"]["Image"]["X"] = 180 - solar_w // 2
    data_system[6]["NumberSequence"]["Text"]["Image"]["Y"] = VALUE_SOLAR_CY - 6  # noqa: E501

    # Always-on memakai seluruh layout normal, termasuk cuaca dan gauge.
    idle = {
        "Time": {"Digital": time_digital},
        "Date": date_system,
        "Data": data_system,
        "BackgroundImageIndex": I_BG,
    }

    preview_index = state["i"]
    params = {
        "Background": {"Preview": {"Language": 2,
                                   "ImageRange": {"ImageIndex": preview_index,
                                                  "ImagesCount": 1}},
                       "ImageIndex": I_BG},
        "Time": {"Digital": time_digital},
        "System": {"Date": date_system, "Data": data_system},
        "IdleScreen": idle,
    }
    (OUT / "watchface.json").write_text(json.dumps(params, indent=2))
    if not (OUT / "preview.png").exists():
        Image.new("RGBA", (220, 220), BLACK + (255,)).save(OUT / "preview.png")

    print(f"total aset: {state['i']} + preview 220 (indeks {preview_index})")
    for i, n in written:
        print(f"  {i:3d} {n}")


if __name__ == "__main__":
    main()
