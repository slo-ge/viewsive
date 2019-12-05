import yaml


class Tab(object):
    def __init__(self, name, url, width):
        print('load config:', name, url, width)
        self.name = name
        self.url = url
        self.width = int(width)


class Profile(object):
    def __init__(self, profile: str, tabs: [], **kwargs):
        self.tabs: [Tab] = []
        self.name = profile
        print('\n\nload profile:', profile)

        for tab in tabs:
            self.tabs.append(Tab(**tab))


class Profiles(object):
    def __init__(self, profiles: [Profile]):
        self.profiles = []

        for profile in profiles:
            self.profiles.append(Profile(**profile))


def load_config(file_path) -> Profiles:
    with open(file_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

        return Profiles(data['profiles'])


if __name__ == '__main__':
    load_config()
