from aoe.parsers.civ.base import BaseCiv


class CivTree(BaseCiv):
    def __init__(self, raw):
        super().__init__(raw)
        self.tree_roots = ['units', 'techs']

    # return codes of available data (e.g. units) for civilisation
    #   name - civilisation name in supported locale
    def codes(self, name):
        raw_name = self._raw_name(name)
        if not raw_name:
            return

        tree = self.raw.base['techtrees'][raw_name]

        return {root: data for root, data in tree.items() if root in self.tree_roots}

    #
    def texts(self, locale):
        old_locale = self.raw.locale
        self.raw.set_locale(locale)
        strings = self.raw.strings

        res = {}
        for root in self.tree_roots:
            root_items = self.raw.base['data'][root].items()
            res[root] = {code: strings[str(data['LanguageNameId'])] for code, data in root_items}

        self.raw.set_locale(old_locale)
        return res
