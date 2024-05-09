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

from . import panel
from .linesplan import get_installed
from .preferences import get_prefs
from .preferences import register as register_preferences
from .preferences import unregister as unregister_preferences
from .registry import unregister_classes, update_registration

_log = logging.getLogger(__name__)


def setup_log():
    prefs = get_prefs
    _log.setLevel(prefs.logging_level)
    _log.addHandler(logging.StreamHandler())


def register():
    register_preferences()
    setup_log()
    _log.info("Registering linesplan add-in")
    update_registration()


def unregister():
    _log.info("Unregistering linesplan add-in")
    unregister_classes()
    unregister_preferences()
