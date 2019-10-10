class JavaScriptBindingParser(object):
    """ Parses the given javascript from file path
    and also helps us to have a nicer way to check if javascript funcitons
    are available


    """
    def __init__(self):
        self.source = None

    def from_file(self, path: str):
        with open(path, 'r') as file:
            self.source = file.read()
        return self.source

    @property
    def js_init(self):
        return self.lookup('jsInit')

    def lookup(self, fun_name: str) -> str:
        if fun_name in self.source:
            return fun_name

        exception = 'function name does not exists in JS file: {}'
        raise Exception(exception.format(fun_name))
