import logging

import bpy
import bpy_extras

_log = logging.getLogger(__name__ + ".panel")


class HydrosLoad(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    bl_idname = "object.hydros_load"
    bl_label = "Load"

    def execute(self, context):
        return {"FINISHED"}


class HydrosSave(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    bl_idname = "object.hydros_save"
    bl_label = "Save"

    def execute(self, context):
        return {"FINISHED"}


class HydrosPanel(bpy.types.Panel):
    bl_label = "Hydros"
    bl_idname = "OBJECT_PT_hydros_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Hydros"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.hydros_load", text="Load...")
        layout.operator("object.hydros_save", text="Save...")


def register():
    _log.info(f"Registering hydros panel")
    bpy.utils.register_class(HydrosPanel)
    bpy.utils.register_class(HydrosLoad)
    bpy.utils.register_class(HydrosSave)


def unregister():
    _log.info(f"Unregistering hydros panel")
    bpy.utils.unregister_class(HydrosSave)
    bpy.utils.unregister_class(HydrosLoad)
    bpy.utils.unregister_class(HydrosPanel)
