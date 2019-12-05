from cefpython3.cefpython_py37 import PyBrowser
from rx.core import typing
from rx.subject import Subject

from utils.config_parser import Profile


class AppState(object):

    def __init__(self):
        self._browser_holder: [PyBrowser] = []
        self._navigation_urlS: typing.Subject = Subject()
        self._update_y_position: typing.Subject = Subject()
        self.current_profileS: typing.Subject = Subject()

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

    def next_profile(self, profile: Profile):
        self.current_profileS.on_next(profile)

    def get_navigation_url_subscription(self) -> typing.Subject:
        return self._navigation_urlS

    def sync_browser_scroll(self, value):
        print('update scrolling of browser')
        for browser in self._browser_holder:
            browser.ExecuteFunction('py_scrollTo', value)
