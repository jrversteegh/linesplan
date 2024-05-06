import difflib
import math
import unittest

import pytest

from hydros.linesplan import *


class TestLinesPlan(unittest.TestCase):
    pass


class TestFunctions(unittest.TestCase):

    def setUp(self):
        # Create a cylindrical body
        f = np.linspace(0, np.pi, 101)
        ys = np.sin(f)
        zs = 1 - np.cos(f)
        frame = [[y, z] for y, z in zip(ys, zs)]
        self.frames = [Frame(frame, x=float(i)) for i in range(5)]
        for frame in self.frames:
            frame.chines.append(50)

    def test_load_save(self, scriptdir):
        f1 = scriptdir / "../data/grender_sailer.json"
        f2 = scriptdir / "../output/grendel_sailer.json"
        lines = load_lines_plan(f1)
        save_lines_plan(lines, f2)
        with open(f1) as f:
            s1 = f.readlines()
        with open(f2) as f:
            s2 = f.readlines()
        diffs = list(difflib.unified_diff(s1, s2))
        self.assertFalse(diffs)

    def test_get_waterline_properties(self):
        w1 = [[1.0, 0.0, 2.0], [1.0, 1.0, 2.0], [2.0, 2.0, 2.0], [2.0, 0.0, 2.0]]
        w2 = [[-2.0, 0.0, 2.0], [-2.0, 2.0, 2.0], [-1.0, 1.0, 2.0], [-1.0, 0.0, 2.0]]
        a1, m1x, m1x2, m1y, m1y2 = get_waterline_properties(w1)
        a2, m2x, m2x2, m2y, m2y2 = get_waterline_properties(w2)
        self.assertEqual(a1, a2)
        self.assertEqual(m1x, m2x)
        self.assertEqual(m1x, 7.0 / 6.0)
        self.assertEqual(m1y, -m2y)
        self.assertEqual(m1y, 7.0 / 3.0)
        self.assertEqual(m1x2, m2x2)
        self.assertEqual(m1x2, 5.0 / 4.0)
        self.assertEqual(m1y2, m2y2)
        self.assertEqual(m1y2, 15.0 / 4.0)

    def test_get_km(self):
        km = get_km(self.frames, 1.0)
        dispvol = get_displacement(self.frames, 1.0)
        self.assertAlmostEqual(math.pi * 2.0, dispvol, delta=1e-2)
        self.assertAlmostEqual(1.0, km, delta=1e-2)
        km = get_km(self.frames, 0.5)
        self.assertAlmostEqual(1.0, km, delta=1e-2)
        tap, tfp = 0.75, 0.50
        km = get_km(self.frames, tap, tfp)
        lcb = get_lcb(self.frames, tap, tfp)
        expected = 1 + lcb / 4.0 * (tap - tfp)
        self.assertAlmostEqual(expected, km, delta=1e-2)

    def test_get_hull_areas(self):
        ha, da = get_hull_areas(self.frames)
        self.assertAlmostEqual(ha, da, delta=1e-3)
        self.assertAlmostEqual(4 * math.pi, ha, delta=1e-3)

    def test_get_wetted_surface(self):
        draft = 1 - 0.5 * math.sqrt(2)
        s = get_wetted_surface(self.frames, draft)
        self.assertAlmostEqual(2 * math.pi, s, delta=1e-3)
