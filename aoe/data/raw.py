import requests
from aoe.data.locale import Locale
from aoe.data.url import DataUrl


class RawData:
    def __init__(self):
        url = DataUrl.raw()
        # TODO: can throw connection exception, need to catch...
        self.base = requests.get(url).json()  # read base aoe json
        self.strings = {}
        self.locale = Locale().default  # get default locale code
        self.set_locale(self.locale)

    # set locale for strings
    def set_locale(self, code):
        if code not in Locale().codes():
            return False

        self.locale = code
        url = DataUrl.strings(code)
        # TODO: can throw connection exception, need to catch...
        self.strings = requests.get(url).json()  # read locale strings json for selected locale
        return True
