from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy

from widgets.cefwidget import CefWidget
from widgets.config import WINDOWS
from widgets.navigationbar import NavigationBar


class MainWindow(QMainWindow):
    """ defines the layout and append ui element including the cef widget"""

    def __init__(self):
        super(MainWindow, self).__init__(None)
        # Avoids crash when shutting down CEF (issue #360)
        self.browser_windows: [BrowserWindow] = []

        self.navigation_bar = None
        self.setWindowTitle("PyQt5 example")
        self.setFocusPolicy(Qt.StrongFocus)
        self.setup_layout()

    def setup_layout(self):
        # self.resize(WIDTH, HEIGHT)
        self.browser_windows.append(BrowserWindow('Phone', 320, parent=self))
        self.browser_windows.append(BrowserWindow('Tablet', 568, parent=self))
        self.browser_windows.append(BrowserWindow('Desktop', 1024, parent=self))

        # append just the first window
        self.navigation_bar = NavigationBar(self.browser_windows)

        layout = QVBoxLayout()
        layout.addWidget(self.navigation_bar)
        hbox = QHBoxLayout()

        browser_window: BrowserWindow
        for browser_window in self.browser_windows:
            vbox = QVBoxLayout()
            vbox.addWidget(browser_window.viewport_label)
            vbox.addWidget(browser_window)
            hbox.addLayout(vbox)

        layout.addLayout(hbox)

        # append main window layout
        frame = QFrame()
        frame.setLayout(layout)
        self.setCentralWidget(frame)

        if WINDOWS:
            self.show()

        # Browser can be embedded only after layout was set up
        # NOTE: this is important to show the browser window
        for browser_window in self.browser_windows:
            browser_window.embedBrowser()

    def closeEvent(self, event):
        # Close browser (force=True) and free CEF reference
        for browser_window in self.browser_windows:
            browser_window.embedBrowser()

            if browser_window.browser:
                browser_window.browser.CloseBrowser(True)
                self.clear_browser_references()

    def clear_browser_references(self):
        self.browser_windows = []


class BrowserWindow(CefWidget):
    def __init__(self, name,  initial_width, parent=None):
        super(BrowserWindow, self).__init__(parent)
        self.initial_width = initial_width
        self.name = name
        self.viewport_label = QLabel()
        self._apply_widget_settings()

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
        return f'{self.name}  |  Viewport: {self.size().width()} px'
