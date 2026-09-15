"""AOD keeps all fields, glyph masks and positioning without runtime effects."""
import unittest
from pathlib import Path
from PIL import Image
from gen_telu import aod_dim, AOD_HOUR_GAIN, AOD_MINUTE_GAIN
from render_mockup import load

ROOT = Path(__file__).resolve().parent.parent


class AodTests(unittest.TestCase):
    def test_decoded_aod_digits_preserve_alpha_and_dimensions(self):
        p, images = load(ROOT/"build/verified_bin")
        normal = p["Time"]["Digital"]["HoursMinutesSeconds"]
        idle = p["IdleScreen"]["Time"]["Digital"]["HoursMinutesSeconds"]
        for n,a,gain in zip(normal,idle,(AOD_HOUR_GAIN,AOD_MINUTE_GAIN)):
            ni=n["Text"]["Image"]["ImageRange"]["ImageRange"]["ImageIndex"]
            ai=a["Text"]["Image"]["ImageRange"]["ImageRange"]["ImageIndex"]
            for digit in range(10):
                src,dst=images[ni+digit],images[ai+digit]
                self.assertEqual(src.size,dst.size)
                self.assertEqual(src.getchannel("A").tobytes(),dst.getchannel("A").tobytes())
                self.assertEqual(aod_dim(src,gain).tobytes(),dst.tobytes())

    def test_normal_preview_unchanged_outside_enlarged_date(self):
        from PIL import ImageDraw
        current = Image.open(ROOT/"out/preview.png").convert("RGB")
        previous = Image.open(ROOT/"out/baseline/preview_idle.png").convert("RGB")
        for image in (current, previous):
            ImageDraw.Draw(image).rectangle((259,91,310,112), fill="black")
        self.assertEqual(current.tobytes(), previous.tobytes())

    def test_dim_preserves_black_and_faint_detail(self):
        image=Image.new("RGBA",(256,1))
        image.putdata([(v,v,v,255) for v in range(256)])
        values=list(aod_dim(image,0.55).getdata())
        self.assertEqual(values[0],(0,0,0,255))
        self.assertTrue(all(0 < p[0] <= i for i,p in enumerate(values) if i))
