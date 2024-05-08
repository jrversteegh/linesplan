import site
import sys
from pathlib import Path

from bpy.types import AddonPreferences
from bpy.props import (
    EnumProperty,
)

log_levels = [
    ("CRITICAL", "Critical", "", 0),
    ("ERROR", "Error", "", 1),
    ("WARNING", "Warning", "", 2),
    ("INFO", "Info", "", 3),
    ("DEBUG", "Debug", "", 4),
    ("NOTSET", "Notset", "", 5),
]

class Preferences(AddonPreferences):
    path = Path(__file__).absolute().parent
    bl_idname = __package__

    logging_level: EnumProperty(
        name="Logging Level",
        items=log_levels,
        default=2,
    )
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        box = layout.box()
        box.label(text="Hydros Module")
        if global_data.registered:
            box.label(text="Registered", icon="CHECKMARK")
            module = check_module("py_slvs")
            if module:
                module_path = module.__path__[0] if module else ""
                box.label(text="Path: " + module_path)
        else:
            row = box.row()
            row.label(text="Module isn't Registered", icon="CANCEL")
            split = box.split(factor=0.8)
            split.prop(self, "package_path", text="")
            split.operator(
                Operators.InstallPackage,
                text="Install from File",
            ).package = self.package_path

            row = box.row()
            row.operator(
                Operators.InstallPackage,
                text="Install from PIP",
            ).package = "py-slvs"

        box = layout.box()
        box.label(text="Debugging")
        col = box.column(align=True)
        col.prop(self, "logging_level")
