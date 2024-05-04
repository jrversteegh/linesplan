import copy
import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simpson, trapezoid
from scipy.optimize import newton_krylov


class Frame:
    x = 0.0

    def __init__(self, *args, **kwargs):
        super().__init__()
        if len(args) > 0:
            self.yz = args[0][:]
        else:
            self.yz = []
        if "x" in kwargs:
            self.x = float(kwargs["x"])
        self.chines = []

    def scale(self, factor):
        scaled = np.asarray(self.yz) * factor
        self.yz = [list(i) for i in scaled]

    def offset(self, vector):
        offset = np.asarray(self.yz) + np.asarray(vector)
        self.yz = [list(i) for i in offset]


class Lines:

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.frames = []
        self.name = ""

    def close_frames(self, margin=5e-3):
        for frame in self.frames:
            if frame.yz[0][0] < margin:
                frame.yz[0][0] = 0.0
            else:
                frame.chines.insert(0, 1)
                frame.yz.insert(0, [0.0, frame.yz[0][1]])

            if frame.yz[-1][0] < margin:
                frame.yz[-1][0] = 0.0
            else:
                frame.chines.append(len(frame.yz) - 1)
                frame.yz.append([0.0, frame.yz[-1][1]])

    def scale(self, factor):
        for frame in self.frames:
            frame.scale(factor)

    def save(self, filename):
        save_lines_plan(self, filename)


def load_lines_plan(filename):
    result = Lines()
    with open(filename) as f:
        data = json.loads(f.read())
        result.name = data["name"]
        for f in data["frames"]:
            frame = Frame()
            frame.x = f["x"]
            frame.yz = f["yz"]
            if "chines" in f:
                frame.chines = f["chines"]
            result.frames.append(frame)
    return result


def save_lines_plan(lines, filename):
    frames = [{"x": fr.x, "yz": fr.yz, "chines": fr.chines} for fr in lines.frames]
    s = json.dumps({"name": lines.name, "frames": frames}, indent=2)
    with open(filename, "w") as f:
        f.write(s)


def plot_frames(
    frames,
    title=None,
    show_legend=False,
    show_waterline=None,
    filename=None,
    ylim=None,
    xlim=None,
    cb=None,
):
    plt.clf()
    if title:
        plt.title(title)
    for i, frame in enumerate(frames):
        a = np.asarray(frame.yz)
        plt.plot(a.T[0, :], a.T[1, :], label=str(i))
    if show_legend:
        plt.legend()
    if show_waterline is not None:
        plt.axhline(y=show_waterline, color="b")
    if cb is not None:
        plt.scatter(cb[1], cb[2], marker="o", s=10, c="#000000")
        plt.axvline(x=cb[1], color="black", linestyle="--", linewidth=1)
    plt.axis("equal")
    if ylim is not None:
        plt.ylim(*ylim)
    if xlim is not None:
        plt.xlim(*xlim)
    if filename is None:
        plt.show()
    else:
        plt.savefig("%s.png" % filename)


def plot_waterlines(
    frames,
    drafts_ap,
    drafts_fp=None,
    title=None,
    show_frames=False,
    show_legend=False,
    filename=None,
):
    plt.clf()
    if title:
        plt.title(title)
    waterlines = get_waterlines(frames, drafts_ap, drafts_fp)
    for i, waterline in enumerate(waterlines):
        if not waterline:
            continue
        waterline = np.asarray(waterline)
        plt.plot(waterline.T[0, :], waterline.T[1, :], label=str(i))
    if show_frames:
        i = 0
        for x, y, z in waterlines[-1]:
            plt.plot([x, x], [0, y], label=str(i))
            i += 1
    plt.axis("equal")
    if filename is None:
        plt.show()
    else:
        plt.savefig("%s.png" % filename)


def line_segments(line):
    if len(line) < 2:
        return []
    line = np.asarray(line)
    segments = line[1:] - line[:-1]
    return [list(i) for i in segments]


def line_lengths(line):
    if len(line) < 2:
        return []
    line = np.asarray(line)
    segments = line[1:] - line[:-1]
    segments *= segments
    lengths = np.sqrt(segments[:, 0] + segments[:, 1])
    return list(lengths)


def get_waterline_points(frame, draft):
    result = []
    prev = [0, 0]
    points = frame.yz
    for coord in points:
        prev_sub = draft - prev[1]
        new_sub = draft - coord[1]
        if prev_sub * new_sub < 0:
            dz = coord[1] - prev[1]
            dy = coord[0] - prev[0]
            if dz != 0:
                new = [prev[0] + prev_sub / dz * dy, draft]
            else:
                new = [prev[0], draft]
            result.append(new)
        prev = coord
    return result


