import importlib.metadata

metadata = importlib.metadata.metadata("linesplan")

__version__ = metadata["Version"]
__author__ = metadata["Author"]

from .lines import Frame, Lines, load_lines_plan, save_lines_plan
