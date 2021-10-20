class AOE2netApi:
    SoloID = 3
    TeamID = 4

    @staticmethod
    def rank(user='', steam_id=None, leaderboard_id=SoloID):
        if not user and not steam_id:
            return

        url = f"https://aoe2.net/api/nightbot/rank?leaderboard_id={leaderboard_id}&color=false&flag=false"
        if user:
            url += f'&search={user}'
        if steam_id:
            url += f"&steam_id={steam_id}"

        return url

    @staticmethod
    def match(user='', steam_id=None):
        if not user and not steam_id:
            return

        url = "https://aoe2.net/api/nightbot/match?color=false&flag=false"
        if user:
            url += f"&search={user}"
        if steam_id:
            url += f"&steam_id={steam_id}"

        return url
