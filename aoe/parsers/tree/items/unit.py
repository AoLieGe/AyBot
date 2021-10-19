from aoe.parsers.tree.items.base import BaseItem


class UnitItem(BaseItem):
    @staticmethod
    def info(item, strings):
        desc = UnitItem.desc(item, strings)
        desc = desc.replace('‹cost›', UnitItem.cost(item))
        stats = UnitItem.stats(item)
        return f'{desc}{stats}'

    @staticmethod
    def stats(item):
        keys = ['HP', 'Attack', 'MeleeArmor', 'PierceArmor', 'Range',
                'LineOfSight', 'Speed', 'TrainTime', 'FrameDelay', 'ReloadTime']

        return ', '.join([f'{k}: {v}' for k, v in item.items() if k in keys])
