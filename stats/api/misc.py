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


class LeaderboardID(enum.Enum):
    # UNRANKED = 0
    SOLO = 3
    TG = 4
