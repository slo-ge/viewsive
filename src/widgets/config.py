from enum import Enum
from pathlib import Path

from cefpython3 import cefpython

from utils.appstore import AppState
from utils.utils import JavaScriptBindingParser

cef = cefpython

# Configuration
WIDTH = 800
HEIGHT = 600
WindowUtils = cef.WindowUtils()
FALLBACK_URL = "https://phipluspi.com/project"
ZOOM_FACTOR = -1.5

# Syncs browser urls over different windows
BROWSER_SYNCHRONIZATION = True

app_state = AppState()

data_folder = Path("src/utils")
file_to_open = data_folder / "utils.js"
parser = JavaScriptBindingParser()
javascript = parser.from_file(file_to_open)

config_file = data_folder / "config.yaml"  # yaml config