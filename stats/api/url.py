class AOE2netApi:
    SoloID = 3
    TeamID = 4

    @staticmethod
    def rank(user, leaderboard_id=SoloID):
        return f"https://aoe2.net/api/nightbot/rank?search={user}&leaderboard_id={leaderboard_id}&color=false&flag=false"

    @staticmethod
    def match(user='', steam_id=None):
        if not user and not steam_id:
            return None

        req = "https://aoe2.net/api/nightbot/match?color=false&flag=false"
        if user:
            req += f"&search={user}"
        if steam_id:
            req += f"&steam_id={steam_id}"

        return req
