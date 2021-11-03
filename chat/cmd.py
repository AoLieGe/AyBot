from commands.container import CmdContainer


class ChatCmd(CmdContainer):
    def __init__(self):
        super().__init__()

        self._commands = {
            '/Лучший': (self.best_male, 0),
            '/Лучшая': (self.best_female, 0)
        }

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




