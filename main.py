import os
import discord
from stream.sub.provider import SubscriptionProvider
from stream.twitch.checker import Checker
from stream.cmd import StreamCmd
from commands.parser import CmdParser
from aoe.cmd import AoeCmd
from stats.cmd import StatsCmd
from chat.forfun.cmd import ChatCmd
from chat.moderate.cmd import ModerateCmd
from db.provider import DBProvider


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # get discord token from
TWITCH_ID = os.getenv("TWITCH_ID")  # get twitch token from
TWITCH_SECRET = os.getenv("TWITCH_SECRET")  # get twitch secret from
DB_URL = os.getenv("DB_URL")

# temp solution
AYGUILD = int(os.getenv("AYGUILD"))
AYCHANNEL = int(os.getenv("AYCHANNEL"))
AYADMIN = int(os.getenv("AYADMIN"))

db = DBProvider(DB_URL)

discord_client = discord.Client()
sub_provider = SubscriptionProvider(db)

stream_checker = Checker(TWITCH_ID, TWITCH_SECRET, discord_client, sub_provider)

cmd = CmdParser()
cmd.add_parser(AoeCmd())
cmd.add_parser(StreamCmd(sub_provider))
cmd.add_parser(StatsCmd(db))
cmd.add_parser(ChatCmd())
cmd.add_parser(ModerateCmd(AYADMIN, AYGUILD))


@discord_client.event
async def on_ready():
    print('Logged on as {0}!'.format(discord_client.user))
    stream_checker.check.start()
    

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    if not message.content:
        return

    response = await cmd.parse(message)
    if response:
        await message.channel.send(response)


discord_client.run(DISCORD_TOKEN)
