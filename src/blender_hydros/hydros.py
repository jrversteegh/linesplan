import importlib
import site
import subprocess
import sys


def get_installed():
    try:
        importlib.import_module("hydros")
        return True
    except ModuleNotFoundError as e:
        return False


def get_version():
    if get_installed():
        return hydros.__version__
    else:
        return "Not installed"


def _install_pip():
    cmd = [sys.executable, "-m", "ensurepip", "--upgrade"]
    subprocess.call(cmd)


def _ensure_pip():
    if subprocess.call([sys.executable, "-m", "pip", "--version"]):
        _install_pip()


def _update_pip():
    _ensure_pip
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
    subprocess.call(cmd)


def install():
    _update_pip()
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "hydros"]
    subprocess.call(cmd)
