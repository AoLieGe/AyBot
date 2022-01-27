from stats.api.misc import *
from misc.response import get_response


class StatsRequest:
    @staticmethod
    async def leaderboard(session, name: str,
                          leaderboard_id: LeaderboardID = LeaderboardID.S.value):
        url = "https://aoe2.net/api/leaderboard"
        params = {
            'game': 'aoe2de',
            'leaderboard_id': f'{leaderboard_id}',
            'count': '10000',
            'search': f'{name}'
        }

        return await get_response(session, url, params)


    "https://aoe2.net/api/player/ratinghistory?game=aoe2de&leaderboard_id=3&start=0&count=1&profile_id=6082789"
    @staticmethod
    async def rating(session, steam_id: str, profile_id: str, leaderboard_id: LeaderboardID):
        url = "https://aoe2.net/api/player/ratinghistory"
        params = {
            'game': 'aoe2de',
            'leaderboard_id': f'{leaderboard_id}',
            'start': '0',
            'count': '1'
        }

        if steam_id and steam_id != '':
            params['steam_id'] = steam_id
        if profile_id and profile_id != '':
            params['profile_id'] = steam_id

        return await get_response(session, url, params)

    "https://aoe2.net/api/player/lastmatch?game=aoe2de&steam_id=76561198379389049"
    @staticmethod
    async def match(session, steam_id: str):
        url = "https://aoe2.net/api/player/lastmatch"
        params = {
            'game': 'aoe2de',
            'steam_id': steam_id
        }

        return await get_response(session, url, params)
