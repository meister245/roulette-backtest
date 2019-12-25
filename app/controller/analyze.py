import itertools

from app.controller.roulette import RouletteController


class AnalyzeController(object):
    roulette_ctrl = RouletteController()

    @classmethod
    def generate_bet_patterns_combinations(cls, pattern_complexity, custom_list=''):
        patterns = []

        if isinstance(custom_list, str) and len(custom_list) > 0:
            bet_types = custom_list.split(',')
        else:
            bet_types = cls.roulette_ctrl.get_bet_types()

        for x in range(pattern_complexity):
            patterns.extend(bet_types)

        for combo in itertools.combinations(patterns, pattern_complexity):
            yield ':'.join(combo)

    @classmethod
    def generate_bet_types_combinations(cls, bet_complexity, custom_list=''):
        if isinstance(custom_list, str) and len(custom_list) > 0:
            bet_types = custom_list.split(',')
        else:
            bet_types = cls.roulette_ctrl.get_bet_types()

        for combo in itertools.combinations(bet_types, bet_complexity):
            yield ':'.join(combo)
