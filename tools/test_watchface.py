"""Regression checks v5 TELKOM UNIVERSITY (container, params, sprite, warna)."""
import json
import math
import struct
import unittest
from unittest.mock import patch
from pathlib import Path

from PIL import Image

from gen_telu import make_digit, F_INTER, TIME_CELL, svg_icon, HEART
from check_layout import layout_errors
from render_mockup import load, draw_number, draw_date, draw_gauge
from check_round import number_box
from trexpro_wf import (validate_trexpro_container, unpack, ids_to_names,
                        decode_image, encode_image)

ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / 'out/telu_trex_pro.bin'


class WatchfaceV5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.params, cls.images, _ = unpack(BIN.read_bytes())
        cls.named = ids_to_names(cls.params)

    def test_deliverable_device_container(self):
        checks = validate_trexpro_container(BIN.read_bytes())
        self.assertEqual(checks['device_id'], 83)
        self.assertEqual(checks['decoded_block_bytes'], 4096)

    def test_wrong_device_is_rejected(self):
        data = bytearray(BIN.read_bytes())
        struct.pack_into('<H', data, 16, 59)
        with self.assertRaisesRegex(ValueError, 'wrong device'):
            validate_trexpro_container(data)

    def test_false_quicklz_length_is_rejected(self):
        data = bytearray(BIN.read_bytes())
        struct.pack_into('<I', data, 45, 32768)
        with self.assertRaisesRegex(ValueError, '4096'):
            validate_trexpro_container(data)

    def test_background_and_preview_resolution(self):
        bg = self.named['Background']['ImageIndex']
        preview = self.named['Background']['Preview']['ImageRange']['ImageIndex']
        self.assertEqual(decode_image(self.images[bg - 1])[:2], (360, 360))
        self.assertEqual(decode_image(self.images[preview - 1])[:2], (220, 220))
        self.assertEqual(decode_image(self.images[preview - 1])[2],
                         Image.open(ROOT / 'build/telu/preview.png')
                         .convert('RGBA').tobytes())

    def test_hour_and_minute_digit_sets_are_white(self):
        hms = self.named['Time']['Digital']['HoursMinutesSeconds']
        for entry in hms:
            rng = entry['Text']['Image']['ImageRange']['ImageRange']
            for i in range(10):
                blob = self.images[rng['ImageIndex'] + i - 1]
                w, h, px = decode_image(blob)
                self.assertEqual((w, h), TIME_CELL)
                opaque = [tuple(px[p:p + 3]) for p in range(0, len(px), 4)
                          if px[p + 3] > 200]
                self.assertGreater(len(opaque), 40, i)
                self.assertTrue(all(rgb == (255, 255, 255) for rgb in opaque),
                                (entry['Type'], i))

    def test_today_month_and_weekday_ranges(self):
        ymd = {e['Type']: e for e in self.named['System']['Date']['YearMonthDay']}
        self.assertEqual(ymd[1]['Text']['Image']['ImageRange']['ImageRange']
                         ['ImagesCount'], 12)
        self.assertEqual(self.named['System']['Date']['Week']['Text']['Image']
                         ['ImageRange']['ImageRange']['ImagesCount'], 7)

    def test_weather_has_29_icon_banner_range(self):
        weather = [e for e in self.named['System']['Data']
                   if e['Type'] == 'Weather']
        linear = [e for e in weather if 'Linear' in e]
        self.assertEqual(len(linear), 1)
        self.assertEqual(linear[0]['Linear']['ImageRange']['ImagesCount'], 29)
        num = [e for e in weather if 'NumberSequence' in e]
        self.assertTrue(num)

    def test_sunrise_is_closest_event_with_icon_pair(self):
        sunrise = [e for e in self.named['System']['Data']
                   if e['Type'] == 'Sunrise']
        self.assertEqual(len(sunrise), 2)
        seq = [e for e in sunrise if 'NumberSequence' in e][0]
        self.assertNotIn('Type', seq['NumberSequence'])
        self.assertIn('DecimalPointImageIndex',
                      seq['NumberSequence']['Text']['Image'])
        pair = [e for e in sunrise if 'Linear' in e][0]
        self.assertEqual(pair['Linear']['ImageRange']['ImagesCount'], 2)

    def test_no_right_alignment_in_delivered_bin(self):
        found = []

        def walk(node, path):
            if isinstance(node, dict):
                for key, value in node.items():
                    if key == 'Alignment' and value == 'Right':
                        found.append(path)
                    walk(value, path + '/' + str(key))
            elif isinstance(node, list):
                for i, value in enumerate(node):
                    walk(value, path + '[%d]' % i)

        walk(self.named, '')
        self.assertEqual(found, [], 'Alignment Right tidak didukung: %s' % found)

    def test_idle_contains_the_complete_normal_layout(self):
        idle = self.named['IdleScreen']
        self.assertEqual(idle['BackgroundImageIndex'],
                         self.named['Background']['ImageIndex'])
        self.assertEqual(idle['Time'], self.named['Time'])
        self.assertEqual(idle['Date'], self.named['System']['Date'])
        self.assertEqual(idle['Data'], self.named['System']['Data'])

    def test_idle_preview_matches_normal_pixel_for_pixel(self):
        with Image.open(ROOT / 'out/preview.png') as normal:
            with Image.open(ROOT / 'out/preview_idle.png') as idle:
                self.assertEqual(idle.size, normal.size)
                self.assertEqual(idle.convert('RGBA').tobytes(),
                                 normal.convert('RGBA').tobytes())

    def test_all_gauges_present(self):
        types = [e['Type'] for e in self.named['System']['Data']]
        for t in ('Battery', 'Steps', 'Calories', 'HeartRate'):
            self.assertIn(t, types)
            entry = [e for e in self.named['System']['Data']
                     if e['Type'] == t][0]
            self.assertIn('CircleScale', entry)

    def test_image_round_trip_keeps_rgb_order(self):
        img = Image.new('RGBA', (2, 1))
        img.putdata([(255, 32, 41, 255), (10, 20, 30, 255)])
        blob = encode_image(img.tobytes(), 2, 1)
        w, h, px = decode_image(blob)
        self.assertEqual((w, h), (2, 1))
        self.assertEqual(px, img.tobytes())

    def test_digits_have_room_on_all_sides(self):
        for cell_w, cell_h, size, stretch in (
                (40, 56, 96, 0.71), (10, 17, 27, 0.55), (9, 12, 19, 0.78)):
            for digit in '0123456789':
                bbox = make_digit(digit, cell_w, cell_h, F_INTER, size,
                                  variation="Black", stretch=stretch).getbbox()
                self.assertIsNotNone(bbox)
                self.assertGreaterEqual(bbox[1], 0, (digit, bbox))
                self.assertLessEqual(bbox[3], cell_h, (digit, bbox))

    def test_metric_values_fit_inside_rings(self):
        folder = ROOT / 'build/telu'
        params = json.loads((folder / 'watchface.json').read_text())
        rings = {'Steps': 47, 'HeartRate': 43, 'Calories': 44, 'Battery': 43}
        for data in params['System']['Data']:
            name = data['Type']
            if name not in rings:
                continue
            txt = data['NumberSequence']['Text']
            rng = txt['Image']['ImageRange']['ImageRange']
            nd = {'Steps': 5, 'HeartRate': 3, 'Calories': 4, 'Battery': 3}[name]
            delim = txt['Image'].get('DelimiterImageIndex')
            suf = None
            if 'SuffixImage' in txt['Image']:
                suf = txt['Image']['SuffixImage']['ImageRange']['ImageIndex']
            x, y, w, h = number_box(folder, txt, nd, suf, delim)
            cx = data['CircleScale']['Angle']['X']
            self.assertLessEqual(abs(x + w / 2 - cx), rings[name], name)
            self.assertLessEqual(w / 2, rings[name], name)

    def test_dynamic_variants_do_not_overlap(self):
        self.assertEqual(layout_errors(ROOT / 'build/verified_bin'), [])

    def test_gauges_close_at_maximum_and_clamp_overflow(self):
        params, images = load(ROOT / 'build/verified_bin')
        for entry in params['System']['Data']:
            if 'CircleScale' not in entry:
                continue
            gauge = entry['CircleScale']
            angle = gauge['Angle']
            self.assertEqual(angle['EndAngle'] - angle['StartAngle'], 360)
            full = Image.new('RGBA', (360, 360))
            draw_gauge(full, images, entry, 1)
            radius = angle['Radius'] - gauge['Width'] / 2
            for degree in range(360):
                rad = math.radians(degree)
                point = (round(angle['X'] + radius * math.cos(rad)),
                         round(angle['Y'] + radius * math.sin(rad)))
                self.assertGreater(full.getpixel(point)[3], 200,
                                   (entry['Type'], degree))
            overflow = Image.new('RGBA', (360, 360))
            draw_gauge(overflow, images, entry, 2)
            self.assertEqual(overflow.tobytes(), full.tobytes())
            empty = Image.new('RGBA', (360, 360))
            draw_gauge(empty, images, entry, 0)
            self.assertIsNone(empty.getbbox())
            half = Image.new('RGBA', (360, 360))
            draw_gauge(half, images, entry, 0.5)
            self.assertGreater(half.getpixel((round(angle['X'] + radius), angle['Y']))[3], 200)
            self.assertEqual(half.getpixel((round(angle['X'] - radius), angle['Y']))[3], 0)

    def test_metric_groups_stay_centered_for_every_digit_length(self):
        params, images = load(ROOT / 'build/verified_bin')
        cases = {'Steps': (5, [0, 1, 7, 12, 99, 100, 999, 1000, 9999, 99999]),
                 'HeartRate': (3, [0, 7, 72, 199]),
                 'Calories': (4, [0, 7, 35, 560, 9999]),
                 'Battery': (3, [0, 1, 7, 82, 100])}
        for entry in params['System']['Data']:
            if entry['Type'] not in cases:
                continue
            maximum, values = cases[entry['Type']]
            txt = entry['NumberSequence']['Text']
            self.assertEqual(txt['Alignment'], 'Center')
            for value in values:
                canvas = Image.new('RGBA', (360, 360))
                draw_number(canvas, images, txt, value, max_digits=maximum)
                box = canvas.getbbox()
                self.assertLessEqual(abs((box[0] + box[2]) / 2 -
                                         entry['CircleScale']['Angle']['X']), 0.5,
                                     (entry['Type'], value, box))

    def test_all_date_combinations_stay_centered(self):
        params, images = load(ROOT / 'build/verified_bin')
        for weekday in range(7):
            for day in range(1, 32):
                for month in range(1, 13):
                    canvas = Image.new('RGBA', (360, 360))
                    draw_date(canvas, images, params['System']['Date'],
                              dict(wday=weekday, day=day, month=month))
                    box = canvas.getbbox()
                    self.assertLessEqual(abs((box[0] + box[2]) / 2 - 180), 0.5,
                                         (weekday, day, month, box))

    def test_colored_svg_keeps_transparent_corners(self):
        icon = svg_icon(ROOT / 'assets/heart.svg', 30, fill=HEART)
        self.assertEqual(icon.getpixel((0, 0))[3], 0)
        self.assertGreater(icon.getpixel((icon.width // 2, icon.height // 2))[3], 200)

    def test_layout_checker_rejects_time_metric_collision(self):
        params, images = load(ROOT / 'build/verified_bin')
        heart = next(e for e in params['System']['Data'] if e['Type'] == 'HeartRate')
        heart['NumberSequence']['Text']['Image'].update(X=200, Y=150)
        with patch('check_layout.load', return_value=(params, images)):
            errors = layout_errors('unused')
        self.assertTrue(any('time-1 overlaps HeartRate' in e for e in errors), errors)


if __name__ == '__main__':
    unittest.main()
