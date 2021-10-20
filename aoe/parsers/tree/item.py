from aoe.data.locale import Locale
from aoe.parsers.tree.items.unit import UnitItem
from aoe.parsers.tree.items.tech import TechItem


class TreeItem:
    def __init__(self, raw):
        self.raw = raw
        self.parsers = {
            'units': UnitItem.info,
            'techs': TechItem.info
        }

    # get info about <name> techtree item and show result in <locale> language
    def info(self, name, locale):
        lang_id = self._get_lang_id(name)
        if lang_id:
            # get group and item code
            item_code = self._get_item_code(lang_id)
            if item_code:
                group = item_code['group']
                code = item_code['code']
                # get item
                item = self.raw.base['data'][group][code]
                # save old locale and set required
                old_locale = self.raw.locale
                self.raw.set_locale(locale)
                # parse by item group parser
                res = self.parsers[group](item, self.raw.strings)
                # return old locale
                self.raw.set_locale(old_locale)
                return res

    # find item in raw data and return it group name and item code
    def _get_item_code(self, lang_id):
        for group, data in self.raw.base['data'].items():
            for code, item in data.items():
                if lang_id == str(item['LanguageNameId']):
                    return {'group': group, 'code': code}

    # check name in all locales and return it language code
    def _get_lang_id(self, name):
        # save locale
        old_locale = self.raw.locale
        found = {}

        # find item name in all locales
        for locale in Locale().codes():
            self.raw.set_locale(locale)
            for code, string in self.raw.strings.items():
                if name.lower() in string.lower():
                    found[code] = string

            if found:
                break

        self.raw.set_locale(old_locale)

        #sort res to find shortest value
        sorted_values = sorted(found.values(), key=len)
        if sorted_values:
            res_value = sorted_values[0]
            #find code of shortest value
            for code, value in found.items():
                if value == res_value:
                    return code

        #res = {k: v for k, v in sorted(res.items(), key=lambda item: item[1])}
        #res = list(res.keys())[0]

