import importlib
import site
import subprocess
import sys


def get_installed():
    try:
        importlib.import_module("linesplan")
        return True
    except ModuleNotFoundError as e:
        return False


def get_version():
    if get_installed():
        return linesplan.__version__
    else:
        return "Not installed"


def install_pip():
    cmd = [sys.executable, "-m", "ensurepip", "--upgrade"]
    return subprocess.call(cmd) == 0


def ensure_pip():
    if subprocess.call([sys.executable, "-m", "pip", "--version"]) != 0:
        return install_pip()
    return True


def update_pip():
    if not ensure_pip():
        return False
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
    return subprocess.call(cmd) == 0


def install():
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "linesplan"]
    return subprocess.call(cmd) == 0
