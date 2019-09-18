from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFrame, QHBoxLayout, QVBoxLayout

from widgets.browserwidget import BrowserWindow
from widgets.config import ViewPortSize, app_state
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
        self.browser_windows.append(BrowserWindow('Phone', ViewPortSize.MOBILE, parent=self))
        self.browser_windows.append(BrowserWindow('Tablet', ViewPortSize.TABLET, parent=self))
        self.browser_windows.append(BrowserWindow('Desktop', ViewPortSize.DESKTOP, parent=self))

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
        self.show()

        # Browser can be embedded only after layout was set up
        # NOTE: this is important to show the browser window
        for browser_window in self.browser_windows:
            browser_window.embedBrowser()

            app_state.append_browser(browser_window.browser)

    def closeEvent(self, event):
        # Close browser (force=True) and free CEF reference
        for browser_window in self.browser_windows:
            browser_window.embedBrowser()

            if browser_window.browser:
                browser_window.browser.CloseBrowser(True)
                self.clear_browser_references()

    def clear_browser_references(self):
        self.browser_windows = []
