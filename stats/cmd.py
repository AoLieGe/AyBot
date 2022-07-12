import time

import aiohttp
import asyncio
import requests
from commands.container import CmdContainer
from db.api.rank import RankApi
from db.api.sdg import SdgApi
from stats.bo99.match import MatchParser
from stats.api.parser import StatsParser as Stats
from stats.api.request import StatsRequest as Api
from stats.api.misc import *


class StatsCmd(CmdContainer):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.db.execute(RankApi.create_table())
        self.db.execute(SdgApi.create_table())
        # tm = int(time.mktime(time.struct_time((2022, 1, 1, 0, 0, 0, 5, 1, -1))))
        # self.db.execute(SdgApi.add_user(76561198131951866, 1063, 0, tm))
        self.bo99_parser = MatchParser('[SDG]Колясик', 3574406)

        self._commands = {
            '/rank': (self.rank, 0),
            '/rank2': (self.rank, 0),
            '/match': (self.match, 0),
            '/reg': (self.reg, 1),
            '/unreg': (self.unreg, 0),
            '/бо99': (self.bo99, 1),
            '/sdg': (self.sdg, 0),
            '/sdgadd': (self.sdg_add, 1),
            '/sdgdel': (self.sdg_del, 1),
            '/sdgdrop': (self.sdg_drop, 0)
        }

    async def rank(self, params):
        async with aiohttp.ClientSession() as s:
            if params:
                player = ' '.join(params)

                resp = await Stats.find_player_id(s, player)
                if not resp:
                    return "Player not found"

                name, steam_id = resp
            else:
                steam_id = self._get_user_steam()
                if not steam_id:
                    return 'Player not found'

                name = await Stats.find_name_by_id(s, steam_id)
                if name == '':
                    return 'Для использования команды без ника необходимо выполнить команду:\n /reg твой_стим_id\n ' \
                           'Без регистрации steam_id использование команды возможно только с указанием ника '

            ratings = await Stats.rating_by_id(s, steam_id, '')
            return f'{name} {ratings}'

    async def match(self, params):
        async with aiohttp.ClientSession() as s:
            if params:
                player = ' '.join(params)

                resp = await Stats.find_player_id(s, player)
                if not resp:
                    return "Player not found"

                name, steam_id = resp
            else:
                steam_id = self._get_user_steam()
                if not steam_id:
                    return 'Для использования команды без ника необходимо выполнить команду:\n /reg твой_стим_id\n ' \
                           'Без регистрации steam_id использование команды возможно только с указанием ника '

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

    async def bo99(self, params):
        player = ' '.join(params)
        return self.bo99_parser.score_with(player)

    async def sdg(self, params):
        sdg = self.db.fetchall(SdgApi.get_users())
        info = []
        async with aiohttp.ClientSession() as s:
            names = [Stats.find_name_by_id(s, player[0]) for player in sdg]
            rates = [Api.rating(s, steam_id, '', leaderboard_id=LeaderboardID.S.value)
                     for steam_id in sdg]

            tasks = names + rates
            resp = await asyncio.gather(*[asyncio.create_task(t) for t in tasks])

            names = resp[:int(len(resp)/2)]
            rates = resp[int(len(resp)/2):]
            print(names)
            print(rates)
            json_data = [to_json(formatted(d)) if s == 200 else {} for s, d in rates]
            print(json_data)
            rates = [data['rating'] if data != {} else '----' for data in json_data]
            print(rates)
            result = [f'{name}: {rate}' for name, rate in
                      sorted(zip(names, rates), key=lambda val: val[1], reverse=True)]
            return '\n'.join(result)

    async def sdg_add(self, params):
        for member in params:
            self.db.execute(SdgApi.add_user(member))

    async def sdg_del(self, params):
        for member in params:
            self.db.execute(SdgApi.del_user(member))

    async def sdg_drop(self, params):
        self.db.execute(SdgApi.drop_table())
        self.db.execute(SdgApi.create_table())

    def _get_user_steam(self):
        user = self.msg.author.id
        data = self.db.fetchone(RankApi.get_user(user))
        if data:
            return data[1]
