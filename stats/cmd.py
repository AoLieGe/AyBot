import aiohttp
import requests
from commands.container import CmdContainer
from db.api.rank import RankApi
from stats.bo99.match import MatchParser
from stats.api.parser import StatsParser as Stats


class StatsCmd(CmdContainer):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.db.execute(RankApi.create_table())
        self.bo99_parser = MatchParser('[SDG]Колясик', 3574406)

        self._commands = {
            '/rank': (self.rank, 0),
            '/match': (self.match, 0),
            '/reg': (self.reg, 1),
            '/unreg': (self.unreg, 0),
            '/бо99': (self.bo99, 1)
        }

    async def rank(self, params):
        async with aiohttp.ClientSession() as s:
            if params:
                player = ' '.join(params)

                resp = await Stats.find_steam_id(s, player)
                if not resp:
                    return "Player not found"

                name, steam_id = resp
            else:
                steam_id = self._get_user_steam()
                if not steam_id:
                    return 'Player not found'

                name = await Stats.find_name_by_id(s, steam_id)
                if name == '':
                    return 'Player not found'

            ratings = await Stats.rating_by_id(s, steam_id)
            return f'{name} {ratings}'

    async def match(self, params):
        async with aiohttp.ClientSession() as s:
            if params:
                player = ' '.join(params)

                resp = await Stats.find_steam_id(s, player)
                print(resp)
                if not resp:
                    return "Player not found"

                name, steam_id = resp
            else:
                steam_id = self._get_user_steam()
                if not steam_id:
                    return 'Player not found'

            return await Stats.match_by_id(s, steam_id)

    async def reg(self, param):
        user = self.msg.author.id
        steam_id = param[0]
        data = self.db.fetchone(RankApi.get_user(user))

        if not data:
            self.db.execute(RankApi.add_user(user, steam_id))
            return 'Success'

    async def unreg(self, params):
        user = self.msg.author.id
        data = self.db.fetchone(RankApi.get_user(user))
        if data:
            self.db.execute(RankApi.del_user(user))
            return 'Success'
        else:
            return 'User not registered'

    def bo99(self, params):
        player = ' '.join(params)
        return self.bo99_parser.score_with(player)

    def _get_user_steam(self):
        user = self.msg.author.id
        data = self.db.fetchone(RankApi.get_user(user))
        if data:
            return data[1]
