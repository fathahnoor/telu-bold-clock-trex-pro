"""V6 regressions for signed weather, no-data, mode and source integrity."""
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageChops
from render_mockup import load, draw_number, draw_time
from check_layout import layout_errors

ROOT = Path(__file__).resolve().parent.parent


class V6Scenarios(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.params, cls.images = load(ROOT / "build/verified_bin")

    def test_signed_and_unsigned_weather(self):
        entry = next(e for e in self.params["System"]["Data"]
                     if e["Type"] == "Weather" and "NumberSequence" in e)
        txt = entry["NumberSequence"]["Text"]
        node = txt["Image"]
        for temperature in (-99, -5, 0, 9, 29, 39, 99):
            canvas = Image.new("RGBA", (360,360))
            draw_number(canvas,self.images,txt,temperature)
            box = canvas.getbbox()
            self.assertTrue(288 <= box[0] < box[2] <= 330 and 253 <= box[1] < box[3] <= 265, (temperature,box))
            if temperature < 0:
                minus = self.images[node["DelimiterImageIndex"]]
                self.assertEqual(canvas.crop((288,253,288+minus.width,253+minus.height)).tobytes(),minus.tobytes())

    def test_no_data_sprites_render(self):
        for entry in self.params["System"]["Data"]:
            if "NumberSequence" not in entry:
                continue
            txt = entry["NumberSequence"]["Text"]
            canvas = Image.new("RGBA",(360,360))
            draw_number(canvas,self.images,txt,None)
            self.assertIsNotNone(canvas.getbbox(),entry["Type"])

    def test_weather_negative_collision_is_detected(self):
        params, images = load(ROOT / "build/verified_bin")
        weather = next(e for e in params["System"]["Data"] if e["Type"] == "Weather" and "NumberSequence" in e)
        weather["NumberSequence"]["Text"]["Image"].update(X=225,Y=245)
        with patch("check_layout.load",return_value=(params,images)):
            self.assertTrue(any("time-1 overlaps Weather" in e for e in layout_errors("unused")))

    def test_24h_mode_omits_ampm_badge(self):
        block = self.params["Time"]["Digital"]
        am = Image.new("RGBA",(360,360))
        plain = Image.new("RGBA",(360,360))
        draw_time(am,self.images,block,dict(time="2359",ampm="PM"))
        draw_time(plain,self.images,block,dict(time="2359",ampm="none"))
        diff = ImageChops.difference(am,plain).getbbox()
        self.assertIsNotNone(diff)
        self.assertGreaterEqual(diff[0],245)
        self.assertLessEqual(diff[3],175)

    def test_product_alias_is_identical(self):
        self.assertEqual((ROOT/"out/telu_university_v6.bin").read_bytes(),(ROOT/"out/telu_trex_pro.bin").read_bytes())

    def test_all_required_previews_exist(self):
        for name in ("preview", "preview_sunrise", "preview_after_sunset", "preview_max", "preview_zero", "preview_idle", "preview_negative"):
            with Image.open(ROOT / f"out/{name}.png") as im:
                self.assertEqual(im.size,(360,360))
        for time in ("0000","0101","0808","1028","1111","1259","1848","2000","2359"):
            self.assertTrue((ROOT/f"out/stress/{time}.png").is_file())


if __name__ == "__main__":
    unittest.main()
