from aoe.parsers.tree.items.base import BaseItem


class TechItem(BaseItem):
    @staticmethod
    def info(item, strings):
        desc = TechItem.desc(item, strings)
        desc = desc.replace('‹cost›', TechItem.cost(item))
        return desc
