from aoe.parsers.tree.item.base import BaseItem


class UnitItem(BaseItem):
    @staticmethod
    def parse(item):
        pass

    @staticmethod
    def base_stats(item):
        pass


    @staticmethod
    def stats(item):
        keys = ['HP', 'Attack', 'MeleeArmor', 'PierceArmor', 'Range',
                'LineOfSight', 'Speed', 'TrainTime', 'FrameDelay', 'ReloadTime']

        return ' ,'.join([f'{k}: {v}' for k, v in item if k in keys])
