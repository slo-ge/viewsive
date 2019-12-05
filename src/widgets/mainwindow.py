from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFrame, QHBoxLayout, QVBoxLayout, QTabWidget

from utils.config_parser import load_config, Profile
from widgets.browserwidget import BrowserWindow
from widgets.config import app_state, config_file
from widgets.navigationbar import NavigationBar
from widgets.profileselector import ProfileSelector


class MainWindow(QMainWindow):
    """ defines the layout and append ui element including the cef widget"""

    def __init__(self):
        super(MainWindow, self).__init__(None)
        self.setWindowTitle("Yeeeyss")
        self.setFocusPolicy(Qt.StrongFocus)
        self.browser_windows: [BrowserWindow] = []
        self.profile = load_config(config_file)
        self.tabs = QTabWidget()
        app_state.current_profileS.subscribe(self.get_tabs)  # $

        self.setup_tab_layout()

    def setup_tab_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(ProfileSelector(self.profile))
        layout.addWidget(self.tabs)
        frame = QFrame()
        frame.setLayout(layout)
        self.setCentralWidget(frame)
        self.show()

    def get_tabs(self, profile: Profile):
        print(profile, profile.name, profile.tabs)
        for tab in profile.tabs:
            print(tab.name, tab.width, tab.url)
            window = BrowserWindow(tab.name, tab.width, tab.url, parent=self)
            self.embed_view(window)
            window.setFixedSize(window.sizeHint())
            window.setFixedSize(window.sizeHint())
            self.tabs.addTab(window, tab.name)

    def setup_default_layout(self):
        # TODO: embed_view to render browser
        navigation_bar = NavigationBar()
        layout = QVBoxLayout()
        layout.addWidget(navigation_bar)
        hbox = QHBoxLayout()

        browser_window: BrowserWindow
        for browser_window in self.browser_windows:
            vbox = QVBoxLayout()
            vbox.addWidget(browser_window.viewport_label)
            vbox.addWidget(browser_window)
            hbox.addLayout(vbox)

        layout.addLayout(hbox)
        frame = QFrame()
        frame.setLayout(layout)
        self.setCentralWidget(frame)
        self.show()
        app_state.append_navigation(navigation_bar)

    def embed_view(self, window):
        window.embedBrowser()
        app_state.append_browser(window.browser)

    def closeEvent(self, event):
        # Close browser (force=True) and free CEF reference
        for browser_window in self.browser_windows:
            browser_window.embedBrowser()

            if browser_window.browser:
                browser_window.browser.CloseBrowser(True)
                self.clear_browser_references()

    def clear_browser_references(self):
        self.browser_windows = []
