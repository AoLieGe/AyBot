from discord.ext import tasks
from stream.twitch.api import TwitchApi
from stream.sub.data import SubscriptionData

OFFLINE_DELAY = 5  # offline delay count (dropped task.loop cycles for check_stream fun)


class Checker:
    def __init__(self, twitch_id, twitch_secret, discord_client, sub_provider):
        self._twitch = TwitchApi(twitch_id, twitch_secret)
        self.provider = sub_provider
        self.client = discord_client

    @tasks.loop(seconds=60)
    async def check(self):
        print('=========Tick=========')
        subs = self.provider.load()
        for sub in subs:
            stream = self._twitch.get_streams(sub.name)

            if stream:
                sub.offline_count = OFFLINE_DELAY
                if sub.status == SubscriptionData.OFFLINE:
                    sub.status = SubscriptionData.ONLINE
                    channel = self.client.get_guild(sub.guild).get_channel(sub.channel)
                    title = stream['title']
                    everyone = '@everyone\n' if sub.everyone else ''
                    await channel.send(f'{everyone}{title}\n https://www.twitch.tv/{sub.name}')
            else:
                if sub.offline_count > 0:
                    sub.offline_count -= 1
                else:
                    sub.status = SubscriptionData.OFFLINE

            self.provider.update(sub)
            print(f'{sub.name}: {stream} \t online={sub.status} offline_count={sub.offline_count}')
