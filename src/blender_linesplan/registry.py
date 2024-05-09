import logging

from bpy.utils import register_class as register
from bpy.utils import unregister_class as unregister

from .linesplan import get_installed

_log = logging.getLogger(__name__ + ".registry")


_to_be_registered = []
_registered = []


def register_class(cls):
    _log.info(f"Queueing class {cls} for registration")
    if cls not in _to_be_registered:
        _to_be_registered.append(cls)


def update_registration():
    if get_installed():
        for cls in _to_be_registered.copy():
            register(cls)
            _log.info(f"Registered {cls}")
            _to_be_registered.remove(cls)
            _registered.append(cls)
    else:
        unregister_classes()


def unregister_classes():
    _log.info("Unregistering classes")
    for cls in _registered.copy():
        unregister(cls)
        _log.info(f"Unregistered {cls}")
        _registered.remove(cls)
        _to_be_registered.append(cls)
