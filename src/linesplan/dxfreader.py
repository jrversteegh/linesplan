import math

import ezdxf
import numpy as np
from scipy.interpolate import BSpline

from .line import Frame


class Spline:
    points = None
    knots = None
    count = 200

    def to_line(self, count=None):
        if count is None:
            count = self.count
        bspline = BSpline(self.knots, self.points, 3)
        space = np.linspace(self.knots[0], self.knots[-1], count)
        points = bspline(space)
        return [[i[0], i[1]] for i in points]


class Arc:
    center = None
    radius = None
    start_angle = None
    end_angle = None

    def to_line(self, count=None):
        if count is None:
            count = int(self.end_angle - self.start_angle) * 2
        angles = np.linspace(self.start_angle, self.end_angle, count)
        angles *= np.pi / 180.0
        xs = np.cos(angles) * self.radius + self.center[0]
        ys = np.sin(angles) * self.radius + self.center[1]
        return [list(i) for i in zip(xs, ys)]


class Dxf:
    _doc = None

    def __init__(self, *args, **kwargs):
        super().__init__()
        if len(args):
            self.load(args[0])

    def load(self, filename):
        self._doc = ezdxf.readfile(filename)

    def check_loaded(self):
        if self._doc is None:
            raise Exception("No DXF file loaded")

    @property
    def blocks(self):
        self.check_loaded()
        return [block.name for block in self._doc.blocks]

    @property
    def layers(self):
        self.check_loaded()
        return [layer.dxf.name for layer in self._doc.layers]

    def get_lines(self, block=None, layer=None):
        result = []
        if block:
            src = self._doc.blocks[block]
        else:
            src = self._doc.modelspace()
        layer = '[layer=="%s"]' % layer if layer else ""
        for l in src.query("LINE" + layer):
            line = [list(l.dxf.start[:2]), list(l.dxf.end[:2])]
            result.append(line)
        for l in src.query("LWPOLYLINE" + layer):
            line = [list(vert) for vert in l.vertices()]
            result.append(line)
        return result

    def get_splines(self, block=None, layer=None):
        result = []
        if block:
            src = self._doc.blocks[block]
        else:
            src = self._doc.modelspace()
        layer = '[layer=="%s"]' % layer if layer else ""
        for s in src.query("SPLINE" + layer):
            spline = Spline()
            spline.points = [list(point[:2]) for point in s.control_points]
            spline.knots = [knot for knot in s.knots]
            result.append(spline)
        return result

    def get_arcs(self, block=None, layer=None):
        result = []
        if block:
            src = self._doc.blocks[block]
        else:
            src = self._doc.modelspace()
        layer = '[layer=="%s"]' % layer if layer else ""
        for a in src.query("ARC" + layer):
            arc = Arc()
            arc.center = list(a.dxf.center[:2])
            arc.radius = a.dxf.radius
            arc.start_angle = a.dxf.start_angle
            arc.end_angle = a.dxf.end_angle
            result.append(arc)
        return result


def collect_frames(lines, threshold=2e-3):

    def points_close(p1, p2):
        p1 = np.asarray(p1)
        p2 = np.asarray(p2)
        return np.linalg.norm(p2 - p1) < threshold

    def check_connection(joined, back):
        end = joined[-back][-back]
        connected = None
        for i, line in enumerate(lines):
            if points_close(end, line[-(not back)]):
                connected = lines.pop(i)
            elif points_close(end, line[-back]):
                connected = lines.pop(i)
                connected.reverse()
            else:
                continue
            break
        return connected

    all_joined = []
    while lines:
        joined = [lines.pop(0)]
        while True:
            front = check_connection(joined, False)
            if front is not None:
                joined.insert(0, front)
            back = check_connection(joined, True)
            if back is not None:
                joined.append(back)
            if front is None and back is None:
                all_joined.append(joined)
                break

    result = []
    for segments in all_joined:
        frame = Frame()
        frame.yz += segments.pop(0)
        while segments:
            frame.chines.append(len(frame.yz) - 1)
            frame.yz += segments.pop(0)[1:]
        result.append(frame)
    return result
