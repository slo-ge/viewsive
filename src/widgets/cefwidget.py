import ctypes

from PyQt5.QtWidgets import QWidget
from cefpython3.cefpython_py37 import PyBrowser, PyFrame

from widgets.config import WindowUtils, cef, FALLBACK_URL, app_state, parser


class CefWidget(QWidget):
    def __init__(self, parent=None, url=None):
        # noinspection PyArgumentList
        super(CefWidget, self).__init__(parent)
        self.url = url
        self.browser: PyBrowser = None
        self.hidden_window = None  # Required for PyQt5 on Linux
        self.show()

    def focusInEvent(self, event):
        if self.browser:
            WindowUtils.OnSetFocus(self.getHandle(), 0, 0, 0)
            self.browser.SetFocus(True)

    def focusOutEvent(self, event):
        # This event seems to never get called on Linux, as CEF is
        # stealing all focus due to Issue #284.
        if self.browser:
            self.browser.SetFocus(False)

    def embedBrowser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.width(), self.height()]
        window_info.SetAsChild(self.getHandle(), rect)
        self.browser = cef.CreateBrowserSync(window_info, url=self.url or FALLBACK_URL)
        self.browser.SetClientHandler(LoadHandler())
        self.browser.SetClientHandler(FocusHandler(self))

        self.javascript_bindings()

    def javascript_bindings(self):
        bindings = cef.JavascriptBindings()
        bindings.SetFunction(
            parser.lookup("py_get_coordinates"),
            self.coordinates_js
        )
        self.browser.SetJavascriptBindings(bindings)

    def getHandle(self):
        try:
            # PyQt4 and PyQt5
            return int(self.winId())
        except Exception as e1:
            # Python 3
            ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
            ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object]
            return ctypes.pythonapi.PyCapsule_GetPointer(self.winId(), None)

    def coordinates_js(self, coordinates: float):
        """ receive coordinates from javascript method

        :param coordinates:
        :return:
        """
        app_state.sync_browser_scroll(int(coordinates))

    def moveEvent(self, _):
        self.x = 0
        self.y = 0
        if self.browser:
            WindowUtils.OnSize(self.getHandle(), 0, 0, 0)
            self.browser.NotifyMoveOrResizeStarted()

    def resizeEvent(self, event):
        if self.browser:
            WindowUtils.OnSize(self.getHandle(), 0, 0, 0)
            self.browser.NotifyMoveOrResizeStarted()

    def load_url(self):
        if self.browser:
            self.browser.LoadUrl(self.url.text())


class FocusHandler(object):
    def __init__(self, cef_widget):
        self.cef_widget = cef_widget

    def OnSetFocus(self, **_):
        pass

    def OnGotFocus(self, browser, **_):
        pass


class LoadHandler(object):
    def __init__(self):
        self.initial_app_loading = True

    def OnLoadingStateChange(self, **_):
        frame = _['browser'].GetMainFrame()  # type: PyFrame
        frame.ExecuteJavascript(parser.source)
        frame.ExecuteFunction(parser.js_init)

    def OnLoadStart(self, browser, **_):
        if not self.initial_app_loading:
            # TODO: url sync is not active
            print('url sync is not active')
            # app_state.update_url(browser.GetUrl())
        self.initial_app_loading = False
