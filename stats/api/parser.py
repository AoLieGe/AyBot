class AOE2netParser:

    # format rank response into list of player name and rank
    @staticmethod
    def rank(response_text):
        if response_text == 'Player not found':
            return None

        name = AOE2netParser._split_name(response_text)
        rank_pos = AOE2netParser._split_rank(response_text)
        rank = response_text[rank_pos[0]+2:rank_pos[1]]
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
