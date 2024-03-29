from commands.container import CmdContainer


class ChatCmd(CmdContainer):
    def __init__(self):
        super().__init__()

        self._commands = {
            '/Лучший': (self.best_male, 0),
            '/Лучшая': (self.best_female, 0),
            '/лучший': (self.best_male, 0),
            '/лучшая': (self.best_female, 0),
            '/пнх': (self.nah, 0),
            '/best': (self.best_test, 0),
            '/zloy': (self.zloy, 0),
            '/франки': (self.franks, 0)
        }
        
    async def franks(self, params):
        return 'Чел, это мейнстрим, лучше сыграй ЦА'

    async def zloy(self, params):
        return 'Чую запах новой псины. Кажется, пора ливать'

    async def best_male(self, params):
        name = 'Boy'
        if params:
            name = params[0]
        await self.msg.delete()
        return f"{name}, ты лучший!"

    async def nah(self, param):
        if param:
            name = param[0]
        await self.msg.delete()
        return f"{name}, пнх, псина!"

    async def best_female(self, params):
        name = 'Детка'
        if params:
            name = params[0]
        await self.msg.delete()
        return f"{name}, ты лучшая!"

    async def best_test(self, params):
        name = 'Boy'
        if params:
            name = params[0]
        await self.msg.delete()
        return f"{name}, ты лучший!"


