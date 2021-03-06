from cefpython3.cefpython_py37 import PyBrowser
from rx.core import typing
from rx.subject import Subject


class AppState(object):

    def __init__(self):
        self._browser_holder: [PyBrowser] = []
        self._navigation_urlS: typing.Subject = Subject()
        self._navigation_bar = None

    def append_browser(self, browser: PyBrowser):
        self._browser_holder.append(browser)

    def append_navigation(self, navigation):
        self._navigation_bar = navigation

    def update_url(self, url):
        if not self._browser_holder:
            raise AssertionError('Browser holder is empty, can not update browser urls')

        # update all browsers
        browser: PyBrowser
        for browser in self._browser_holder:
            if browser.GetUrl() != url:
                browser.LoadUrl(url)

        # update url of navigation bar
        self._navigation_bar.url.setText(url)

    def next_navigation_url(self, url: str):
        self._navigation_urlS.on_next(url)

    def get_navigation_url_subscription(self) -> typing.Subject:
        return self._navigation_urlS
