from cefpython3.cefpython_py37 import PyBrowser


class AppState(object):

    def __init__(self):
        self._browser_holder: [PyBrowser] = []

    def append_browser(self, browser: PyBrowser):
        self._browser_holder.append(browser)

    def update_url(self, url):
        if not self._browser_holder:
            raise AssertionError('Browser holder is empty, can not update browser urls')

        browser: PyBrowser
        for browser in self._browser_holder:
            if browser.GetUrl() != url:
                browser.LoadUrl(url)
