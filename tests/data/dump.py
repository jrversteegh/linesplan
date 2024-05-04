#!/usr/bin/env python

import copy
import os
import sys

scriptdir = os.path.dirname(os.path.realpath(__file__))
_module_path = scriptdir + "/.."
sys.path.insert(0, _module_path)

from hydros.dxfreader import *
from hydros.linesplan import *

dxf = Dxf("tally_ho.dxf")

lines = []
arcs = []
# lines = dxf.get_lines(block='bodyplan forward')
splines_fwd = dxf.get_splines(block="bodyplan forward")
splines_fwd.pop(14)  # Deck line
splines_fwd.pop(13)  # Keel line
splines_fwd.pop(0)  # Main frame: duplicated in aft frame set

arcs_fwd = dxf.get_arcs(block="bodyplan forward")
arcs_fwd.pop(0)  # Main frame: duplicated in aft frame set

# lines += dxf.get_lines(block='bodyplan aft')
splines_aft = dxf.get_splines(block="bodyplan aft")
splines_aft.pop(-1)  # Aft pot lid/cap rail
splines_aft.pop(-1)  # Deck line 1
splines_aft.pop(-3)  # Deck line 2
splines_aft.pop(9)  # Transom
splines_aft.pop(8)  # Aft keel line

arcs_aft = dxf.get_arcs(block="bodyplan aft")
arcs_aft.pop(-1)  # Transom cap rail
arcs_aft.pop(-1)  # Transom deck line


def point_up(lines):
    for line in lines:
        if line[-1][1] < line[0][1]:
            line.reverse()


def flip_right(lines):
    for line in lines:
        if line[-2][0] < 0:
            for p in line:
                p[0] = -p[0]


def get_frames(splines, arcs):
    splines = [spline.to_line() for spline in splines]
    point_up(splines)
    flip_right(splines)
    arcs = [arc.to_line() for arc in arcs]
    point_up(arcs)
    flip_right(arcs)

    intersects = 0
    join_map = {}
    # Find intersections of arc ends with frame splines
    for i, arc in enumerate(arcs):
        p0 = [arc[0]]
        intersect_found = False
        for j, spline in enumerate(splines):
            segs = np.asarray(line_segments(spline))
            vecs = (np.asarray(p0) - np.asarray(spline))[:-1]
            dot = np.sum(vecs * segs, axis=1)
            lvecs = np.linalg.norm(vecs, axis=1)
            lsegs = np.maximum(np.linalg.norm(segs, axis=1), lvecs)
            l2 = lvecs * lsegs
            small = (l2 - dot) < 5e-2
            small_count = np.sum(small)
            if small_count == 0:
                pass  # Spline doesn't touch the arc
            elif small_count == 1:
                k = int(np.arange(len(l2))[small])
                join_map[i] = j, k
                intersect_found = True
            else:
                # Multiple frame segments touch the arc??
                print("Unexpected small count of %s" % small_count)
        if not intersect_found:
            # Arc doesn't touch any frame
            print("No intersection found for arc: %d" % i)

    # Now chop of the top of the frames
    for arci, v in join_map.items():
        spli, pi = v
        chopped = splines[spli][: pi + 1]
        chopped.append(arcs[arci][0])
        splines[spli] = chopped

    lines = arcs + splines

    frames = collect_frames(lines)
    frames.sort(key=lambda f: f.yz[f.chines[0]])
    return frames


frames_fwd = get_frames(splines_fwd, arcs_fwd)
frames_fwd.reverse()
frames_aft = get_frames(splines_aft, arcs_aft)
frames = frames_aft + frames_fwd
for i, frame in enumerate(frames):
    frame.x = i * 0.3048

lines = Lines()
lines.name = "Tally Ho"
lines.frames = frames
lines.scale(0.001)
lines.close_frames()
plot_lines_plan(lines, show_legend=True)
save_lines_plan(lines, "tally_ho.json")

persp1_lines = copy.deepcopy(lines)
persp2_lines = copy.deepcopy(lines)
persp3_lines = copy.deepcopy(lines)
for i in range(len(lines.frames)):
    f1 = persp1_lines.frames[i]
    f2 = persp2_lines.frames[i]
    f3 = persp3_lines.frames[i]
    j = 44 - i
    f1.scale(1 - j * 0.007)
    f2.scale(1 - j * 0.007)
    f3.scale(1 - i * 0.007)
    f1.offset([j * 0.1, j * 0.05])
    f2.offset([j * 0.1, j * -0.03])
    f3.offset([i * 0.1, i * -0.03])

plot_lines_plan(persp1_lines)
plot_lines_plan(persp2_lines)
plot_lines_plan(persp3_lines)
