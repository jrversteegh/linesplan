import logging

import bpy
import bpy_extras

from .registry import register_class

_log = logging.getLogger(__name__ + ".panel")


class LinesplanLoad(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    bl_idname = "object.linesplan_load"
    bl_label = "Load"

    def execute(self, context):
        return {"FINISHED"}


class LinesplanSave(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    bl_idname = "object.linesplan_save"
    bl_label = "Save"

    def execute(self, context):
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
