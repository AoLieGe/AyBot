from commands.container import CmdContainer


class ModerateCmd(CmdContainer):
    def __init__(self):
        super().__init__()

        self.bans = ['хуйхуй']
        self.admin_id = 123

    def parse(self, message):
        msg = message.content.lower()
        user = message.author.id

        for banword in self.bans:
            if banword.lower() in msg:
                message.delete()
                print('deleted: ' + msg)
