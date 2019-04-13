from typing import List

from app.factory.strategy import StrategyFactory

import cachetools.func

TIER, ORPHELINS, VOISONS, ZERO = 'tier', 'orphelins', 'voisons', 'zero'
RED, BLACK, EVEN, ODD, LOW, HIGH = 'red', 'black', 'even', 'odd', 'low', 'high'
COLUMN_TOP, COLUMN_MIDDLE, COLUMN_BOTTOM = 'column_top', 'column_center', 'column_bottom'
DOZEN_LEFT, DOZEN_MIDDLE, DOZEN_RIGHT = 'dozen_left', 'dozen_middle', 'dozen_right'
LINE, CORNER, FOUR, STREET, SPLIT, STRAIGHT = 'line', 'corner', 'four', 'street', 'split', 'straight'


class BetModel(object):
    bet_mapping = {
        COLUMN_TOP: [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
        COLUMN_MIDDLE: [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
        COLUMN_BOTTOM: [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],

        ZERO: [12, 35, 3, 26, 0, 32, 15],
        ORPHELINS: [17, 34, 6, 1, 20, 14, 31, 9],
        VOISONS: [22, 18, 29, 7, 28, 19, 4, 21, 2, 25],
        TIER: [27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33],

        RED: [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 27, 30, 32, 34, 36],
        BLACK: [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35],

        FOUR: [0, 1, 2, 3],

        STREET: [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12), (13, 14, 15), (16, 17, 18), (19, 20, 21),
                 (22, 23, 24), (25, 26, 27), (28, 29, 30), (31, 32, 33), (34, 35, 36)],

        LINE: [(1, 2, 3, 4, 5, 6), (4, 5, 6, 7, 8, 9), (7, 8, 9, 10, 11, 12), (10, 11, 12, 13, 14, 15),
               (13, 14, 15, 16, 17, 18), (16, 17, 18, 19, 20, 21), (19, 20, 21, 22, 23, 24), (22, 23, 24, 25, 26, 27),
               (25, 26, 27, 28, 29, 30), (28, 29, 30, 31, 32, 33), (31, 32, 33, 34, 35, 36)],

        CORNER: [(1, 2, 4, 5), (2, 3, 5, 6), (4, 5, 7, 8), (5, 6, 8, 9), (7, 8, 10, 11), (8, 9, 11, 12),
                 (10, 11, 13, 14), (11, 12, 14, 15), (13, 14, 16, 17), (14, 15, 17, 18), (16, 17, 19, 20),
                 (17, 18, 20, 21), (19, 20, 22, 23), (20, 21, 23, 24), (22, 23, 25, 26), (23, 24, 26, 27),
                 (25, 26, 28, 29), (26, 27, 29, 30), (28, 29, 31, 32), (29, 30, 32, 33), (31, 32, 34, 35),
                 (32, 33, 35, 36)],

        SPLIT: [(1, 2), (2, 3), (4, 5), (5, 6), (7, 8), (8, 9), (10, 11), (11, 12), (13, 14), (14, 15), (16, 17),
                (17, 18), (19, 20), (20, 21), (22, 23), (23, 24), (25, 26), (26, 27), (28, 29), (29, 30), (31, 32),
                (32, 33), (34, 35), (35, 36), (1, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9), (7, 10), (8, 11),
                (9, 12), (10, 13), (11, 14), (12, 15), (13, 16), (14, 17), (15, 18), (16, 19), (17, 20), (18, 21),
                (19, 22), (20, 23), (21, 24), (22, 25), (23, 26), (24, 27), (25, 28), (26, 29), (27, 30), (28, 31),
                (29, 32), (30, 33), (31, 34), (32, 35), (33, 36)]
    }

    payout_mapping = {
        RED: 1, BLACK: 1, EVEN: 1, ODD: 1, LOW: 1, HIGH: 1, DOZEN_LEFT: 2,
        DOZEN_MIDDLE: 2, DOZEN_RIGHT: 2, COLUMN_TOP: 2, COLUMN_MIDDLE: 2, COLUMN_BOTTOM: 2,
        LINE: 5, CORNER: 8, FOUR: 8, STREET: 11, SPLIT: 17, STRAIGHT: 35
    }

    strategy_fctr = StrategyFactory()

    @classmethod
    def parse_bet_pattern(cls, config_pattern: str) -> dict:
        elements = [x for x in config_pattern.split(',') if len(x) != 0]

        if len(elements) != 5:
            exit('invalid bet pattern - {}'.format(config_pattern))

        return {
            'active': False,
            'lose_current': 0,
            'lose_limit': int(elements[4]),
            'pattern': cls.get_bet_pattern(elements[1]),
            'size_current': float(elements[2]),
            'size_original': float(elements[2]),
            'strategy': cls.strategy_fctr.get_strategy(elements[0]),
            'type': cls.validate_bet_type(elements[3])
        }

    @classmethod
    def get_bets_result(cls, bets, win_types):
        bets_result = []

        for x in bets:
            if x['active']:
                win_loss = True if x['type'] in win_types else False
                result = {'bet_type': x['type'], 'bet_amount': x['size_current'], 'win': win_loss}
                bets_result.append(result)

        return bets_result if len(bets_result) > 0 else None

    @classmethod
    def update_bets(cls, bets, bet_result, total_results, **kwargs):
        new_bets = []

        for b in bets:
            new_bet = b

            if not b['active']:
                new_bet['active'] = cls.match_patterns(b, total_results)

            elif b['active'] and 0 < b['lose_limit'] == b['lose_current']:
                new_bet['active'] = False
                new_bet['lose_current'] = 0
                new_bet['size_current'] = new_bet['size_original']

            elif b['active'] and b['type'] in bet_result['win_types']:
                new_bet['active'] = False
                new_bet['lose_current'] = 0
                new_bet['size_current'] = new_bet['size_original']

            elif b['active'] and b['type'] not in bet_result['win_types']:
                new_bet['size_current'] = b['strategy'].set_new_bet(b, bet_result, kwargs.get('table_limit', 150.0))
                new_bet['lose_current'] += 1

            new_bets.append(new_bet)

        return new_bets

    @classmethod
    def match_patterns(cls, bet, total_results):
        pattern_len = len(bet['pattern'])

        if pattern_len <= len(total_results):
            pattern_subset = []

            for idx, result in enumerate(total_results[-pattern_len:]):
                p = bet['pattern'][idx] if bet['pattern'][idx] in result['win_types'] else None
                pattern_subset.append(p)

            if tuple(pattern_subset) != bet['pattern']:
                return False

        else:
            return False

        return True

    @classmethod
    def get_bet_pattern(cls, result_pattern: str) -> tuple:
        return tuple([cls.validate_bet_type(x) for x in result_pattern.split(':') if len(x) != 0])

    @classmethod
    def validate_bet_type(cls, bet_type_name: str) -> str:
        if bet_type_name not in cls.get_bet_types():
            exit('invalid bet_type - {}'.format(bet_type_name))

        return bet_type_name

    @classmethod
    @cachetools.func.lfu_cache()
    def get_bet_types(cls) -> List[str]:
        bet_types = [RED, BLACK, EVEN, ODD, LOW, HIGH, TIER, ORPHELINS, VOISONS, ZERO, FOUR, COLUMN_TOP, COLUMN_MIDDLE,
                     COLUMN_BOTTOM, DOZEN_LEFT, DOZEN_MIDDLE, DOZEN_RIGHT]

        bet_types.extend(['{}_{}'.format(STRAIGHT, x) for x in range(37)])
        bet_types.extend(['{}_{}_{}'.format(SPLIT, x[0], x[1]) for x in cls.bet_mapping[SPLIT]])
        bet_types.extend(['{}_{}_{}_{}'.format(STREET, x[0], x[1], x[2]) for x in cls.bet_mapping[STREET]])
        bet_types.extend(['{}_{}_{}_{}_{}'.format(CORNER, x[0], x[1], x[2], x[3]) for x in cls.bet_mapping[CORNER]])
        bet_types.extend(['{}_{}_{}_{}_{}_{}_{}'.format(LINE, x[0], x[1], x[2], x[3], x[4], x[5]) for x in
                          cls.bet_mapping[LINE]])

        return bet_types

    @classmethod
    def get_bets_sum(cls, bets):
        current_bets_values = [x['size_current'] for x in bets if x['active']]
        bet_sum = sum(current_bets_values) if len(current_bets_values) > 0 else 0
        return round(bet_sum, 2)

    @classmethod
    def get_win_bet_types(cls, number: int) -> List[str]:
        win_bet_types = ['{}_{}'.format(STRAIGHT, number)]

        if number == 0:
            win_bet_types.append(FOUR)
            win_bet_types.append(ZERO)

        elif number != 0:
            win_bet_types.append(RED if number in cls.bet_mapping[RED] else BLACK)
            win_bet_types.append(EVEN if number % 2 == 0 else ODD)
            win_bet_types.append(LOW if 1 <= number <= 18 else HIGH)

            win_bet_types.append(
                COLUMN_TOP if number in cls.bet_mapping[COLUMN_TOP] else COLUMN_MIDDLE
                if number in cls.bet_mapping[COLUMN_MIDDLE] else COLUMN_BOTTOM
            )

            win_bet_types.append(
                DOZEN_LEFT if 1 <= number <= 12 else DOZEN_MIDDLE
                if 13 <= number <= 22 else DOZEN_RIGHT
            )

            win_bet_types.append(
                TIER if number in cls.bet_mapping[TIER] else ORPHELINS
                if number in cls.bet_mapping[ORPHELINS] else VOISONS
                if number in cls.bet_mapping[VOISONS] else ZERO
            )

            if number in cls.bet_mapping[FOUR]:
                win_bet_types.append(FOUR)

            for x in cls.bet_mapping[SPLIT]:
                if number in x:
                    win_bet_types.append('{}_{}_{}'.format(SPLIT, x[0], x[1]))

            for x in cls.bet_mapping[STREET]:
                if number in x:
                    win_bet_types.append('{}_{}_{}_{}'.format(STREET, x[0], x[1], x[2]))

            for x in cls.bet_mapping[CORNER]:
                if number in x:
                    win_bet_types.append('{}_{}_{}_{}_{}'.format(CORNER, x[0], x[1], x[2], x[3]))

            for x in cls.bet_mapping[LINE]:
                if number in x:
                    win_bet_types.append('{}_{}_{}_{}_{}_{}_{}'.format(LINE, x[0], x[1], x[2], x[3], x[4], x[5]))

        else:
            exit('invalid number - {}'.format(number))

        return win_bet_types
