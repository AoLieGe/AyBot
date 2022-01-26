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


class LeaderboardID(enum.Enum):
    S = 3  # SOLO
    TG = 4  # TG

