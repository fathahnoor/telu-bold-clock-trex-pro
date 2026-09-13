"""Verifikasi .bin hasil pack vs sumber desain (toleran kuantisasi RGB565)."""
import json
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trexpro_wf import unpack, names_to_ids, decode_image, shift_image_ids, validate_image_references, ids_to_names

REPO = Path(__file__).resolve().parent.parent
BIN = REPO / "out" / "telu_trex_pro.bin"
SRC = REPO / "build" / "telu"


def norm(node):
    if isinstance(node, dict):
        return {k: norm(v) for k, v in node.items()}
    if isinstance(node, list) and len(node) == 1:
        return norm(node[0])
    if isinstance(node, list):
        return [norm(v) for v in node]
    return node


import struct
from trexpro_wf import decompress_uihh, validate_trexpro_container
raw = BIN.read_bytes()
container_checks = validate_trexpro_container(raw)
assert raw[:6] == b"UIHH\x02\x00", "signature/version salah"
assert raw[40] in (0x4e, 0x4f), "output harus compressed"
expanded = decompress_uihh(raw)
assert struct.unpack_from("<I", raw, 32)[0] == len(expanded) - 40
params, images, _ = unpack(raw)
print("bin: %d gambar" % len(images))
src_files = sorted(SRC.glob("[0-9]*.png"), key=lambda p: int(p.stem))
assert [int(p.stem) for p in src_files] == list(range(len(src_files))), \
    "PNG sumber tidak berurutan"
assert len(images) == len(src_files) + 1, "jumlah gambar harus = aset + preview"

named = json.loads((SRC / "watchface.json").read_text())
firmware_named = ids_to_names(params)
image_checks = validate_image_references(firmware_named, images)
expected = names_to_ids(shift_image_ids(named, 1))
exp = norm(json.loads(json.dumps(expected)))
got = norm(json.loads(json.dumps({str(k): v for k, v in params.items()})))
assert exp == got, "parameter hasil unpack berbeda"
print("params sama: True")

bad = 0
maxd = 0
for i, src in enumerate(src_files):
    src_img = Image.open(src).convert("RGBA")
    w, h, px = decode_image(images[i])
    assert (w, h) == src_img.size, (i, (w, h), src_img.size)
    a, b = src_img.tobytes(), px
    d = max(abs(x - y) for x, y in zip(a, b))
    maxd = max(maxd, d)
    # piksel fully transparan/opaque harus eksak; hanya tepi antialias yg noise
    if d > 8:
        bad += 1
        print("img %d delta besar: %d" % (i, d))
w, h, px = decode_image(images[len(src_files)])
src_prev = Image.open(SRC / "preview.png").convert("RGBA")
d = max(abs(x - y) for x, y in zip(src_prev.tobytes(), px))
maxd = max(maxd, d)
print("preview 220x220 ok:", (w, h) == (220, 220), "delta:", d)
print("max delta global:", maxd, "| gambar bermasalah:", bad)
assert (w, h) == (220, 220), "ukuran preview salah"
assert maxd <= 8 and bad == 0, "pixel round-trip gagal"
print("VERIFIKASI SELESAI")

# Preserve serialized firmware parameters and normalize only the local renderer copy.
from trexpro_wf import ids_to_names
folder = REPO / "build" / "verified_bin"
folder.mkdir(exist_ok=True)
(folder / "firmware_params.json").write_text(json.dumps(firmware_named, indent=2))
(folder / "watchface.json").write_text(json.dumps(shift_image_ids(firmware_named, -1), indent=2))
for i, blob in enumerate(images):
    w, h, pixels = decode_image(blob)
    Image.frombytes("RGBA", (w, h), pixels).save(folder / f"{i}.png")
import hashlib
report = {"file": BIN.name, "sha256": hashlib.sha256(raw).hexdigest(),
          "bytes": len(raw), "format": "UIHH v2 compressed", "images": len(images),
          "params_equal": True, "max_pixel_delta": maxd,
          "container_checks": container_checks, "image_reference_checks": image_checks,
          "device_test": "v5 TELKOM UNIVERSITY menunggu uji perangkat",
          "previous_device_result": "Compat v4 aktif dan berjalan di T-Rex Pro (laporan pengguna, 12 September 2026)"}
(REPO / "out" / "validation.json").write_text(json.dumps(report, indent=2))
