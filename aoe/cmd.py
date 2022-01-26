from commands.container import CmdContainer

from aoe.data.locale import Locale
from aoe.data.raw import RawData
from aoe.data.tree import TreeView

from aoe.parsers.civ.info import CivInfo
from aoe.parsers.civ.tree import CivTree
from aoe.parsers.tree.item import TreeItem
from aoe.parsers.tree.view import TreeViewParser
from aoe.data.voice import VoiceCommands


class AoeCmd(CmdContainer):
    def __init__(self):
        super().__init__()
        self.raw = RawData()
        self.civ_info = CivInfo(self.raw)               # gives base civ information
        self.civ_tree = CivTree(self.raw)               # gives tree item codes and locale texts for civ
        self.tree_item = TreeItem(self.raw)             # gives info about every items in tree
        self.tree_view = TreeViewParser(TreeView())     # gives tree view for each civ
        self.voice = VoiceCommands()                    # gives info for game voice commands

        self._commands = {
            '/инфо': (self.info, 1),
            '/цивы': (self.civ_list, 0),
            '/языки': (self.locales, 0),
            '/язык': (self.set_locale, 1),
            '/чат': (self.voice_cmd, 1)
            }

        self.tree_view_cmd = {
            'пехота': self.tree_view.barrack,
            'кони': self.tree_view.stable,
            'луки': self.tree_view.archery,
            'осадка': self.tree_view.siege,
            'монастырь': self.tree_view.monastery,
            'док': self.tree_view.dock
        }

    def info(self, params):
        civ_name = self._find_civ_name(params)
        tree_view = self._find_tree_view(params)
        locale = self._find_locale_code(params)
        info = ''

        if not locale:
            locale = self.raw.locale

        if civ_name:
            if not tree_view:
                # if command contain only civ name - return information about civ
                info = self.civ_info.get(civ_name, locale)
            else:
                # if command contain civ tree cmd - return tree view for civ
                codes = self.civ_tree.codes(civ_name)
                texts = self.civ_tree.texts(locale)
                info = self.tree_view_cmd[tree_view](codes, texts)
        else:
            # if cmd not contain civ, check that it contain tree item
            if locale in params:
                params.remove(locale)
                name = ' '.join(params)
            else:
                name = ' '.join(params)

            info = self.tree_item.info(name, locale)
        return info

    def voice_cmd(self, params):
        return self.voice.data.get(params[0])

    # get all civilisations
    async def civ_list(self, params):
        locale = self._find_locale_code(params)
        if not locale:
            locale = self.raw.locale
        return '\n'.join(self.civ_info.list(locale))

    # get locales listing
    def locales(self, params):
        names = Locale().names()
        code = Locale().code

        return ''.join(["{0} - {1}\n".format(name, code(name)) for name in names])

    # set default locale for answers
    def set_locale(self, params):
        locale_code = Locale().code(params[0])
        self.raw.set_locale(locale_code)

# ===================helper methods====================
    def _find_civ_name(self, params):
        for locale in Locale().codes():
            civ_list = self.civ_info.list(locale)
            for param in params:
                if param.capitalize() in civ_list:
                    return param

    # return first civ aoe commands found in params or None if not
    def _find_tree_view(self, params):
        for param in params:
            if param.lower() in self.tree_view_cmd:
                return param.lower()

    # return first locale code found in params list or None if not
    def _find_locale_code(self, params):
        for param in params:
            if param.lower() in Locale().codes():
                return param.lower()



