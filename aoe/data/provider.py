import requests
from aoe.data.locale import Locale
from aoe.data.url import AoeUrl


class AoeData:
    _base = None  # base aoe in json format
    _strings = None  # strings in selected locale
    _locale_code = None  # current strings locale

    def __init__(self):
        url = AoeUrl.base()
        # TODO: can throw connection exception, need to catch...
        self._base = requests.get(url).json()  # read base aoe json
        self._locale_code = Locale().default_code()  # get default locale code
        self.set_locale(self._locale_code)

    # get base aoe json
    def base(self):
        return self._base

    # get locale strings json
    def strings(self):
        return self._strings

    # get current strings locale code
    def locale_code(self):
        return self._locale_code

    # set locale for strings
    def set_locale(self, code):
        # TODO: need to check 'code' parameter before set
        self._locale_code = code
        url = AoeUrl.strings(code)
        # TODO: can throw connection exception, need to catch...
        self._strings = requests.get(url).json()  # read locale strings json for selected locale
