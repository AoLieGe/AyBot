class CmdParser:
    _parsers = []

    def add_parser(self, cmd_parser):
        self._parsers.append(cmd_parser)

    def delete_parser(self, cmd_parser):
        if cmd_parser in self._parsers:
            self._parsers.remove(cmd_parser)

    async def parse(self, message):
        for parser in self._parsers:
            result = await parser.parse(message)
            if result:
                break

        return result
