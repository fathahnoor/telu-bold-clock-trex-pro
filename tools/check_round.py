#!/usr/bin/env python3
"""Validator lingkaran v5: pastikan semua elemen dinamis di dalam r=174.

Layar fisik bulat; konten di luar lingkaran terpotong bezel. Gagalkan build
bila ada kotak elemen yang keluar. Dijalankan oleh tools/build_all.py.
"""

import json
import math
import sys
from pathlib import Path

from PIL import Image

CX = CY = 180
SAFE_R = 174

# perkiraan jumlah digit maksimum per elemen
MAXDIGITS = {
    ("Time", 0): 2, ("Time", 1): 2,
    "Steps": 5, "HeartRate": 3, "Calories": 4, "Battery": 3,
    "Weather": 2, "Sunrise": 4, "Day": 2,
}

RING_SAFE_R = 176  # cincin dekoratif boleh menyentuh bezel (sesuai referensi)


def box_dist(x, y, w, h):
    return max(math.hypot(px - CX, py - CY)
               for px, py in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)))


def dims(folder, index):
    with Image.open(Path(folder) / f"{index}.png") as im:
        return im.size


def as_list(value):
    return value if isinstance(value, list) else [value]


def number_box(folder, text_cfg, ndigits, suffix_index=None, delim_index=None):
    node = text_cfg["Image"]
    x0, y0 = node["X"], node["Y"]
    rng = node["ImageRange"]["ImageRange"]
    cells = [dims(folder, rng["ImageIndex"] + i) for i in range(rng["ImagesCount"])]
    cell_w = max(c[0] for c in cells)
    cell_h = max(c[1] for c in cells)
    total = cell_w * ndigits + text_cfg.get("Spacing", 0) * max(0, ndigits - 1)
    decimal = node.get("DecimalPointImageIndex")
    if decimal is not None:
        dw, dh = dims(folder, decimal)
        total += dw
        cell_h = max(cell_h, dh)
    if ndigits >= 4 and delim_index is not None:
        total += dims(folder, delim_index)[0]
    if suffix_index is not None:
        sw, sh = dims(folder, suffix_index)
        total += sw
        cell_h = max(cell_h, sh)
    align = text_cfg.get("Alignment", "Left")
    suffix_width = dims(folder, suffix_index)[0] if suffix_index is not None else 0
    reserved = cell_w * ndigits + 1 + max(0, text_cfg.get("Spacing", 0)) * (ndigits - 1)
    if align == "Right":
        x = x0 + reserved - (total - suffix_width)
    elif align == "Center":
        x = x0 + reserved // 2 - (total - suffix_width) // 2
    else:
        x = x0
    return x, y0, total, cell_h


