from aoe.data.locale import Locale


class BaseCiv:
    def __init__(self, raw):
        self.raw = raw
        self.str = raw.strings
        self.names = self.raw.base['civ_names']
        self.civ_desc = self.raw.base['civ_helptexts']

    # find <name> in locales and return how it named in raw json
    def _raw_name(self, name):
        old_locale = self.raw.locale
        raw_name = None

        for locale in Locale().codes():
            self.raw.set_locale(locale)
            code = {v: k for k, v in self.raw.strings.items()}.get(name.capitalize())  # get code if exist
            if code:
                raw_name = {v: k for k, v in self.names.items()}.get(code)
                break

        self.raw.set_locale(old_locale)
        return raw_name
