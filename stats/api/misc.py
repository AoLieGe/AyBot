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
    sort_by_counts = [p for count, p in sorted(counts, key=lambda val: val[0])]
    return sort_by_counts[0]['name'], sort_by_counts[0]['steam_id']


class LeaderboardID(enum.Enum):
    S = 3  # SOLO
    TG = 4  # TG
    UNRANKED = 0

