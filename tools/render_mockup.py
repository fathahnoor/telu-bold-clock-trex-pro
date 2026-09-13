#!/usr/bin/env python3
"""Render mockup v5 dari folder build (watchface.json + PNG).

Pakai:
  python tools/render_mockup.py build/telu out/mockup_360.png [--small out.png]
Skenario: --time 1028 --steps 8426 --hr 72 --batt 82 --kcal 560 --temp 29
  --cond 2 (indeks kondisi cuaca) --solar sunset --wday 4 --day 12
  --mode idle  (always-on)
"""

import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

RED = (255, 32, 41, 255)
GRAY_LABEL = (154, 154, 156)


def load(folder):
    folder = Path(folder)
    params = json.loads((folder / "watchface.json").read_text())
    imgs = {}
    for p in folder.glob("[0-9]*.png"):
        imgs[int(p.stem)] = Image.open(p).convert("RGBA")
    return params, imgs


def as_list(value):
    return value if isinstance(value, list) else [value]


def imgs_range(rng):
    base = rng["ImageIndex"]
    return [base + i for i in range(rng["ImagesCount"])]


def number_start(text_cfg, cell_width, actual_width, max_digits):
    """UIHH alignment is relative to a reserved digit box, not an X anchor.

    Matches Draw_dagital_text in the SashaCX75 editor. Suffixes follow
    the aligned number, so their width is compensated in the stored X.
    """
    x = text_cfg["Image"]["X"]
    reserved = cell_width * max_digits + 1
    reserved += max(0, text_cfg.get("Spacing", 0)) * (max_digits - 1)
    if text_cfg.get("Alignment") == "Center":
        x += reserved // 2 - actual_width // 2
    elif text_cfg.get("Alignment") == "Right":
        x += reserved - actual_width
    return x


def draw_number(canvas, imgs, text_cfg, digits, value=None, max_digits=None):
    node = text_cfg["Image"]
    x, y = node["X"], node["Y"]
    rng = node["ImageRange"]["ImageRange"]
    base = rng["ImageIndex"]
    if digits is None:
        canvas.alpha_composite(imgs[node["NoDataImageIndex"]], (x, y))
        return
    digits = str(digits)
    if text_cfg.get("ZeroPadding") and len(digits) < 2:
        digits = digits.rjust(2, "0")
    delim = node.get("DelimiterImageIndex")
    negative = digits.startswith("-")
    if delim is not None and len(digits) > 3 and not negative:
        digits = digits[:-3] + "," + digits[-3:]
    cells = []
    for ch in digits:
        if ch == ",":
            cell = imgs[delim]
        elif ch == "-":
            if delim is None:
                raise ValueError("Negative value requires a delimiter sprite")
            cell = imgs[delim]
        else:
            cell = imgs[base + int(ch)]
        cells.append(cell)
    spacing = text_cfg.get("Spacing", 0)
    width = sum(cell.width for cell in cells) + spacing * max(0, len(cells) - 1)
    x = number_start(text_cfg, imgs[base].width, width, max_digits or len(cells))
    for cell in cells:
        canvas.alpha_composite(cell, (int(x), int(y)))
        x += cell.width + spacing
    if cells:
        x -= spacing
    suffix = node.get("SuffixImage")
    if suffix:
        s = imgs[suffix["ImageRange"]["ImageIndex"]]
        canvas.alpha_composite(s, (int(x), int(y)))
        x += s.width


def draw_gauge(canvas, imgs, entry, frac, radius_offset=0):
    if "CircleScale" not in entry or frac is None:
        return
    angle = entry["CircleScale"]["Angle"]
    ss = 4
    layer = Image.new("RGBA", (canvas.width * ss, canvas.height * ss))
    d = ImageDraw.Draw(layer)
    cx, cy, r = angle["X"], angle["Y"], angle["Radius"] + radius_offset
    start = angle["StartAngle"]
    span = (angle["EndAngle"] - start) % 360 or 360
    end = start + span * max(0.0, min(1.0, frac))
    w = entry["CircleScale"].get("Width", 7)
    if frac <= 0:
        return
    box = [(cx - r) * ss, (cy - r) * ss, (cx + r) * ss, (cy + r) * ss]
    if end - start >= 360:
        # Modulo would turn 360 degrees into a zero-length arc.
        d.ellipse(box, outline=RED, width=w * ss)
    else:
        d.arc(box, start=(start + 270) % 360, end=(end + 270) % 360,
              fill=RED, width=w * ss)
    canvas.alpha_composite(layer.resize(canvas.size, Image.LANCZOS))


def draw_time(canvas, imgs, block, args, date_shift=(0, 0)):
    sx, sy = date_shift
    hms = {e["Type"]: e for e in as_list(block["HoursMinutesSeconds"])}
    hh, mm = args["time"][:2], args["time"][2:]
    for typ, digits in ((0, hh), (1, mm)):
        txt = hms[typ]["Text"]
        node = txt["Image"]
        node = dict(node, X=node["X"] + sx, Y=node["Y"] + sy)
        draw_number(canvas, imgs, dict(txt, Image=node), digits)
    if "AM" in block and args.get("ampm") != "none":
        ap = block["AM" if args.get("ampm", "AM") == "AM" else "PM"]
        rng = ap["ImageRange"]["ImageRange"]
        badge = imgs[rng["ImageIndex"]]
        canvas.alpha_composite(badge, (ap["Coordinates"]["X"] + sx,
                                       ap["Coordinates"]["Y"] + sy))


