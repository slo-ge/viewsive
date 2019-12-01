from PyQt5.QtWidgets import QFrame, QGridLayout, QLineEdit

from utils.qt import create_button
from widgets.config import FALLBACK_URL, app_state


class NavigationBar(QFrame):
    def __init__(self):
        super(NavigationBar, self).__init__()
        # self.cef_widget = cef_widget[0]

        # Init layout
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Back button
        self.back = create_button("back")
        self.back.clicked.connect(self.on_back)
        layout.addWidget(self.back, 0, 0)

        # Forward button
        self.forward = create_button("forward")
        self.forward.clicked.connect(self.on_forward)
        layout.addWidget(self.forward, 0, 1)

        # Reload button
        self.reload = create_button("reload")
        self.reload.clicked.connect(self.on_reload)
        layout.addWidget(self.reload, 0, 2)

        # Url input
        self.url = QLineEdit("")
        self.url.returnPressed.connect(self.on_go_url)
        layout.addWidget(self.url, 0, 3)

        # Layout
        self.setLayout(layout)
        self.update_state()
        self.init_config()

    def init_config(self):
        self.url.setText(FALLBACK_URL)

    def on_back(self):
        pass
        # if self.cef_widget.browser:
        #    self.cef_widget.browser.GoBack()

    def on_forward(self):
        pass
        # if self.cef_widget.browser:
        #    self.cef_widget.browser.GoForward()

    def on_reload(self):
        pass
        # if self.cef_widget.browser:
        #    self.cef_widget.browser.Reload()

    def on_go_url(self):
        # just push the next url into navigation state
        app_state.next_navigation_url(self.url.text())

    def update_state(self):
        # browser = self.cef_widget.browser

        # if not browser:
        #    self.back.setEnabled(False)
        #    self.forward.setEnabled(False)
        #    self.reload.setEnabled(False)
        #    self.url.setEnabled(False)
        #    return

        # TODO
        # self.back.setEnabled(browser.CanGoBack())
        # self.forward.setEnabled(browser.CanGoForward())
        self.reload.setEnabled(True)
        self.url.setEnabled(True)

        # TODO: set text of textbox
        # self.url.setText(browser.GetUrl())
