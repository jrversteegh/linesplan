import logging

import bpy
import bpy_extras

from .model import load_model, save_model
from .registry import register_class

_log = logging.getLogger(__name__ + ".panel")


_lines = None


class LinesplanLoad(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    bl_idname = "object.linesplan_load"
    bl_label = "Load linesplan"

    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={"HIDDEN"},
        maxlen=255,
    )

    def execute(self, context):
        global _lines
        _log.info(f"Opening file: {self.filepath}")
        load_model(self.filepath)
        return {"FINISHED"}


class LinesplanSave(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "object.linesplan_save"
    bl_label = "Save linesplan"

    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={"HIDDEN"},
        maxlen=255,
    )

    def execute(self, context):
        _log.info(f"Saving file: {self.filepath}")
        save_model(self.filepath)
        return {"FINISHED"}


class LinesplanPanel(bpy.types.Panel):
    bl_label = "Linesplan"
    bl_idname = "OBJECT_PT_linesplan_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Linesplan"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.linesplan_load", text="Load...")
        layout.operator("object.linesplan_save", text="Save...")


register_class(LinesplanLoad)
register_class(LinesplanSave)
register_class(LinesplanPanel)
