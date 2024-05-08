import logging
import site
import sys
from pathlib import Path

import bpy
from bpy.props import EnumProperty, StringProperty
from bpy.types import AddonPreferences, Operator

from .hydros import ensure_pip, get_installed, get_version, install, update_pip

_log = logging.getLogger(__name__ + ".preferences")

log_levels = [
    ("CRITICAL", "Critical", "", 0),
    ("ERROR", "Error", "", 1),
    ("WARNING", "Warning", "", 2),
    ("INFO", "Info", "", 3),
    ("DEBUG", "Debug", "", 4),
    ("NOTSET", "Notset", "", 5),
]


class InstallPackage(Operator):
    """Install module from local .whl file or from PyPi"""

    bl_idname = "view3d.hydros_install_package"
    bl_label = "Install/update"

    package: StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        if not ensure_pip():
            self.report(
                {"WARNING"},
                "PIP is not available and cannot be installed, please install PIP manually",
            )
            return {"CANCELLED"}

        if not self.package:
            self.report({"WARNING"}, "Specify package to be installed")
            return {"CANCELLED"}

        if not update_pip():
            self.report({"WARNING"}, "Failed to update pip")

        if not install():
            self.report({"WARNING"}, "Failed to install hydros")
            return {"CANCELLED"}

        return {"FINISHED"}


class Preferences(AddonPreferences):
    path = Path(__file__).absolute().parent
    bl_idname = __package__

    package_path: StringProperty(
        name="Hydros package filepath",
        description="Filepath to the hydro's .whl file",
        subtype="FILE_PATH",
        default="",
    )

    logging_level: EnumProperty(
        name="Logging level",
        items=log_levels,
        default=2,
    )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        box = layout.box()
        box.label(text="Hydros Module")
        if get_installed():
            box.label(text="Installed", icon="CHECKMARK")
            box.label(text="Version: " + get_version())
        else:
            row = box.row()
            row.label(text="Hydros isn't installed", icon="CANCEL")
            split = box.split(factor=0.8)
            split.prop(self, "package_path", text="")
            split.operator(
                "view3d.hydros_install_package",
                text="Install from File",
            ).package = self.package_path

            row = box.row()
            row.operator(
                "view3d.hydros_install_package",
                text="Install from PIP",
            ).package = "hydros"

        box = layout.box()
        box.label(text="Debugging")
        col = box.column(align=True)
        col.prop(self, "logging_level")


def register():
    _log.info(f"Registering preferences")
    bpy.utils.register_class(InstallPackage)
    bpy.utils.register_class(Preferences)


def unregister():
    _log.info(f"Unregistering preferences")
    bpy.utils.unregister_class(Preferences)
    bpy.utils.unregister_class(InstallPackage)
