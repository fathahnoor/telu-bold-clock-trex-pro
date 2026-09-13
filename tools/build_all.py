#!/usr/bin/env python3
"""Satu perintah build penuh v5: aset -> mockup -> pack -> verifikasi.

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
    run("tools/render_mockup.py", "build/verified_bin", "out/preview_max.png",
        "--time", "1259", "--steps", "99999", "--kcal", "9999",
        "--hr", "220", "--batt", "100", "--day", "31", "--wday", "0",
        "--month", "12", "--ampm", "PM", "--temp", "35", "--cond", "0")
    run("tools/render_mockup.py", "build/verified_bin", "out/preview_zero.png",
        "--time", "0007", "--steps", "0", "--kcal", "0", "--hr", "0",
        "--batt", "0", "--day", "1", "--wday", "2", "--month", "1",
        "--temp", "0", "--cond", "12")
    run("tools/render_mockup.py", "build/verified_bin", "out/preview_idle.png",
        "--mode", "idle")
    run("tools/render_mockup.py", "build/verified_bin", "out/preview_sunrise.png",
        "--solar", "sunrise", "--solartime", "0547", "--time", "0510",
        "--batt", "94", "--steps", "220", "--kcal", "35", "--hr", "64",
        "--temp", "21", "--cond", "0", "--wday", "4", "--day", "12")
    # Alias dengan nama produk baru.
    shutil.copyfile(ROOT / "out/telu_trex_pro.bin",
                    ROOT / "out/telu_university_v5.bin")
    run("tools/refresh_gallery.py")
    print("BUILD OK -> out/telu_trex_pro.bin (alias: out/telu_university_v5.bin)")


if __name__ == "__main__":
    main()
