import requests
from stats.api.url import AOE2netApi
from stats.api.parser import AOE2netParser
from commands.container import CmdContainer
from db.api.rank import RankApi


class StatsCmd(CmdContainer):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.db.execute(RankApi.create_table())
        self._commands = {
            '/rank': (self.rank, 1),
            '/match': (self.match, 1),
            '/reg': (self.reg, 1)
        }

    def rank(self, params):
        player = params[0]
        solo_url = AOE2netApi.rank(player, AOE2netApi.SoloID)
        tg_url = AOE2netApi.rank(player, AOE2netApi.TeamID)

        solo_resp = requests.get(solo_url)
        tg_resp = requests.get(tg_url)

        solo_rating = AOE2netParser.rank(solo_resp.text)
        tg_rating = AOE2netParser.rank(tg_resp.text)

        name = player
        solo = tg = '----'

        if solo_rating:
            name = solo_rating[0]
            solo = solo_rating[1]
        if tg_rating:
            name = tg_rating[0]
            tg = tg_rating[1]

        res = f"{name} S:{solo} TG:{tg}"
        return res

    def match(self, params):
        user = params[0]
        match_url = AOE2netApi.match(user=user)

        match_resp = requests.get(match_url)

        commands = AOE2netParser.match(match_resp.text)

        res = []

        for players in commands:
            cmd = []
            for player in players:
                cmd.append(self.rank([player]))
            res.append('\n'.join(cmd))

        return '\n        --VS--\n'.join(res)

    def reg(self, param):
        user = self.msg.author.id
        steam_id = param[0]
        data = self.db.fetchone(RankApi.get_user(user))
        print(user)
        print(steam_id)
        print(data)
        if not data:
            self.db.fetchone(RankApi.add_user(user, steam_id))

    def users(self):
        pass
