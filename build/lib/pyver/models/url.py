

from ..constants.methods import GET, POST


class Urls:

    def __init__(self):
        self.urls = {}

    def add_url(self, url, function, method):
        self.urls[url] = {
            "url": url,
            "function":function,
            "method": method
        }

    def get(self, url, function):
        self.add_url(url, function, GET)

    def post(self, url, function):
        self.add_url(url, function, POST)

    
    def find(self, method, path):
        try:
            path = path.split("?")[0]
            url = self.urls[path]
            if url != None and url['method'] == method:
                return url['function']
            return None
        except:
            return None
