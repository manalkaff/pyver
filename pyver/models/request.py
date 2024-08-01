



class Request:

    def __init__(self, params, data):
        self._params = params
        self._data = data


    @property
    def params(self):
        return self._params

    @property
    def data(self):
        return self._data