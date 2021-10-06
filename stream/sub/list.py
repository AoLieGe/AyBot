from stream.sub.data import SubscriptionData


class SubscriptionList:
    def __init__(self):
        self.ONLINE = True
        self.OFFLINE = False
        self.data = []

    def add(self, name, guild, channel, everyone):
        for user in self.data:
            if user.name == name and user.guild == guild:
                return False
        user = SubscriptionData(name, guild, channel, everyone)
        self.data.append(user)
        return True

    def delete(self, name, guild):
        for user in self.data:
            if user.name == name and user.guild == guild:
                self.data.remove(user)
                return True
        return False

    def __str__(self):
        return '\n'.join([str(user) for user in self.data])
