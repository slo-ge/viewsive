import platform
from enum import Enum

from cefpython3 import cefpython

cef = cefpython

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Configuration
WIDTH = 800
HEIGHT = 600
WindowUtils = cef.WindowUtils()
START_URL = "https://phipluspi.com"
ZOOM_FACTOR = -1.5


class ViewPortSize(Enum):
    """ original viewport sizes, will automatically be zoomed by ZOOM_FACTOR"""
    MOBILE = 280 * 1.25
    TABLET = 560 * 1.25
    DESKTOP = 900 * 1.25
