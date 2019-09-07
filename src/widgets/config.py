import platform
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
