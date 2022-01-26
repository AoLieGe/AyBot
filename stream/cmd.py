from commands.container import CmdContainer
from stream.sub.data import SubscriptionData


class StreamCmd(CmdContainer):
    def __init__(self, sub_provider):
        super().__init__()
        self.provider = sub_provider

        self._commands = {
            '/sub': (self.sub, 1),
            '/unsub': (self.unsub, 1)  # ,'/subs': (self.subs, 0)
        }

    async def subs(self, params):
        return [sub.__str__() for sub in self.provider.load()]

    async def sub(self, params):
        name = params[0]
        sub = SubscriptionData(name, self.msg.guild.id, self.msg.channel.id, True if 'everyone' in params else False)
        self.provider.add(sub)

    async def unsub(self, params):
        name = params[0]
        guild = self.msg.guild.id
        self.provider.delete(name, guild)
