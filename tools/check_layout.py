"""Reject overlapping visible pixels in all dynamic sprite variants.

Checks the generated layout or the unpacked BIN with the same coordinates.
Opaque backgrounds, static labels/icons, and gauge tracks are obstacles.
"""
import sys
import math
from itertools import combinations
from pathlib import Path

from PIL import Image, ImageChops

from render_mockup import load, as_list, number_start

MAX_DIGITS = {"Battery": 3, "Steps": 5, "HeartRate": 3, "Calories": 4,
              "Weather": 2, "Sunrise": 4}


def layout_errors(folder):
    params, images = load(folder)
    errors = []

    def mask():
        return Image.new("L", (360, 360))

    def stamp(target, index, x, y):
        layer = mask()
        ink = images[index].getchannel("A").point(lambda a: 255 if a > 48 else 0)
        layer.paste(ink, (int(x), int(y)))
        return ImageChops.lighter(target, layer)

    def range_mask(index, count, x, y):
        result = mask()
        for i in range(count):
            result = stamp(result, index + i, x, y)
        return result

    def number(txt, maximum, solar=False, signed=False):
        node = txt["Image"]
        rng = node["ImageRange"]["ImageRange"]
        base, count = rng["ImageIndex"], rng["ImagesCount"]
        result = mask()
        # Each length moves the suffix or delimiter. Include them all.
        minimum = maximum if solar else (2 if txt.get("ZeroPadding") else 1)
        for length in range(minimum, maximum + 1):
            x, y = node["X"], node["Y"]
            width = images[base].width * length
            separators = []
            if solar:
                separators.append(node["DecimalPointImageIndex"])
            elif length > 3 and "DelimiterImageIndex" in node:
                separators.append(node["DelimiterImageIndex"])
            width += sum(images[i].width for i in separators)
            width += txt.get("Spacing", 0) * (length + len(separators) - 1)
            x = number_start(txt, images[base].width, width, maximum)
            for i in range(length):
                separator = (node.get("DecimalPointImageIndex") if solar and i == 2
                             else node.get("DelimiterImageIndex")
                             if length > 3 and i == length - 3 else None)
                if separator is not None:
                    result = stamp(result, separator, x, y)
                    x += images[separator].width
                result = ImageChops.lighter(result, range_mask(base, count, x, y))
                x += images[base].width + txt.get("Spacing", 0)
            if "SuffixImage" in node:
                result = stamp(result, node["SuffixImage"]["ImageRange"]["ImageIndex"], x, y)
        if "NoDataImageIndex" in node:
            result = stamp(result, node["NoDataImageIndex"], node["X"], node["Y"])
        if signed and "DelimiterImageIndex" in node:
            # Weather uses this field for a leading minus, not thousands.
            x, y = node["X"], node["Y"]
            minus = node["DelimiterImageIndex"]
            result = stamp(result, minus, x, y)
            x += images[minus].width
            for digit in range(maximum):
                result = ImageChops.lighter(result, range_mask(base, count, x, y))
                x += images[base].width
                if "SuffixImage" in node:
                    result = stamp(result, node["SuffixImage"]["ImageRange"]["ImageIndex"], x, y)
        return result

    for mode in ("main", "idle"):
        idle = params["IdleScreen"]
        bg = images[params["Background"]["ImageIndex"] if mode == "main"
                    else idle["BackgroundImageIndex"]]
        rgb = bg.convert("RGB").split()
        static = ImageChops.lighter(ImageChops.lighter(rgb[0], rgb[1]), rgb[2])
        layers = {"background": static.point(lambda p: 255 if p > 24 else 0)}
        time = params["Time"]["Digital"] if mode == "main" else idle["Time"]["Digital"]
        date = params["System"]["Date"] if mode == "main" else idle["Date"]
        for entry in as_list(time["HoursMinutesSeconds"]):
            layers[f"time-{entry['Type']}"] = number(entry["Text"], 2)
        ap = mask()
        for key in ("AM", "PM"):
            if key in time:
                entry = time[key]
                rng = entry["ImageRange"]["ImageRange"]
                ap = stamp(ap, rng["ImageIndex"], entry["Coordinates"]["X"],
                           entry["Coordinates"]["Y"])
        layers["AM/PM"] = ap
        for entry in as_list(date["YearMonthDay"]):
            txt = entry["Text"]
            if entry["Type"] == 2:
                layers["day"] = number(txt, 2)
            else:
                node = txt["Image"]
                rng = node["ImageRange"]["ImageRange"]
                layers["month"] = range_mask(rng["ImageIndex"], rng["ImagesCount"],
                                              node["X"], node["Y"])
        node = date["Week"]["Text"]["Image"]
        rng = node["ImageRange"]["ImageRange"]
        layers["weekday"] = range_mask(rng["ImageIndex"], rng["ImagesCount"], node["X"], node["Y"])
        data = params["System"]["Data"] if mode == "main" else idle["Data"]
        for entry in as_list(data):
            typ = entry["Type"]
            if "NumberSequence" in entry:
                layers[typ] = number(entry["NumberSequence"]["Text"], MAX_DIGITS[typ],
                                     solar=typ == "Sunrise", signed=typ == "Weather")
                if "CircleScale" in entry:
                    gauge = entry["CircleScale"]
                    a = gauge["Angle"]
                    inner = a["Radius"] - gauge["Width"]
                    ink = layers[typ]
                    box = ink.getbbox()
                    if box and any(ink.getpixel((x, y)) and
                                   math.hypot(x-a["X"], y-a["Y"]) >= inner
                                   for y in range(box[1], box[3])
                                   for x in range(box[0], box[2])):
                        errors.append(f"{mode}: {typ} value exceeds the gauge interior")
            if "Linear" in entry:
                linear = entry["Linear"]
                rng, pos = linear["ImageRange"], linear["Segments"]
                layers[typ + " banner"] = range_mask(rng["ImageIndex"], rng["ImagesCount"],
                                                      pos["X"], pos["Y"])
        for (a, left), (b, right) in combinations(layers.items(), 2):
            overlap = ImageChops.multiply(left, right).getbbox()
            if overlap:
                errors.append(f"{mode}: {a} overlaps {b} at {overlap}")
    return errors


if __name__ == "__main__":
    issues = layout_errors(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("build/telu"))
    print("\n".join(issues) if issues else "LAYOUT OK: all sprite variants clear of other content")
    sys.exit(bool(issues))
