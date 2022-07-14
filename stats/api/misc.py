import enum
import json
from datetime import datetime


def remove_brackets(resp: str) -> str:
    """remove start and end brackets ->[data]<- in rating response"""
    return resp[1:len(resp) - 1]


def calc_winrate(wins: int, losses: int) -> int:
    """calculate winrate using number of wins and number of losses"""
    if (wins + losses) != 0:
        return round(100 * wins / (wins + losses))
    else:
        return 0


def convert_rank(leaderboard: str, status: int, data: str) -> str:
    """parse rank query results into string"""

    if status == 200:
        data = remove_brackets(data)
        try:
            data = json.loads(data)
            winrate = calc_winrate(data['num_wins'], data['num_losses'])
            result = f"{leaderboard}:{data['rating']} {winrate}% {data['streak']}"
            return result

        except ValueError:
            return '----'
    else:
        return '----'


def format_time(timestamp: int) -> str:
    time = datetime.fromtimestamp(timestamp)
    return time.strftime("Started: %d.%m.%Y %H:%M:%S UTC+0\n")


def format_match_player(data: dict, rank) -> str:
    try:
        team = data['color'] if data['team'] != -1 else '-'
        return f"{team}: {data['name']} {rank}"
    except ValueError:
        return '----'


def formatted(resp: tuple) -> str:
    """remove brackets [] in rating response"""
    return resp[1:len(resp) - 1]


def to_json(resp: str) -> dict:
    try:
        return json.loads(resp)
    except ValueError:
        return {}


def format_team(team: int) -> str:
    if team == -1:
        return '-'
    else:
        return f'{team}'


def max_counts(players: list) -> tuple:
    """return player with max counts in players list"""
    counts = [(players.count(p), p) for p in players]
    sort_by_counts = [p for count, p in sorted(counts, key=lambda val: val[0], reverse=True)]
    return sort_by_counts[0]['name'], sort_by_counts[0]['steam_id']


def streak(num: str) -> str:
    return f'+{num}' if int(num) > 0 else f'{num}'


def winrate(wins: str, losses: str) -> str:
    wins = int(wins)
    losses = int(losses)
    rate = round(100 * wins / (wins + losses))
    print(rate)
    return f'{rate}'


class LeaderboardID(enum.Enum):
    S = 3  # SOLO
    TG = 4  # TG
    UNRANKED = 0

