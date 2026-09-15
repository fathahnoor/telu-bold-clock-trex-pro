"""Decoded-BIN visual signal audit, not a battery/power measurement."""
import json
import hashlib
from pathlib import Path
from PIL import Image
from render_mockup import load, draw_time, draw_date, draw_data

ROOT = Path(__file__).resolve().parent.parent


def main():
    params, images = load(ROOT / "build/verified_bin")
    rows = []
    for time in ("0000", "0101", "0808", "1028", "1111", "1259", "1848", "2000", "2359"):
        args = dict(time=time, ampm="none", day=12, month=9, wday=4, steps=8426,
                    hr=72, kcal=560, batt=82, temp=29, cond=2, solar="sunset",
                    solartime="1802", sunrisetime="0546")
        totals = []
        for mode in ("normal", "idle"):
            idle = params["IdleScreen"]
            canvas = images[params["Background"]["ImageIndex"] if mode == "normal"
                            else idle["BackgroundImageIndex"]].copy()
            draw_time(canvas, images, params["Time"]["Digital"] if mode == "normal" else idle["Time"]["Digital"], args)
            draw_date(canvas, images, params["System"]["Date"] if mode == "normal" else idle["Date"], args)
            draw_data(canvas, images, params["System"]["Data"] if mode == "normal" else idle["Data"], args)
            totals.append(sum(canvas.convert("RGB").tobytes()))
            if mode == "idle":
                folder = ROOT / "out/aod-stress"
                folder.mkdir(exist_ok=True)
                canvas.save(folder / f"{time}.png")
        rows.append(dict(time=time, normal_rgb_sum=totals[0], aod_rgb_sum=totals[1],
                         rgb_signal_reduction_percent=round(100*(1-totals[1]/totals[0]),2)))
    result = dict(bin_sha256=hashlib.sha256((ROOT/"out/telu_university_v6.bin").read_bytes()).hexdigest(),
                  metric="Sum of encoded RGB channel values; not watts, luminance or battery life",
                  measured_battery_saving=None, firmware_refresh_control=False,
                  extra_time_sprites=20, shared_date_and_metrics=True, scenarios=rows)
    (ROOT/"out/aod-analysis.json").write_text(json.dumps(result,indent=2)+"\n")
    from make_contact_sheet import sheet
    sheet([("AOD sebelumnya", ROOT/"out/baseline/preview_idle.png"),
           ("AOD hemat", ROOT/"out/preview_idle.png")], "out/aod-comparison.png", columns=2)


if __name__ == "__main__":
    main()
