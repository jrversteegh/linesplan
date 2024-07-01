import bpy

from linesplan import Lines, load_lines_plan, save_lines_plan

models = []


class Model:
    lines: Lines = None
    frames = None

    def __init__(self, filename):
        self.lines = load_lines_plan(filename)
        self.setup_frames()

    def save(self, filename):
        save_lines_plan(self.lines, filename)

    def setup_frames(self):
        scene = bpy.context.scene
        for i, frame in enumerate(self.lines.frames):
            curve = bpy.data.curves.new(name=f"Frame_{i}", type="CURVE")
            j = 0
            x = frame.x

            def add_spline(c):
                points = [(y, z) for (y, z) in frame.yz[j : c + 1]]
                spline = curve.splines.new(type="POLY")
                spline.points.add(len(points) - 1)
                for k, (y, z) in enumerate(points):
                    spline.points[k].co = x, y, z, 1
                return c

            for c in frame.chines:
                j = add_spline(c)
            add_spline(len(frame))
            curve_obj = bpy.data.objects.new(f"{curve.name}_Object", curve)
            scene.collection.objects.link(curve_obj)


def load_model(filename):
    models.append(Model(filename))


def save_model(filename):
    if models:
        models[0].save(filename)
