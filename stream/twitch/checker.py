from discord.ext import tasks
from stream.twitch.api import TwitchApi


OFFLINE_DELAY = 5  # offline delay count (dropped task.loop cycles for check_stream fun)


class Checker:
    def __init__(self, twitch_id, twitch_secret, discord_client, sub_provider):
        self._twitch = TwitchApi(twitch_id, twitch_secret)
        self.provider = sub_provider
        self.client = discord_client

    @tasks.loop(seconds=60)
    async def check(self):
        print('=========Tick=========')
        subs = self.provider.subs
        for sub in subs.data:
            stream = self._twitch.get_streams(sub.name)
            print(f'{sub.name}: {stream}')

            if stream:
                if sub.status == subs.OFFLINE:
                    sub.status = subs.ONLINE
                    sub.offline_count = OFFLINE_DELAY
                    print(sub.guild)
                    channel = self.client.get_guild(sub.guild).get_channel(sub.channel)
                    title = stream['title']
                    everyone = '@everyone\n' if sub.everyone else ''
                    await channel.send(f'{everyone}{title}\n https://www.twitch.tv/{sub.name}')
            else:
                if sub.offline_count > 0:
                    sub.offline_count -= 1
                else:
                    sub.status = subs.OFFLINE
