class AoeUrl:
    # get website url
    @staticmethod
    def site():
        return "https://aoe2techtree.net"

    # get base aoe url
    @staticmethod
    def base():
        return "https://aoe2techtree.net/data/data.json"

    # get locale strings url
    @staticmethod
    def strings(locale_code):
        return "https://aoe2techtree.net/data/locales/{0}/strings.json".format(locale_code)
