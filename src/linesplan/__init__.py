import importlib.metadata
metadata = importlib.metadata.metadata("linesplan")

__version__ = metadata["Version"]
__author__ = metadata["Author"]
