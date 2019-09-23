from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QLabel, QSizePolicy

from widgets.cefwidget import CefWidget
from widgets.config import ZOOM_FACTOR, ViewPortSize, cef, app_state


class BrowserWindow(CefWidget):
    def __init__(self, name, initial_width: ViewPortSize, parent=None):
        super(BrowserWindow, self).__init__(parent)

        self.initial_width = initial_width.value  # unpack dict value
        self.name = name
        self.viewport_label = QLabel()
        self._apply_widget_settings()
        self.init_subscribers()
        self.scroll_top_position: int = 0

    def init_subscribers(self):
        """"""
        app_state.get_navigation_url_subscription().subscribe(self.change_url)

    def _apply_widget_settings(self):
        """ make global widget settings here """
        self.viewport_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.viewport_label.setAlignment(Qt.AlignCenter)

    def sizeHint(self):
        return QSize(self.initial_width, 1000)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.viewport_label.setText(self.build_viewport_label())

    def build_viewport_label(self):
        return (
            f'{self.name}  |  Viewport: {self.size().width()} px'
            f' (Zoom: {ZOOM_FACTOR} as {self.size().width() * abs(ZOOM_FACTOR)})'
        )

    def embedBrowser(self):
        super(BrowserWindow, self).embedBrowser()
        bindings = cef.JavascriptBindings()
        bindings.SetFunction("py_get_coordinates", self.coordinates_js)
        self.browser.SetJavascriptBindings(bindings)

    def change_url(self, url):
        self.browser.LoadUrl(url)

    def coordinates_js(self, coordinates: float):
        """ receive coordinates from javascript method

        :param coordinates:
        :return:
        """
        self.scroll_top_position = int(coordinates)
        print("Value sent from Javascript: " + str(coordinates))
