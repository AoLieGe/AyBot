from stats.api.misc import *
from misc.response import get_response


class StatsRequest:
    @staticmethod
    async def leaderboard(session, name: str = '', steam_id: str = '',
                          leaderboard_id: LeaderboardID = LeaderboardID.SOLO.value):
        url = "https://aoe2.net/api/leaderboard"
        params = {
            'game': 'aoe2de',
            'leaderboard_id': f'{leaderboard_id}',
            'count': '10000',
        }

        if name:
            params['search'] = f'{name}'
        elif steam_id:
            params['steam_id'] = f'{steam_id}'

        print(f'{name} + {params}')

        return await get_response(session, url, params)

    @staticmethod
    async def rating(session, steam_id: str, leaderboard_id: LeaderboardID):
        url = "https://aoe2.net/api/player/ratinghistory"
        params = {
            'game': 'aoe2de',
            'leaderboard_id': f'{leaderboard_id}',
            'start': '0',
            'count': '1',
            'steam_id': steam_id
        }

        return await get_response(session, url, params)

    @staticmethod
    async def match(session, steam_id: str):
        url = "https://aoe2.net/api/player/lastmatch"
        params = {
            'game': 'aoe2de',
            'steam_id': steam_id
        }

        return await get_response(session, url, params)
