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
            '/rank': (self.rank, 0),
            '/match': (self.match, 0),
            '/reg': (self.reg, 1),
            '/unreg': (self.unreg, 0)
        }

    def rank(self, params):
        if params:
            player = ' '.join(params)
            solo_url = AOE2netApi.rank(player=player, leaderboard_id=AOE2netApi.SoloID)
            tg_url = AOE2netApi.rank(player=player, leaderboard_id=AOE2netApi.TeamID)
        else:
            steam_id = self._get_user_steam()
            if not steam_id:
                return 'User not found'

            solo_url = AOE2netApi.rank(steam_id=steam_id, leaderboard_id=AOE2netApi.SoloID)
            tg_url = AOE2netApi.rank(steam_id=steam_id, leaderboard_id=AOE2netApi.TeamID)

        solo_resp = requests.get(solo_url)
        tg_resp = requests.get(tg_url)

        solo_rating = AOE2netParser.rank(solo_resp.text)
        tg_rating = AOE2netParser.rank(tg_resp.text)

        name = ''
        solo = tg = '----'

        if solo_rating:
            name = solo_rating[0]
            solo = solo_rating[1]
        if tg_rating:
            name = tg_rating[0]
            tg = tg_rating[1]

        if name:
            res = f"{name} S:{solo} TG:{tg}"
        else:
            res = 'Rank not found'
        return res

    def match(self, params):
        if params:
            player = ' '.join(params)
            match_url = AOE2netApi.match(player=player)
        else:
            steam_id = self._get_user_steam()
            if not steam_id:
                return 'User not found'

            match_url = AOE2netApi.match(steam_id=steam_id)

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
        if not param:
            return "Reg error"

        user = self.msg.author.id
        steam_id = param[0]
        data = self.db.fetchone(RankApi.get_user(user))

        if not data:
            self.db.execute(RankApi.add_user(user, steam_id))
            return 'Success'

    def unreg(self, param):
        user = self.msg.author.id
        data = self.db.fetchone(RankApi.get_user(user))
        if data:
            self.db.execute(RankApi.del_user(user))
            return 'Success'
        else:
            return 'User not registered'

    def _get_user_steam(self):
        user = self.msg.author.id
        data = self.db.fetchone(RankApi.get_user(user))
        if data:
            return data[1]
