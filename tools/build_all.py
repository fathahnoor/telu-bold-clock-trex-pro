#!/usr/bin/env python3
"""Satu perintah build penuh V6: aset -> mockup -> pack -> verifikasi.

Pakai dari root repo:
  python tools/build_all.py
Hasil: out/telu_trex_pro.bin untuk uji instalasi pada jam, plus deretan
preview di out/.
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(*args):
    print("+", " ".join(args))
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def main():
    run("tools/gen_telu.py")
    run("tools/check_round.py", "build/telu")
    run("tools/check_layout.py", "build/telu")
    run("tools/render_mockup.py", "build/telu", "build/mockup_360.png",
        "--small", "build/mockup_220.png")
    shutil.copy(ROOT / "build" / "mockup_220.png", ROOT / "build" / "telu" / "preview.png")
    (ROOT / "out").mkdir(exist_ok=True)
    run("tools/pack_watchface.py", "build/telu", "out/telu_trex_pro.bin")
    run("tools/verify_bin.py")
    run("tools/check_layout.py", "build/verified_bin")
    # Preview dari bin yang sudah diverifikasi (round-trip).
    run("tools/render_mockup.py", "build/verified_bin", "out/preview.png")
    scenarios = {
        "max": ["--time", "2359", "--steps", "10000", "--kcal", "1000", "--hr", "220", "--batt", "100", "--ampm", "none"],
        "zero": ["--time", "0101", "--steps", "0", "--kcal", "0", "--hr", "0", "--batt", "1", "--temp", "0"],
        "idle": ["--mode", "idle"],
        "sunrise": ["--time", "0520", "--solar", "sunrise", "--sunrisetime", "0546"],
        "after_sunset": ["--time", "2030", "--solar", "sunrise", "--sunrisetime", "0546", "--ampm", "none"],
        "negative": ["--temp", "-5", "--cond", "10"],
    }
    for name, options in scenarios.items():
        run("tools/render_mockup.py", "build/verified_bin", f"out/preview_{name}.png", *options)
    (ROOT / "out/stress").mkdir(exist_ok=True)
    for time in ("0000", "0101", "0808", "1028", "1111", "1259", "1848", "2000", "2359"):
        run("tools/render_mockup.py", "build/verified_bin", f"out/stress/{time}.png", "--time", time, "--ampm", "none")
    shutil.copyfile(ROOT / "out/telu_trex_pro.bin", ROOT / "out/telu_university_v6.bin")
    run("tools/make_contact_sheet.py")
    run("tools/aod_report.py")
    print("BUILD OK -> out/telu_university_v6.bin")



if __name__ == "__main__":
    main()
