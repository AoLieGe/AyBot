from aoe.data.locale import Locale


class AoeDataParser:
    def __init__(self, data):
        self._data = data
        self._base = self._data.base()  # get base data
        self._names = self._base['civ_names']  # extract {base civ name : civ locale name code}
        self._texts = self._base['civ_helptexts']  # extract {base civ name : civ locale description code}

    # return string contained list of all civilisations
    def all_civs(self):
        strings = self._data.strings()  # get actual strings
        return ''.join([v + '\n' for k, v in strings.items() if k in list(self._names.values())])

    # return information about civilisation
    #   name - civilisation name in supported locale
    def civ_info(self, name):
        strings = self._data.strings()
        base_name = self._base_civ_name(name)
        if not base_name:
            return

        text_code = self._texts[base_name]
        return strings[text_code].replace('<br>', '').replace('</br>', '')\
            .replace('<b>', '').replace('</b>', '')

    # return codes of available data (e.g. units) for civilisation
    #   name - civilisation name in supported locale
    def data_codes(self, name):
        base_name = self._base_civ_name(name)
        # TODO: check base_name
        civ_tree = self._base['techtrees'][base_name]

        return {
            'units': civ_tree['units'],
            'techs': civ_tree['techs']
        }

    # return civilisation data (e.g. units) in locale language
    def data_names(self, locale_code):
        old_locale = self._data.locale()  # save current locale
        self._data.set_locale(locale_code)  # set locale
        strings = self._data.strings()  # get strings for current locale

        result = {}
        for data_type in ['units', 'techs']:
            data = self._base['data'][data_type]
            # extract language id for each codes, use it to find locale data name in strings
            # and create new dic {code: locale_data_name}
            result[data_type] = {code: strings[str(info['LanguageNameId'])] for code, info in data.items()}

        self._data.set_locale(old_locale)  # set old locale
        return result

    # ===================helper methods====================

    # return code of civilisation
    #   name - civilisation name in supported locale
    def _civ_code(self, name):
        name = name[0].upper() + name[1:].lower()  # format name
        result = None  # init result label
        old_locale_code = self._data.locale()  # save old locale

        for locale_code in Locale().codes():
            self._data.set_locale(locale_code)  # set locale
            result = {v: k for k, v in self._data.strings().items()}.get(name)  # get code if exist
            if result:
                break

        self._data.set_locale(old_locale_code)  # set old locale
        return result

    # return base civ name (how it named in json data)
    #   name - civilisation name in supported locale
    def _base_civ_name(self, name):
        code = self._civ_code(name)  # locale_civ_codes[civ_name]
        if not code:
            return

        return {v: k for k, v in self._names.items()}[code]
