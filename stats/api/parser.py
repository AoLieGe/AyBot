import asyncio
import aiohttp
from stats.api.request import StatsRequest as Api
from stats.api.misc import *


class StatsParser:
    @staticmethod
    async def find_steam_id(session: aiohttp.ClientSession, name: str) -> tuple:
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
    async def rating_by_id(session: aiohttp.ClientSession, steam_id: str) -> str:
        leaderboards = [lb.name for lb in LeaderboardID if lb != LeaderboardID.UNRANKED]
        tasks = [Api.rating(session, steam_id, leaderboard_id=lb.value)
                 for lb in LeaderboardID if lb != LeaderboardID.UNRANKED]
        resp = await asyncio.gather(*[asyncio.create_task(t) for t in tasks])
        json_data = [to_json(formatted(d)) if s == 200 else {} for s, d in resp]
        rates = [data['rating'] if data != {} else '----' for data in json_data]
        result = [f'{lb}:{r}' for lb, r in zip(leaderboards, rates)]
        return ' '.join(result)

    @staticmethod
    async def match_by_id(session: aiohttp.ClientSession, steam_id: str) -> str:
        status, resp = await Api.match(session, steam_id)
        if status != 200:
            return f'Error: Request return status {status}'
        try:
            data = json.loads(resp)
            players_data = data['last_match']['players']
            sorted_by_team = [p for p in sorted(players_data, key=lambda item: item['team'])]
            rates = [await StatsParser.rating_by_id(session, data['steam_id']) for data in sorted_by_team]
            return '\n'.join([f"{format_team(d['team'])}: {d['name']} {r}" for r, d in zip(rates, sorted_by_team)])
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
        except (ValueError, KeyError):
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
            'steam_id': result['steam_id']
        }

class AOE2netParser:

    # format rank response into list of player name and rank
    @staticmethod
    def rank(response_text):
        if response_text == 'Player not found':
            return None

        name = AOE2netParser._split_name(response_text)
        rank_pos = AOE2netParser._split_rank(response_text)
        rank = response_text[rank_pos[0] + 2:rank_pos[1]]
        return [name, rank]

    # format match response into list of players names
    @staticmethod
    def match(response_text):
        res = []
        commands = response_text.split(' -VS- ')

        for command in commands:
            players = command.split(' + ')
            res.append([AOE2netParser._split_name(player) for player in players])

        return res

    @staticmethod
    def _split_name(text):
        rank = AOE2netParser._split_rank(text)

        if not rank:  # if rating not in string, split string by Civilisation
            return text.split(' as ')[0]
        else:
            return text[:rank[0]]

    @staticmethod
    def _split_rank(text):
        left_bracket = ''

        # find rating in string:
        try:
            right_bracket = text.rindex(') ')
            left_bracket = text.index(' (', right_bracket - 6, right_bracket)
        except ValueError:
            return None

        return [left_bracket, right_bracket]
