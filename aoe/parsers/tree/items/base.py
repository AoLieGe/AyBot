class BaseItem:
    @staticmethod
    def name(item, strings):
        return strings[item['LanguageNameId']]

    @staticmethod
    def help_text(item, strings):
        raw = strings['{}'.format(item['LanguageHelpId'])]
        b = raw.replace('<b>', '').replace('</b>', '')
        br = b.replace('<br>', '')
        i = br.replace('<i>', '').replace('</i>', '')
        stats = i.replace('‹hp› ‹attack› ‹armor› ‹piercearmor› ‹range›', '')
        return stats

    @staticmethod
    def cost(item):
        order = ['Wood', 'Food', 'Gold', 'Stone']
        cost = item['Cost']

        return ' '.join('{0}{1}'.format(cost[res], res[0]) for res in order if res in cost.keys())

