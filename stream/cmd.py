from commands.container import CmdContainer


class StreamCmd(CmdContainer):
    def __init__(self, sub_provider):
        super().__init__()
        self.provider = sub_provider

        self._commands = {
            '/sub': (self.sub, 1),
            '/unsub': (self.unsub, 1)
        }

    def sub(self, params):
        name = params[0]
        subs = self.provider.subs

        if subs.add(name, self.msg.guild.id, self.msg.channel.id, True if 'everyone' in params else False):
            print(self.msg.guild.id)
            print(self.msg.channel.id)
            self.provider.save()
            print('success')
        else:
            print('error')

    def unsub(self, params):
        name = params[0]
        subs = self.provider.subs

        if subs.delete(name, self.msg.guild.id):
            self.provider.save()
            print('success')
        else:
            print('error')