def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("build/telu")
    params = json.loads((folder / "watchface.json").read_text())
    bad = []

    def check(name, x, y, w, h):
        dist = box_dist(x, y, w, h)
        flag = "OK " if dist <= SAFE_R else "FAIL"
        print("%s %-24s box=(%d,%d %dx%d) maxdist=%.1f"
              % (flag, name, x, y, w, h, dist))
        if dist > SAFE_R:
            bad.append(name)

    def check_time(prefix, block):
        hms = as_list(block["HoursMinutesSeconds"])
        for e in hms:
            txt = e["Text"]
            nd = MAXDIGITS[("Time", e["Type"])]
            check("%s time t%d" % (prefix, e["Type"]),
                  *number_box(folder, txt, nd))
        for key in ("AM", "PM"):
            if key not in block:
                continue
            ap = block[key]
            rng = ap["ImageRange"]["ImageRange"]
            w, h = dims(folder, rng["ImageIndex"])
            check("%s %s" % (prefix, key), ap["Coordinates"]["X"],
                  ap["Coordinates"]["Y"], w, h)

    def check_date(prefix, block):
        ymd = {e["Type"]: e for e in as_list(block["YearMonthDay"])}
        for typ, label, nd in ((2, "day", 2), (1, "month", 5)):
            e = ymd.get(typ)
            if e is None:
                continue
            rng = e["Text"]["Image"]["ImageRange"]["ImageRange"]
            widest = max(dims(folder, rng["ImageIndex"] + i)[0]
                         for i in range(rng["ImagesCount"]))
            h = dims(folder, rng["ImageIndex"])[1]
            check("%s %s" % (prefix, label), e["Text"]["Image"]["X"],
                  e["Text"]["Image"]["Y"], widest if typ == 1 else 2 * widest, h)
        week = block.get("Week")
        if week:
            txt = week["Text"]
            rng = txt["Image"]["ImageRange"]["ImageRange"]
            widest = max(dims(folder, rng["ImageIndex"] + i)[0]
                         for i in range(rng["ImagesCount"]))
            h = dims(folder, rng["ImageIndex"])[1]
            check("%s weekday" % prefix, txt["Image"]["X"], txt["Image"]["Y"],
                  widest, h)

    def check_data(prefix, entries):
        for e in as_list(entries):
            t = e.get("Type")
            if "NumberSequence" in e and t in MAXDIGITS:
                txt = e["NumberSequence"]["Text"]
                nd = MAXDIGITS[t]
                suf = None
                if "SuffixImage" in txt["Image"]:
                    suf = txt["Image"]["SuffixImage"]["ImageRange"]["ImageIndex"]
                delim = txt["Image"].get("DelimiterImageIndex")
                check("%s %s" % (prefix, t),
                      *number_box(folder, txt, nd, suf, delim))
            if "Linear" in e:
                seg = e["Linear"]["Segments"]
                rng = e["Linear"]["ImageRange"]
                # Pisahkan klaster ikon (atas) dan label (bawah) supaya
                # sudut transparan tidak dihitung.
                icon_box = [10 ** 6, 10 ** 6, -1, -1]
                label_box = [10 ** 6, 10 ** 6, -1, -1]
                for i in range(rng["ImagesCount"]):
                    with Image.open(Path(folder) / f"{rng['ImageIndex'] + i}.png") as im:
                        im = im.convert("RGBA")
                        for box, y0, y1 in ((icon_box, 0, 36), (label_box, 36, im.height)):
                            crop = im.crop((0, y0, im.width, y1)).getbbox()
                            if crop is None:
                                continue
                            box[0] = min(box[0], crop[0])
                            box[1] = min(box[1], y0 + crop[1])
                            box[2] = max(box[2], crop[2])
                            box[3] = max(box[3], y0 + crop[3])
                for tag, box in (("icon", icon_box), ("label", label_box)):
                    if box[2] < 0:
                        continue
                    check("%s %s %s" % (prefix, t, tag), seg["X"] + box[0],
                          seg["Y"] + box[1], box[2] - box[0], box[3] - box[1])
            if "CircleScale" in e:
                a = e["CircleScale"]["Angle"]
                r = a["Radius"] + e["CircleScale"].get("Width", 7)
                dist = math.hypot(a["X"] - CX, a["Y"] - CY) + r
                flag = "OK " if dist <= RING_SAFE_R else "FAIL"
                print("%s %-24s ring center-dist+r=%.1f (r=%.1f)"
                      % (flag, "%s %s ring" % (prefix, t), dist, r))
                if dist > RING_SAFE_R:
                    bad.append("%s %s ring" % (prefix, t))

    check_time("main", params["Time"]["Digital"])
    check_date("main", params["System"]["Date"])
    check_data("main", params["System"]["Data"])

    idle = params["IdleScreen"]
    check_time("idle", idle["Time"]["Digital"])
    check_date("idle", idle["Date"])
    check_data("idle", idle["Data"])

    if bad:
        print("GAGAL: %d elemen di luar lingkaran: %s" % (len(bad), bad))
        return 1
    print("LINGKARAN AMAN: semua elemen di dalam r=%d" % SAFE_R)
    return 0


if __name__ == "__main__":
    sys.exit(main())
