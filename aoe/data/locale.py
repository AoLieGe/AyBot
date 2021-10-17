from misc.singleton import Singleton


# singleton class Locale collect all locales used in bot
class Locale(metaclass=Singleton):  # can be singleton?
    def __init__(self):
        self._data = {
            'Русский': 'ru',
            'English': 'en'
        }
        self._default = list(self._data.values())[0]

    # get locale names list
    def names(self):
        return list(self._data)

    # get locale codes list
    def codes(self):
        return list(self._data.values())

    # get code by name otherwise return None
    def code(self, name):
        name = name[0].upper() + name[1:].lower()  # format name before
        return self._data.get(name)

    # get name by code otherwise return None
    def name(self, code):
        return {v: k for k, v in self._data.items()}.get(code.lower())

    # get default locale code
    def default_code(self):
        return self._default
