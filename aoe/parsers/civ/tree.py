


self.tree_roots = ['units', 'techs']

# return codes of available data (e.g. units) for civilisation
    #   name - civilisation name in supported locale
    def tree_codes(self, name):
        raw_name = self._raw_name(name)
        if not raw_name:
            return

        tree = self.raw.base['techtrees'][raw_name]

        return {root: data for root, data in tree if root in self.tree_roots}

    #
    def tree_texts(self, locale):
        old_locale = self.raw.locale
        self.raw.set_locale(locale)
        strings = self.raw.strings

        res = {}
        for root in self.tree_roots:
            root_items = self.raw.base['data'][root].items()
            res[root] = {code: strings[str(data['LanguageNameId'])] for code, data in root_items}

        self.raw.set_locale(old_locale)
        return res
