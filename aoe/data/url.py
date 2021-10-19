class DataUrl:
    # get base aoe url
    @staticmethod
    def raw():
        return "https://aoe2techtree.net/data/data.json"

    # get locale strings url
    @staticmethod
    def strings(locale_code):
        return "https://aoe2techtree.net/data/locales/{0}/strings.json".format(locale_code)
