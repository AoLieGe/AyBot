from commands.container import CmdContainer
from aoe.data.locale import Locale
from aoe.data.provider import AoeData
from aoe.data.tree import AoeTree
from aoe.parsers.data import AoeDataParser
from aoe.parsers.tree import AoeTreeParser
from aoe.data.voice import VoiceCommands


class AoeCmd(CmdContainer):
    def __init__(self):
        super().__init__()
        self._data = AoeData()
        self._data_parser = AoeDataParser(self._data)
        self._tree = AoeTree()
        self._tree_parser = AoeTreeParser(self._tree)
        self._voice = VoiceCommands()

        self._commands = {
            '/инфо': (self.civ_info, 1),
            '/цивы': (self.civ_list, 0),
            '/языки': (self.locales, 0),
            '/язык': (self.set_locale, 1),
            '/чат': (self.voice_cmd, 1)
            }

        self._civ_sub_cmd = {
            'пехота': self._tree_parser.get_infantry,
            'кони': self._tree_parser.get_stable,
            'луки': self._tree_parser.get_archers,
            'осадка': self._tree_parser.get_siege,
            'монастырь': self._tree_parser.get_monastery,
            'док': self._tree_parser.get_dock
        }

    def civ_info(self, params):
        old_locale = self._data.locale_code()  # save old locale
        locale_code = self._find_locale_code(params)  # find locale code in params (it's optionally parameter)
        data_param = self._find_data_cmd(params)  # find civ aoe command (it's optionally parameter)

        if locale_code:  # set new locale if it found in params
            if locale_code != old_locale:
                self._data.set_locale(locale_code)
        else:
            locale_code = old_locale

        info = None
        civ_name = params[0]  # civ name
        if data_param:
            data_codes = self._data_parser.data_codes(civ_name)
            data_names = self._data_parser.data_names(locale_code)
            info = self._civ_sub_cmd[data_param](data_codes, data_names)
        else:
            info = self._data_parser.civ_info(civ_name)

        self._data.set_locale(old_locale)  # set old locale
        return info

    def voice_cmd(self, params):
        cmd = params[0]
        print(cmd)
        res = self._voice.data.get(cmd)
        print(res)
        return res

    # get all civilisations
    def civ_list(self, params):
        return self._data_parser.all_civs()

    # get locales listing
    def locales(self, params):
        names = Locale().names()
        code = Locale().code

        return ''.join(["{0} - {1}\n".format(name, code(name)) for name in names])

    # set default locale for answers
    def set_locale(self, params):
        locale_code = Locale().code(params[0])
        self._data.set_locale(locale_code)

# ===================helper methods====================

    # return first locale code found in params list or None if not
    def _find_locale_code(self, params):
        for param in params:
            if Locale().name(param):
                return param

            code = Locale().code(param)
            if code:
                return code
        return

    # return first civ aoe commands found in params or None if not
    def _find_data_cmd(self, params):
        for param in params:
            if param.lower() in self._civ_sub_cmd:
                return param.lower()
        return
