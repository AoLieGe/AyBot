handler_id = 0  # constant means id number of Handler function in tuple in commands dictionary
params_id = 1  # constant means id number of additional parameters in tuple in commands dictionary


class CmdContainer:
    def __init__(self):
        self._commands = {}
        self.msg = None

    def commands(self):
        return self._commands.keys()

    # method read commands and execute helper method for it
    def parse(self, message):
        self.msg = message
        split = message.content.split() #.lower()

        try:
            cmd = split[0]
            params = split[1:]
        except IndexError:
            return

        res = None
        if cmd in self._commands:
            param_number = self._commands[cmd][params_id]
            if len(params) >= param_number:
                res = self._commands[cmd][handler_id](params)
        return res