def get_submerged_frame(frame, draft):
    result = Frame(x=frame.x)
    points = frame.yz
    prev = frame.yz[0]
    for coord in points:
        prev_sub = draft - prev[1]
        new_sub = draft - coord[1]
        if prev_sub * new_sub < 0:
            dz = coord[1] - prev[1]
            dy = coord[0] - prev[0]
            if dz != 0:
                new = [prev[0] + prev_sub / dz * dy, draft]
            else:
                new = [prev[0], draft]
            result.yz.append(new)
        if new_sub >= 0:
            result.yz.append(coord)
        prev = coord
    return result


def get_cross_section(frame, full=False):
    if not len(frame.yz):
        return 0.0
    a = np.asarray(frame.yz)
    return trapezoid(a[:, 0], a[:, 1]) * (2 - full)


def get_mom_y(frame):
    if not len(frame.yz):
        return 0.0
    a = np.asarray(frame.yz)
    dz = a[1:, 1] - a[:-1, 1]
    yy = a[:-1, 0] ** 2 + a[:-1, 0] * a[1:, 0] + a[1:, 0] ** 2
    return np.sum(dz * yy) / 6.0


def get_mom_z(frame):
    if not len(frame.yz):
        return 0.0
    a = np.asarray(frame.yz)
    dz = a[1:, 1] - a[:-1, 1]
    yz = 2 * (a[:-1, 1] * a[:-1, 0] + a[1:, 1] * a[1:, 0]) + (
        a[:-1, 1] * a[1:, 0] + a[1:, 1] * a[:-1, 0]
    )
    return np.sum(dz * yz) / 6.0


def get_submerged_frames(frames, draft_ap, draft_fp=None):
    if draft_fp is None:
        draft_fp = draft_ap
    xs = np.array([frame.x for frame in frames])
    drafts = xs / (xs[-1] - xs[0]) * (draft_fp - draft_ap) + draft_ap
    return [get_submerged_frame(frame, draft) for frame, draft in zip(frames, drafts)]


def get_displacement(frames, draft_ap, draft_fp=None, full=False):
    submerged_frames = get_submerged_frames(frames, draft_ap, draft_fp)
    xs = np.array([frame.x for frame in frames])
    cross_sections = [
        get_cross_section(submerged, full) for submerged in submerged_frames
    ]
    disp = simpson(cross_sections, x=xs)
    return disp


def get_lcb(frames, draft_ap, draft_fp=None):
    submerged_frames = get_submerged_frames(frames, draft_ap, draft_fp)
    xs = np.array([frame.x for frame in frames])
    cross_sections = [get_cross_section(submerged) for submerged in submerged_frames]
    disp = simpson(cross_sections, x=xs)
    mom = simpson(cross_sections * xs, x=xs)
    return mom / disp


def get_waterline(frames, draft_ap, draft_fp=None):
    result = []
    if draft_fp is None:
        draft_fp = draft_ap
    xs = np.array([frame.x for frame in frames])
    drafts = xs / (xs[-1] - xs[0]) * (draft_fp - draft_ap) + draft_ap
    waterline_points_list = [
        (frame.x, get_waterline_points(frame, draft))
        for frame, draft in zip(frames, drafts)
    ]
    # Pop empty items from front and back (frames not touching the waterline)
    while waterline_points_list and not waterline_points_list[-1][1]:
        waterline_points_list.pop(-1)
    while waterline_points_list and not waterline_points_list[0][1]:
        waterline_points_list.pop(0)

    direction = -1
    # Start at the bow
    i = len(waterline_points_list)
    if i < 2:
        # If there are fewer than 2 points, there is no line
        return result
    while True:
        i += direction
        if i < 0 or i == len(waterline_points_list):
            direction = -direction
            i += 2 * direction

        waterline_points = waterline_points_list[i]
        if not waterline_points[1]:
            break
        p = waterline_points[1].pop(-1)
        result.append([waterline_points[0], p[0], p[1]])
    result.reverse()
    return result


def get_waterline_properties(waterline):
    area, momx, momx2, momy, momy2 = 0.0, 0.0, 0.0, 0.0, 0.0
    for p1, p2 in zip(waterline[:-1], waterline[1:]):
        x1, x2, y1, y2 = p1[0], p2[0], p1[1], p2[1]
        area += (x2 - x1) * (y1 + y2) / 2.0
        momx += (x2 - x1) * (y1**2 + y1 * y2 + y2**2) / 6.0
        momx2 += (x2 - x1) * (y1**3 + y1 * y2**2 + y1**2 * y2 + y2**3) / 12.0
        momy += (x2 - x1) * (2 * (x1 * y1 + x2 * y2) + (x1 * y2 + x2 * y1)) / 6.0
        momy2 += (
            (x2 - x1)
            * (
                y1 * (3 * x1**2 + 1 * x2**2 + 2 * x1 * x2)
                + y2 * (1 * x1**2 + 3 * x2**2 + 2 * x1 * x2)
            )
            / 12.0
        )
    return area, momx, momx2, momy, momy2


def get_waterlines(frames, drafts_ap, drafts_fp=None):
    if drafts_fp is None:
        drafts_fp = drafts_ap
    result = []
    for tap, tfp in zip(drafts_ap, drafts_fp):
        waterline = get_waterline(frames, tap, tfp)
        result.append(waterline)
    return result


