#!/usr/bin/env python

from testing_utils import *

from hydros.dxfreader import *


class TestDxf(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dxf = Dxf("data/meeuw.dxf")

    def test_blocks(self):
        for block in self.dxf.blocks:
            pass

    def test_layers(self):
        for layer in self.dxf.layers:
            pass

    def test_get_lines(self):
        self.assertEqual(11, len(self.dxf.get_lines()))

    def test_get_splines(self):
        self.assertEqual(0, len(self.dxf.get_splines()))

    def test_get_arcs(self):
        self.assertEqual(0, len(self.dxf.get_arcs()))


class TestSpline(unittest.TestCase):

    def test_to_line(self):
        spline = Spline()
        points = [[1, 0], [2, 1], [3, 2], [4, 3], [5, 4]]
        spline.points = points
        spline.knots = [0, 0, 0, 0, 1, 2, 2, 2, 2]
        line = np.array(spline.to_line(5))
        self.assertTrue((np.abs(line[0] - points[0]) < 1e-9).all())
        self.assertTrue((np.abs(line[-1] - points[-1]) < 1e-9).all())


class TestArc(unittest.TestCase):

    def test_to_line(self):
        arc = Arc()
        arc.center = [0, 1]
        arc.radius = 2
        arc.start_angle = 0
        arc.end_angle = 90
        line = np.array(arc.to_line(3))
        sq2 = math.sqrt(2)
        expected = np.array([(2, 1), (sq2, 1 + sq2), (0, 3)])
        self.assertTrue((np.abs(expected - line) < 1e-9).all())


class TestFunctions(unittest.TestCase):

    def test_collect_frames(self):
        line1 = [[1, 0], [2, 1], [3, 2]]
        line2 = [[4, 4], [3, 2]]
        lines = [line1, line2]
        frames = collect_frames(lines)
        self.assertEqual(1, len(frames))
        frame = frames[0]
        self.assertEqual([2], frame.chines)
        expected = [[1, 0], [2, 1], [3, 2], [4, 4]]
        self.assertEqual(expected, frames[0].yz)


if __name__ == "__main__":
    unittest.main()
