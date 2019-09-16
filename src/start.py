import sys

from cefpython3 import cefpython as cef

from widgets.cefapplication import CefApplication
from widgets.config import ZOOM_FACTOR
from widgets.mainwindow import MainWindow


def main():
    """
    See https://github.com/cztomczak/cefpython/blob/master/api/ApplicationSettings.md
    for mor settings
    """
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    # see for more infos
    settings = {
        'auto_zooming': f'{ZOOM_FACTOR}'
    }

    cef.Initialize(settings)
    app = CefApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.activateWindow()
    main_window.raise_()
    app.exec_()
    if not cef.GetAppSetting("external_message_pump"):
        app.stopTimer()
    del main_window  # Just to be safe, similarly to "del app"
    del app  # Must destroy app object before calling Shutdown
    cef.Shutdown()


if __name__ == '__main__':
    main()
