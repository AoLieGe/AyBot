from commands.container import CmdContainer


class ModerateCmd(CmdContainer):
    def __init__(self, admin_id, guild_id):
        super().__init__()

        self.admin = admin_id
        self.guild = guild_id

        self.bans = ['удоли']

    async def parse(self, message):
        msg = message.content.lower()
        user = message.author.id

        print(msg + user)

        for banword in self.bans:
            if banword.lower() in msg:
                await message.delete()
                print('deleted: ' + msg)
