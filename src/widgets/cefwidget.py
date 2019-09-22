import ctypes

from PyQt5.QtWidgets import QWidget
from cefpython3.cefpython_py37 import PyBrowser, PyFrame

from widgets.config import WindowUtils, cef, START_URL, app_state


class CefWidget(QWidget):
    def __init__(self, parent=None):
        # noinspection PyArgumentList
        super(CefWidget, self).__init__(parent)
        self.browser: PyBrowser = None
        self.hidden_window = None  # Required for PyQt5 on Linux
        self.show()
        self.init_subscribers()

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
        def get_coordinates(coordinates: float):
            """ receive coordinates from browser
            
            :param coordinates: 
            :return: 
            """
            print("Value sent from Javascript: " + str(coordinates))

        window_info = cef.WindowInfo()
        rect = [0, 0, self.width(), self.height()]
        window_info.SetAsChild(self.getHandle(), rect)
        self.browser = cef.CreateBrowserSync(window_info, url=START_URL)
        self.browser.SetClientHandler(LoadHandler())
        self.browser.SetClientHandler(FocusHandler(self))
        bindings = cef.JavascriptBindings()
        bindings.SetFunction("py_get_coordinates", get_coordinates)
        self.browser.SetJavascriptBindings(bindings)
        # print(frame.ViewSource())

    def getHandle(self):
        try:
            # PyQt4 and PyQt5
            return int(self.winId())
        except Exception as e1:
            # Python 3
            ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
            ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object]
            return ctypes.pythonapi.PyCapsule_GetPointer(self.winId(), None)

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

    def init_subscribers(self):
        """"""
        app_state.get_navigation_url_subscription().subscribe(self.change_url)

    def change_url(self, url):
        self.browser.LoadUrl(url)


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
        # TODO: call update navbar widget, but now in state managment
        print('on loading state change')
        # app_state.update_url(_['browser'].GetUrl())
        # self.navigation_bar.update_state()

        frame = _['browser'].GetMainFrame()  # type: PyFrame
        # TODO: listen to scroll top event
        frame.ExecuteJavascript("""
        
        function test() {
          window.onscroll = function(event) {
             console.log(document.documentElement.scrollTop);
             py_get_coordinates(document.documentElement.scrollTop);
          };
        }
        
        """)
        frame.ExecuteFunction('test')

    def OnLoadStart(self, browser, **_):
        if not self.initial_app_loading:
            app_state.update_url(browser.GetUrl())

        self.initial_app_loading = False

        # TODO: we just set the focus
        # if self.initial_app_loading:
        #    self.navigation_bar.cef_widget.setFocus()
        #    self.initial_app_loading = False
