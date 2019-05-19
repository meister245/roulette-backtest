import itertools

from app.model.roulette import RouletteModel


class AnalyzeModel(object):
    roulette_mdl = RouletteModel()

    @classmethod
    def get_bet_patterns_combinations(cls, pattern_complexity, custom_list=False):
        patterns = []

        if isinstance(custom_list, str):
            bet_types = custom_list.split(',')
        else:
            bet_types = cls.roulette_mdl.get_bet_types()

        for x in range(pattern_complexity):
            patterns.extend(bet_types)

        combos = itertools.combinations(patterns, pattern_complexity)

        return set([':'.join(x) for x in combos])

    @classmethod
    def get_bet_types_combinations(cls, bet_complexity, custom_list=False):

        if isinstance(custom_list, str):
            bet_types = custom_list.split(',')
        else:
            bet_types = cls.roulette_mdl.get_bet_types()

        combos = itertools.combinations(bet_types, bet_complexity)

        return set([':'.join(x) for x in combos])
