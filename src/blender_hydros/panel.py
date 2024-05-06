import logging

import bpy

_log = logging.getLogger(__name__ + ".panel")


class HydrosPanel(bpy.types.Panel):
    bl_label = "Hydros Panel"
    bl_idname = "OBJECT_PT_hydros_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"


def register():
    _log.info(f"Registering hydros panel")
    bpy.utils.register_class(HydrosPanel)


def unregister():
    _log.info(f"Unregistering hydros panel")
    bpy.utils.unregister_class(HydrosPanel)
