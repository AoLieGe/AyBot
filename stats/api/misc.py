import enum
import json


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

