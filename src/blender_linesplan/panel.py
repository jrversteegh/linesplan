import logging

import bpy
import bpy_extras

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


def register():
    _log.info(f"Registering linesplan panel")
    bpy.utils.register_class(LinesplanPanel)
    bpy.utils.register_class(LinesplanLoad)
    bpy.utils.register_class(LinesplanSave)


def unregister():
    _log.info(f"Unregistering linesplan panel")
    bpy.utils.unregister_class(LinesplanSave)
    bpy.utils.unregister_class(LinesplanLoad)
    bpy.utils.unregister_class(LinesplanPanel)
