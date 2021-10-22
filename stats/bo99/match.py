import requests


class MatchParser:
    def __init__(self, name, profile_id):
        self.name = name
        self.profile_id = profile_id

    def score_with(self, opponent):
        match_count = 0
        wins = 0
        start = 0

        while True:
            r = requests.get(self._url(start))
            if r.status_code == 200:
                matches = r.json()
                if len(matches) == 0:
                    break

                for match in matches:
                    match_result = MatchParser.result(match, opponent)
                    if match_result:
                        match_count += 1
                        if match_result == 'Win':
                            wins += 1
            else:
                break
            start += 1000

        if match_count:
            return f'Арена   {self.name} {wins}:{match_count - wins} {opponent}'
        else:
            return 'Матчи не найдены'

    def _url(self, start):
        return f'https://aoe2.net/api/player/matches?game=aoe2de&profile_id={self.profile_id}&start={start}&count=1000'

    def result(self, match, opponent):
        if not match:
            return

        dur = 0
        start_time = match['started']
        finish_time = match['finished']
        player_num = match['num_players']
        map_type = match['map_type']
        players = match['players']

        if start_time and finish_time:
            dur = (finish_time - start_time) / 60

        if dur < 5 or player_num != 2 or map_type != 29:
            return

        for player in players:
            name = player['name']
            if not name:
                return

            if name == self.name:
                continue

            if opponent.lower() in name.lower():
                player_won = player['won']
                result = not player_won
                return 'Win' if result else 'Lose'
