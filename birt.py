import requests


class BirtConnection(object):

    def __init__(self, url):
        self.url = "%s/run" % url

    def __call__(self, name, format, params):
        settings = { "__report": name,
                     "__format": format}
        settings.update(params)
        r = requests.get(self.url, params=settings)
        return (r.content, format)