def draw_date(canvas, imgs, block, args):
    ymd = {e["Type"]: e for e in as_list(block["YearMonthDay"])}
    e = ymd.get(2)
    if e is not None:
        txt = e["Text"]
        draw_number(canvas, imgs, txt, args["day"])
    e = ymd.get(1)
    if e is not None:
        txt = e["Text"]
        rng = txt["Image"]["ImageRange"]["ImageRange"]
        month = int(args.get("month", 9))
        img = imgs[rng["ImageIndex"] + month - 1]
        canvas.alpha_composite(img, (txt["Image"]["X"], txt["Image"]["Y"]))
    week = block.get("Week")
    if week:
        txt = week["Text"]
        rng = txt["Image"]["ImageRange"]["ImageRange"]
        wday = int(args.get("wday", 4))
        img = imgs[rng["ImageIndex"] + wday]
        canvas.alpha_composite(img, (txt["Image"]["X"], txt["Image"]["Y"]))


def draw_data(canvas, imgs, data_list, args):
    data = {e["Type"]: e for e in as_list(data_list)}
    if "Steps" in data:
        draw_gauge(canvas, imgs, data["Steps"], args["steps"] / 10000.0)
        txt = data["Steps"]["NumberSequence"]["Text"]
        draw_number(canvas, imgs, txt, args["steps"], max_digits=5)
    if "HeartRate" in data:
        draw_gauge(canvas, imgs, data["HeartRate"], args["hr"] / 220.0)
        txt = data["HeartRate"]["NumberSequence"]["Text"]
        draw_number(canvas, imgs, txt, args["hr"], max_digits=3)
    if "Calories" in data:
        draw_gauge(canvas, imgs, data["Calories"], args["kcal"] / 1000.0)
        txt = data["Calories"]["NumberSequence"]["Text"]
        draw_number(canvas, imgs, txt, args["kcal"], max_digits=4)
    if "Battery" in data:
        draw_gauge(canvas, imgs, data["Battery"], args["batt"] / 100.0)
        txt = data["Battery"]["NumberSequence"]["Text"]
        draw_number(canvas, imgs, txt, args["batt"], max_digits=3)

    # Cuaca: ikon (Linear) + suhu (NumberSequence).
    weather = [e for e in as_list(data_list) if e["Type"] == "Weather"]
    for e in weather:
        if "Linear" in e:
            seg = e["Linear"]["Segments"]
            rng = e["Linear"]["ImageRange"]
            idx = rng["ImageIndex"] + int(args.get("cond", 2))
            canvas.alpha_composite(imgs[idx], (seg["X"], seg["Y"]))
        elif "NumberSequence" in e:
            txt = e["NumberSequence"]["Text"]
            draw_number(canvas, imgs, txt, args["temp"])

    # Solar: event terdekat + pasangan ikon.
    solar = [e for e in as_list(data_list) if e["Type"] == "Sunrise"]
    show_sunset = args.get("solar", "sunset") == "sunset"
    for e in solar:
        if "Linear" in e:
            seg = e["Linear"]["Segments"]
            rng = e["Linear"]["ImageRange"]
            idx = rng["ImageIndex"] + (1 if show_sunset else 0)
            canvas.alpha_composite(imgs[idx], (seg["X"], seg["Y"]))
        elif "NumberSequence" in e:
            txt = e["NumberSequence"]["Text"]
            node = txt["Image"]
            solar_time = args["solartime"] if show_sunset else args["sunrisetime"]
            x = node["X"]
            y = node["Y"]
            for i, ch in enumerate(solar_time):
                if i == 2:
                    canvas.alpha_composite(imgs[node["DecimalPointImageIndex"]],
                                           (int(x), int(y)))
                    x += imgs[node["DecimalPointImageIndex"]].width
                cell = imgs[node["ImageRange"]["ImageRange"]["ImageIndex"] +
                            int(ch)]
                canvas.alpha_composite(cell, (int(x), int(y)))
                x += cell.width


def main(argv):
    folder = Path(argv[1])
    out = Path(argv[2])
    args = {"time": "1028", "steps": "8426", "hr": "72", "batt": "82",
            "kcal": "560", "temp": "29", "cond": "2", "solar": "sunset",
            "wday": "4", "day": "12", "month": "9", "ampm": "AM",
            "solartime": "1802", "sunrisetime": "0546", "mode": "main"}
    small = None
    i = 3
    while i < len(argv):
        if argv[i].startswith("--"):
            key = argv[i][2:]
            if key == "small":
                small = Path(argv[i + 1])
                i += 2
                continue
            args[key] = argv[i + 1]
            i += 2
        else:
            i += 1

    params, imgs = load(folder)
    for key in ("steps", "hr", "batt", "kcal", "temp", "cond", "wday", "day",
                "month"):
        args[key] = int(args[key])
    if args["mode"] == "idle":
        idle = params["IdleScreen"]
        canvas = imgs[idle["BackgroundImageIndex"]].copy()
        draw_time(canvas, imgs, idle["Time"]["Digital"], args)
        draw_date(canvas, imgs, idle["Date"], args)
        draw_data(canvas, imgs, idle["Data"], args)
    else:
        canvas = imgs[params["Background"]["ImageIndex"]].copy()
        draw_time(canvas, imgs, params["Time"]["Digital"], args)
        draw_date(canvas, imgs, params["System"]["Date"], args)
        draw_data(canvas, imgs, params["System"]["Data"], args)

    canvas.save(out)
    print("mockup:", out)
    if small:
        canvas.resize((220, 220), Image.LANCZOS).save(small)
        print("small:", small)


if __name__ == "__main__":
    main(sys.argv)
