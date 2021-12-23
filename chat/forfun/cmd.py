from commands.container import CmdContainer


class ChatCmd(CmdContainer):
    def __init__(self):
        super().__init__()

        self._commands = {
            '/Лучший': (self.best_male, 0),
            '/Лучшая': (self.best_female, 0),
            '/лучший': (self.best_male, 0),
            '/лучшая': (self.best_female, 0),
            '/best': (self.best_test, 0),
            '/zloy': (self.zloy, 0)
        }

    def zloy(self, params):
        return 'Чую запах новой псины. Кажется, пора ливать'

    def best_male(self, params):
        name = 'Boy'
        if params:
            name = params[0]

        return f"{name}, ты лучший!"

    def best_female(self, params):
        name = 'Детка'
        if params:
            name = params[0]

        return f"{name}, ты лучшая!"

    def best_test(self, params):
        name = 'Boy'
        if params:
            name = params[0]

        return f"{name}, ты лучший!"


