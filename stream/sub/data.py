class SubscriptionData:
    ONLINE = True
    OFFLINE = False

    def __init__(self, name, guild, channel, everyone, status=False, count=0):
        self.name = name
        self.guild = guild
        self.channel = channel
        self.everyone = everyone
        self.status = status
        self.offline_count = count

    def __str__(self):
        return f'{self.name}, {self.guild}, {self.channel}, {self.everyone}, {self.status}, {self.offline_count}'