def get_bm(frames, draft_ap, draft_fp=None):
    waterline = get_waterline(frames, draft_ap, draft_fp)
    a, mx, mx2, my, my2 = get_waterline_properties(waterline)
    dispvol = get_displacement(frames, draft_ap, draft_fp)
    return 2 * mx2 / dispvol


def get_kb(frames, draft_ap, draft_fp=None):
    if draft_fp is None:
        draft_fp = draft_ap
    max_draft = max(draft_fp, draft_ap)
    drafts_ap = np.linspace(draft_ap - max_draft, draft_ap, 41)
    drafts_fp = np.linspace(draft_fp - max_draft, draft_fp, 41)
    trim_aft = max_draft == draft_ap
    waterlines = get_waterlines(frames, drafts_ap, drafts_fp)
    areas = [get_waterline_properties(waterline)[0] for waterline in waterlines]
    drafts = drafts_ap if trim_aft else drafts_fp
    dispvol = simpson(areas, x=drafts)
    m = simpson(areas * drafts, x=drafts)
    return m / dispvol


def get_km(frames, draft_ap, draft_fp=None):
    return get_bm(frames, draft_ap, draft_fp) + get_kb(frames, draft_ap, draft_fp)


def get_lcf(frames, draft_ap, draft_fp=None):
    waterline = get_waterline(frames, draft_ap, draft_fp)
    a, mx, mx2, my, my2 = get_waterline_properties(waterline)
    return my / a


def get_hull_volume(frames):
    xs = np.array([frame.x for frame in frames])
    cross_sections = [get_cross_section(frame) for frame in frames]
    vol = simpson(cross_sections, x=xs)
    return vol


def get_hull_areas(frames, deck_chine=-1):
    hull = []
    deck = []
    xs = np.array([frame.x for frame in frames])
    for frame in frames:
        chine_index = frame.chines[deck_chine]
        hull.append(np.sum(line_lengths(frame.yz[: chine_index + 1])))
        deck.append(np.sum(line_lengths(frame.yz[chine_index:])))
    ha = 2 * simpson(np.asarray(hull), x=xs)
    da = 2 * simpson(np.asarray(deck), x=xs)
    return ha, da


def get_wetted_surface(frames, draft_ap, draft_fp=None):
    xs = np.array([frame.x for frame in frames])
    submerged_frames = get_submerged_frames(frames, draft_ap, draft_fp)
    lengths = [np.sum(line_lengths(submerged.yz)) for submerged in submerged_frames]
    return 2 * simpson(np.asarray(lengths), x=xs)


def get_full_frames(frames):
    result = []
    for frame in frames:
        full_frame = Frame(x=frame.x)
        starboard = [[-y, z] for y, z in reversed(frame.yz)]
        port = [[y, z] for y, z in frame.yz]
        full_frame.yz = np.asarray(starboard + port)
        result.append(full_frame)
    return result


def get_rotated_frames(full_frames, phi):
    result = []
    for frame in full_frames:
        new_frame = Frame(x=frame.x)
        new_frame.yz = np.zeros_like(frame.yz)
        new_frame.yz[:, 0] = np.cos(phi) * frame.yz[:, 0] + np.sin(phi) * frame.yz[:, 1]
        new_frame.yz[:, 1] = (
            -np.sin(phi) * frame.yz[:, 0] + np.cos(phi) * frame.yz[:, 1]
        )
        result.append(new_frame)
    return result


def submerge_frames(full_frames, draft, trim=0):
    draft_ap = draft
    draft_fp = draft - trim
    xs = np.array([frame.x for frame in full_frames])
    drafts = xs / (xs[-1] - xs[0]) * (draft_fp - draft_ap) + draft_ap
    for i, frame in enumerate(full_frames):
        frame.yz[:, 1] -= drafts[i]
    submerged_frames = get_submerged_frames(full_frames, 0)
    cross_sections = [
        get_cross_section(submerged, full=True) for submerged in submerged_frames
    ]
    mom_ys = [get_mom_y(submerged) for submerged in submerged_frames]
    mom_zs = [get_mom_z(submerged) for submerged in submerged_frames]
    disp = simpson(cross_sections, x=xs)
    momx = simpson(cross_sections * xs, x=xs)
    momy = simpson(mom_ys, x=xs)
    momz = simpson(mom_zs, x=xs)
    return disp, momx / disp, momy / disp, momz / disp


def float_frames(full_frames, dispvol, lcb):
    def submerge(draft_trim):
        draft, trim = draft_trim
        ff = copy.deepcopy(full_frames)
        v, x = submerge_frames(ff, draft, trim)[:2]
        return dispvol - v, lcb - x

    main_frame = full_frames[len(full_frames) // 2]
    draft_guess = get_mom_z(main_frame) / get_cross_section(main_frame, full=True)

    return newton_krylov(submerge, [draft_guess, 0])
