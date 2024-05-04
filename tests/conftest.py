import logging
import os
import sys
import time
import unittest
from datetime import datetime

import __main__ as main

scriptdir = os.path.dirname(os.path.realpath(__file__))
_module_path = scriptdir + "/.."
sys.path.insert(0, _module_path)

os.chdir(scriptdir)
if not os.path.exists("output"):
    os.mkdir("output")
filename = os.path.basename(main.__file__)
_logname = scriptdir + "/output/" + os.path.splitext(filename)[0] + ".log"

logging.basicConfig(
    filename=_logname,
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

log = logging.getLogger("test")


def log_line():
    log.info("==============================================")


def file_exists(filename):
    return os.path.exists(filename)


def file_age(filename):
    return time.time() - os.path.getmtime(filename)


log_line()
log.info("Started logging: %s" % str(datetime.now()))
log_line()
