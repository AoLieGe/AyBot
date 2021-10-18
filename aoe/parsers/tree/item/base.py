class BaseItem:
    @staticmethod
    def name(item, strings):
        return strings[item['LanguageNameId']]

    @staticmethod
    def help_text(item, strings):
        return strings[item['LanguageHelpId']]

    @staticmethod
    def cost(item):
        return ' '.join(f'{name[0]}: {cost}' for name, cost in item['Cost'].items())