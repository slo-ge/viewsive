from enum import Enum

from cefpython3 import cefpython

from utils.appstore import AppState

cef = cefpython

# Configuration
WIDTH = 800
HEIGHT = 600
WindowUtils = cef.WindowUtils()
START_URL = "https://phipluspi.com"
ZOOM_FACTOR = -1.5

# Syncs browser urls over different windows
BROWSER_SYNCHRONIZATION = True

app_state = AppState()

class ViewPortSize(Enum):
    """ original viewport sizes, will automatically be zoomed by ZOOM_FACTOR"""
    MOBILE = 280 * 1.25
    TABLET = 560 * 1.25
    DESKTOP = 900 * 1.25
