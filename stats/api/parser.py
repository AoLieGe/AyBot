import asyncio
import aiohttp
from datetime import datetime

import stats.api.misc
from stats.api.request import StatsRequest as Api
from stats.api.misc import *


class StatsParser:
    @staticmethod
    async def find_name_by_id(session: aiohttp.ClientSession, steam_id: str) -> str:
        status, resp = await Api.match(session, steam_id)
        if status != 200:
            return f''
        try:
            data = json.loads(resp)
            return data['name']
        except ValueError:
            return ''

    @staticmethod
    async def find_player_id(session: aiohttp.ClientSession, name: str) -> tuple:
        """return (name, steam_id) for founded player or None if not"""
        tasks = [StatsParser._find_player(session, name, lb.value) for lb in LeaderboardID]
        resp = await asyncio.gather(*[asyncio.create_task(t) for t in tasks])
        full_match = [p for p in resp if p and p['full_match']]
        if full_match:
            return max_counts(full_match)

        not_full_match = [p for p in resp if p and not p['full_match']]
        if not_full_match:
            return max_counts(not_full_match)

    @staticmethod
    async def rating_by_id(session: aiohttp.ClientSession, steam_id: str, profile_id: str) -> str:
        leaderboards = [lb.name for lb in LeaderboardID if lb != LeaderboardID.UNRANKED]
        if (not steam_id or steam_id == '') and (not profile_id or profile_id == ''):
            return ' '.join([f'{lb}:----' for lb in leaderboards])

        tasks = [Api.rating(session, steam_id, profile_id, leaderboard_id=lb.value)
                 for lb in LeaderboardID if lb != LeaderboardID.UNRANKED]
        resp = await asyncio.gather(*[asyncio.create_task(t) for t in tasks])
        json_data = [to_json(formatted(d)) if s == 200 else {} for s, d in resp]
        rates = [(data['rating'], data['num_wins'], data['num_losses'], data['streak'])
                 if data != {} else '----' for data in json_data]
        result = [f'{lb}:{r[0]} {int(int(r[1]) / (int(r[1]) + int(r[2])))}% {streak(r[3])}'
                  for lb, r in zip(leaderboards, rates)]
        return ' | '.join(result)

    @staticmethod
    async def match_by_id(session: aiohttp.ClientSession, steam_id: str) -> str:
        status, resp = await Api.match(session, steam_id)
        if status != 200:
            return f'Error: Request return status {status}'
        try:
            data = json.loads(resp)
            timestamp = data['last_match']['opened']
            players_data = data['last_match']['players']
            time = datetime.fromtimestamp(timestamp)
            time_str = time.strftime("Started: %d.%m.%Y %H:%M:%S UTC+0\n")
            sorted_by_team = [p for p in sorted(players_data, key=lambda item: item['team'])]
            rates = [await StatsParser.rating_by_id(session, data['steam_id'], data['profile_id'])
                     for data in sorted_by_team]
            rates_str = '\n'.join([f"{format_team(d['team'])}: {d['name']} {r}" for r, d in zip(rates, sorted_by_team)])
            return time_str + rates_str
        except ValueError:
            return 'Match parse error: incorrect match json'

    @staticmethod
    async def _find_player(session: aiohttp.ClientSession, name: str, leaderboard_id: LeaderboardID) -> dict:
        """find full match in name or return first if not found or return {} if any players not found"""
        status, resp = await Api.leaderboard(session, name, leaderboard_id)
        if status != 200:
            return {}

        try:
            players = json.loads(resp)['leaderboard']
        except ValueError:
            return {}

        if not players:
            return {}

        full_match = False
        for player in players:
            if name == player['name']:
                result = player
                full_match = True
                break
        else:
            result = players[0]

        return {
            'full_match': full_match,
            'name': result['name'],
            'steam_id': result['steam_id'],
            'profile_id': result['profile_id']
        }
