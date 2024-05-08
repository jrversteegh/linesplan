import logging

import bpy

bl_info = {
    "name": "Hydros",
    "author": "J.R. Versteegh",
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "location": "View3D > UI > Hydros",
    "description": "Ship linesplan and hydrostatics",
    "category": "3D View",
    "license": "GPL",
    "warning": "In development",
    "doc_url": "https://www.orca-st.com/",
    "tracker_url": "https://www.orca-st.com/",
    "link": "https://www.orca-st.com/",
    "support": "COMMUNITY",
}

__version__ = ".".join([str(i) for i in bl_info["version"]])
__author__ = bl_info["author"]

from .hydros import get_installed
from .panel import register as register_panel
from .panel import unregister as unregister_panel
from .preferences import register as register_preferences
from .preferences import unregister as unregister_preferences

_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)
_log.addHandler(logging.StreamHandler())


def register():
    _log.info("Registering hydros add-in")
    register_preferences()
    if get_installed():
        register_panel()


def unregister():
    _log.info("Unregistering hydros add-in")
    unregister_preferences()
    if get_installed():
        unregister_panel()
