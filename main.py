import os
import discord
from stream.sub.list import SubscriptionList
from stream.sub.provider import SubscriptionProvider
from stream.twitch.checker import Checker
from stream.cmd import StreamCmd
from commands.parser import CmdParser
from aoe.cmd import AoeCmd


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # get discord token from
TWITCH_ID = os.getenv("TWITCH_ID")  # get twitch token from
TWITCH_SECRET = os.getenv("TWITCH_SECRET")  # get twitch secret from

# temp solution
AYGUILD = os.getenv("AYGUILD")
AYCHANNEL = os.getenv("AYCHANNEL")


discord_client = discord.Client()
subs = SubscriptionList()
sub_provider = SubscriptionProvider(subs)
sub_provider.load()

subs.add('heyayvaz', AYGUILD, AYCHANNEL, True)  #temp solution

stream_checker = Checker(TWITCH_ID, TWITCH_SECRET, sub_provider)

cmd = CmdParser()
cmd.add_parser(AoeCmd())
cmd.add_parser(StreamCmd(sub_provider))


@discord_client.event
async def on_ready():
    print('Logged on as {0}!'.format(discord_client.user))
    stream_checker.check.start(discord_client)


@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    if not message.content:
        return

    response = cmd.parse(message)
    if response:
        await message.channel.send(response)


discord_client.run(DISCORD_TOKEN)
