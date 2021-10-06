class SubscriptionData:
    def __init__(self, name, guild, channel, everyone):
        self.name = name
        self.guild = guild
        self.channel = channel
        self.everyone = everyone
        self.status = False
        self.offline_count = 0

    def __str__(self):
        return f'{self.name}, {self.guild}, {self.channel}, {self.status}, {self.everyone}'
