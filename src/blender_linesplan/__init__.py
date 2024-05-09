import logging

import bpy

bl_info = {
    "name": "Linesplan",
    "author": "J.R. Versteegh",
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "location": "View3D > UI > Linesplan",
    "description": "Ship linesplans and hydrostatics",
    "category": "3D View",
    "license": "GPL",
    "warning": "In development",
    "doc_url": "https://github.com/jrversteegh/linesplan/README.md",
    "tracker_url": "https://github.com/jrversteegh/linesplan",
    "link": "https://www.orca-st.com/",
    "support": "COMMUNITY",
}

__version__ = ".".join([str(i) for i in bl_info["version"]])
__author__ = bl_info["author"]

from .lines import get_installed
from .panel import register as register_panel
from .panel import unregister as unregister_panel
from .preferences import register as register_preferences
from .preferences import unregister as unregister_preferences

_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)
_log.addHandler(logging.StreamHandler())


def register():
    _log.info("Registering linesplan add-in")
    register_preferences()
    if get_installed():
        register_panel()


def unregister():
    _log.info("Unregistering linesplan add-in")
    unregister_preferences()
    if get_installed():
        unregister_panel()
