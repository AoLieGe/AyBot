from db.api.sub import SubApi
from stream.sub.data import SubscriptionData


class SubscriptionProvider:
    def __init__(self, db):
        self.db = db
        self.db.execute(SubApi.create_table())

    def add(self, sub):
        self.db.execute(SubApi.add_sub(sub.name,
                                       sub.guild,
                                       sub.channel,
                                       sub.everyone,
                                       sub.status,
                                       sub.offline_count))

    def delete(self, sub_name, sub_guild):
        self.db.execute(SubApi.del_sub(sub_name, sub_guild))

    def update(self, sub):
        self.db.execute(SubApi.update_sub(sub.name,
                                          sub.guild,
                                          sub.channel,
                                          sub.everyone,
                                          sub.status,
                                          sub.offline_count))

    def load(self):
        subs_data = self.db.fetchall(SubApi.get_subs())
        subs_list = []

        for sub_data in subs_data:
            _, name, guild, channel, everyone, status, count = sub_data
            subs_list.append(SubscriptionData(name, guild, channel, everyone, status, count))

        return subs_list
