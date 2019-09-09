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


# def get_browser_views(parent: QMainWindow):
#    return [
#        BrowserWindow('Phone', 320, parent=parent),
#        BrowserWindow('Tablet', 568, parent=parent),
#        BrowserWindow('Desktop', 1024, parent=parent)
#    ]


class ViewPortSizes(Enum):
    MOBILE = 320
    TABLET = 768
    DESKTOP = 1024
