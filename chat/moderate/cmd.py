from commands.container import CmdContainer


class ModerateCmd(CmdContainer):
    def __init__(self, admin_id, guild_id):
        super().__init__()

        self.admin = admin_id
        self.guild = guild_id

        self.bans = ['www.twitch.tv']

    async def parse(self, message):
        msg = message.content.lower()
        user = message.author.id
        guild = message.guild.id
        channel = message.channel.id

        if guild != self.guild:
            return
        
        if channel == 822903067233878016:
            return

        if user == self.admin:
            return

        for banword in self.bans:
            if banword.lower() in msg:
                await message.delete()
                print('deleted: ' + msg)
