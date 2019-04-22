from typing import List

import cachetools.func

TIER, ORPHELINS, VOISONS, ZERO = 'tier', 'orphelins', 'voisons', 'zero'
RED, BLACK, EVEN, ODD, LOW, HIGH = 'red', 'black', 'even', 'odd', 'low', 'high'
COLUMN_TOP, COLUMN_MIDDLE, COLUMN_BOTTOM = 'column_top', 'column_center', 'column_bottom'
DOZEN_LEFT, DOZEN_MIDDLE, DOZEN_RIGHT = 'dozen_left', 'dozen_middle', 'dozen_right'
LINE, CORNER, FOUR, STREET, SPLIT, STRAIGHT = 'line', 'corner', 'four', 'street', 'split', 'straight'


class RouletteModel(object):
    number_mapping = {
        COLUMN_TOP: [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
        COLUMN_MIDDLE: [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
        COLUMN_BOTTOM: [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],

        ZERO: [12, 35, 3, 26, 0, 32, 15],
        ORPHELINS: [17, 34, 6, 1, 20, 14, 31, 9],
        VOISONS: [22, 18, 29, 7, 28, 19, 4, 21, 2, 25],
        TIER: [27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33],

        RED: [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
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

    @classmethod
    def is_pattern_match(cls, pattern, numbers):
        p_subset = []
        win_types = cls.get_win_types_all()
        last_n_numbers = numbers[-len(pattern):]

        for idx, num in enumerate(last_n_numbers):
            type = cls.validate_bet_type(pattern[idx])
            p_subset.append(type if type in win_types[num] else None)

            if tuple(p_subset) == pattern:
                return True

        return False

    @classmethod
    def get_bet_pattern(cls, bet_pattern: str) -> tuple:
        patterns = bet_pattern.split(':')

        if len(patterns) == 0:
            raise ValueError('invalid bet pattern')

        for x in patterns:
            cls.validate_bet_type(x)

        return tuple([x for x in patterns if len(x) != 0])

    @classmethod
    @cachetools.func.lfu_cache()
    def get_bet_types(cls) -> List[str]:
        bet_types = [RED, BLACK, EVEN, ODD, LOW, HIGH, TIER, ORPHELINS, VOISONS, ZERO, FOUR,
                     COLUMN_TOP, COLUMN_MIDDLE, COLUMN_BOTTOM, DOZEN_LEFT, DOZEN_MIDDLE, DOZEN_RIGHT]

        bet_types.extend(['{}_{}'.format(STRAIGHT, x) for x in range(37)])
        bet_types.extend(['{}_{}_{}'.format(SPLIT, x[0], x[1]) for x in cls.number_mapping[SPLIT]])
        bet_types.extend(['{}_{}_{}_{}'.format(STREET, x[0], x[1], x[2]) for x in cls.number_mapping[STREET]])
        bet_types.extend(['{}_{}_{}_{}_{}'.format(CORNER, x[0], x[1], x[2], x[3]) for x in cls.number_mapping[CORNER]])
        bet_types.extend(['{}_{}_{}_{}_{}_{}_{}'.format(LINE, x[0], x[1], x[2], x[3], x[4], x[5]) for x in
                          cls.number_mapping[LINE]])

        return bet_types

    @classmethod
    @cachetools.func.lfu_cache()
    def get_win_types_all(cls) -> dict:
        win_types = {}

        for n in [x for x in range(37)]:
            win_types[n] = cls.get_win_types(n)

        return win_types

    @classmethod
    def get_win_types(cls, number: int) -> List[str]:
        win_types = ['{}_{}'.format(STRAIGHT, number), 'any']

        if number == 0:
            win_types.append(FOUR)
            win_types.append(ZERO)

        elif number != 0:
            win_types.append(RED if number in cls.number_mapping[RED] else BLACK)
            win_types.append(EVEN if number % 2 == 0 else ODD)
            win_types.append(LOW if 1 <= number <= 18 else HIGH)

            win_types.append(
                COLUMN_TOP if number in cls.number_mapping[COLUMN_TOP] else COLUMN_MIDDLE
                if number in cls.number_mapping[COLUMN_MIDDLE] else COLUMN_BOTTOM
            )

            win_types.append(
                DOZEN_LEFT if 1 <= number <= 12 else DOZEN_MIDDLE
                if 13 <= number <= 22 else DOZEN_RIGHT
            )

            win_types.append(
                TIER if number in cls.number_mapping[TIER] else ORPHELINS
                if number in cls.number_mapping[ORPHELINS] else VOISONS
                if number in cls.number_mapping[VOISONS] else ZERO
            )

            if number in cls.number_mapping[FOUR]:
                win_types.append(FOUR)

            for x in cls.number_mapping[SPLIT]:
                if number in x:
                    win_types.append('{}_{}_{}'.format(SPLIT, x[0], x[1]))

            for x in cls.number_mapping[STREET]:
                if number in x:
                    win_types.append('{}_{}_{}_{}'.format(STREET, x[0], x[1], x[2]))

            for x in cls.number_mapping[CORNER]:
                if number in x:
                    win_types.append('{}_{}_{}_{}_{}'.format(CORNER, x[0], x[1], x[2], x[3]))

            for x in cls.number_mapping[LINE]:
                if number in x:
                    win_types.append('{}_{}_{}_{}_{}_{}_{}'.format(LINE, x[0], x[1], x[2], x[3], x[4], x[5]))

        return win_types

    @classmethod
    def validate_bet_type(cls, bet_type_name: str) -> str:
        if bet_type_name == 'any':
            return bet_type_name

        elif bet_type_name not in cls.get_bet_types():
            raise ValueError('invalid bet type - {}'.format(bet_type_name))

        return bet_type_name
