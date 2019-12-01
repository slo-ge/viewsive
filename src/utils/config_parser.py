import yaml


class Tab(object):
    def __init__(self, name, url, width):
        print('load config', name, url, width)
        self.name = name
        self.url = url
        self.width = int(width)


class TabConfig:
    def __init__(self, tabs: []):
        self.tabs: [Tab] = []

        for tab in tabs:
            self.tabs.append(Tab(**tab))


def load_config(file_path):
    with open(file_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return TabConfig(data['profile-1']['tabs'])


if __name__ == '__main__':
    load_config()
