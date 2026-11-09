class Conflict(Exception):
    pass


class Drafts:
    def __init__(self):
        self.values = {}

    def read(self, name):
        return self.values.get(name, {'text': '', 'version': 0}).copy()

    def write(self, name, text, version):
        if len(text.encode('utf-8')) > 65536:
            raise ValueError('draft is too large')
        current = self.read(name)
        if version != current['version']:
            raise Conflict(current['version'])
        result = {'text': text, 'version': version + 1}
        self.values[name] = result
        return result.copy()
