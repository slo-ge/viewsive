from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QFrame, QHBoxLayout, QVBoxLayout, QWidget, QSizePolicy

from widgets.cefwidget import CefWidget
from widgets.config import WIDTH, HEIGHT, WINDOWS
from widgets.navigationbar import NavigationBar


class MainWindow(QMainWindow):
    """ defines the layout and append ui element including the cef widget"""

    def __init__(self):
        super(MainWindow, self).__init__(None)
        # Avoids crash when shutting down CEF (issue #360)
        self.browser_windows: [QWidget] = []

        self.navigation_bar = None
        self.setWindowTitle("PyQt5 example")
        self.setFocusPolicy(Qt.StrongFocus)
        self.setup_layout()

    def setup_layout(self):
        # self.resize(WIDTH, HEIGHT)
        self.browser_windows.append(BrowserWindow(320, parent=self))
        self.browser_windows.append(BrowserWindow(568, parent=self))
        self.browser_windows.append(BrowserWindow(1024, parent=self))

        # append just the first window
        self.navigation_bar = NavigationBar(self.browser_windows)

        layout = QVBoxLayout()
        layout.addWidget(self.navigation_bar)
        hbox = QHBoxLayout()

        for browser_window in self.browser_windows:
            hbox.addWidget(browser_window)

        layout.addLayout(hbox)

        #layout.setContentsMargins(0, 0, 0, 0)
        #layout.setSpacing(0)

        #layout.setRowStretch(0, 0)
        #layout.setRowStretch(1, 2)
        #layout.setRowStretch(2, 3)
        #layout.setRowStretch(3, 3)

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
    def __init__(self, initial_width, parent=None):
        super(BrowserWindow, self).__init__(parent)
        self.initial_width = initial_width

    def sizeHint(self):
        return QSize(self.initial_width, 1000)
