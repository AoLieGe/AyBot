from aoe.parsers.civ.base import BaseCiv


class CivInfo(BaseCiv):
    def __init__(self, raw):
        super.__init__(raw)

    # return string that contain list of all civilisations
    def list(self, locale):
        old_locale = self.raw.locale
        self.raw.set_locale(locale)
        res = ''.join([v + '\n' for k, v in self.str.items() if k in list(self.names.values())])

        self.raw.set_locale(old_locale)
        return res

    # return information about civilisation
    #   name - civilisation name in supported locale
    def info(self, name):
        raw_name = self._raw_name(name)
        if not raw_name:
            return

        desc_code = self.civ_desc[raw_name]
        desc = self.raw.strings[desc_code]
        formatted = desc.replace('<br>', '').replace('</br>', '')\
            .replace('<b>', '').replace('</b>', '')
        return formatted



