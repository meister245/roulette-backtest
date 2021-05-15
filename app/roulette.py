import math
from typing import List

import cachetools.func

COLUMN, DOZEN = 'column', 'dozen'
RED, BLACK, EVEN, ODD, LOW, HIGH = 'red', 'black', 'even', 'odd', 'low', 'high'
LINE, CORNER, FOUR, STREET, SPLIT, STRAIGHT = 'line', 'corner', 'four', 'street', 'split', 'straight'


class Roulette:
    number_mapping = {
        RED: (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36),
        BLACK: (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35),

        FOUR: (0, 1, 2, 3),

        STREET: ((1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12), (13, 14, 15), (16, 17, 18), (19, 20, 21),
                 (22, 23, 24), (25, 26, 27), (28, 29, 30), (31, 32, 33), (34, 35, 36)),

        LINE: ((1, 2, 3, 4, 5, 6), (4, 5, 6, 7, 8, 9), (7, 8, 9, 10, 11, 12), (10, 11, 12, 13, 14, 15),
               (13, 14, 15, 16, 17, 18), (16, 17, 18, 19, 20, 21), (19, 20, 21, 22, 23, 24), (22, 23, 24, 25, 26, 27),
               (25, 26, 27, 28, 29, 30), (28, 29, 30, 31, 32, 33), (31, 32, 33, 34, 35, 36)),

        CORNER: ((1, 2, 4, 5), (2, 3, 5, 6), (4, 5, 7, 8), (5, 6, 8, 9), (7, 8, 10, 11), (8, 9, 11, 12),
                 (10, 11, 13, 14), (11, 12, 14, 15), (13, 14, 16, 17), (14, 15, 17, 18), (16, 17, 19, 20),
                 (17, 18, 20, 21), (19, 20, 22, 23), (20, 21, 23, 24), (22, 23, 25, 26), (23, 24, 26, 27),
                 (25, 26, 28, 29), (26, 27, 29, 30), (28, 29, 31, 32), (29, 30, 32, 33), (31, 32, 34, 35),
                 (32, 33, 35, 36)),

        SPLIT: ((1, 2), (2, 3), (4, 5), (5, 6), (7, 8), (8, 9), (10, 11), (11, 12), (13, 14), (14, 15), (16, 17),
                (17, 18), (19, 20), (20, 21), (22, 23), (23, 24), (25, 26), (26, 27), (28, 29), (29, 30), (31, 32),
                (32, 33), (34, 35), (35, 36), (1, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9), (7, 10), (8, 11),
                (9, 12), (10, 13), (11, 14), (12, 15), (13, 16), (14, 17), (15, 18), (16, 19), (17, 20), (18, 21),
                (19, 22), (20, 23), (21, 24), (22, 25), (23, 26), (24, 27), (25, 28), (26, 29), (27, 30), (28, 31),
                (29, 32), (30, 33), (31, 34), (32, 35), (33, 36))
    }

    payout_mapping = {
        RED: 1, BLACK: 1, EVEN: 1, ODD: 1, LOW: 1, HIGH: 1, DOZEN: 2, COLUMN: 2,
        LINE: 5, CORNER: 8, FOUR: 8, STREET: 11, SPLIT: 17, STRAIGHT: 35
    }

    @classmethod
    def is_pattern_match(cls, pattern, numbers):
        p_subset = []
        win_types = cls.get_win_types_all()
        last_n_numbers = numbers[-len(pattern):]

        for idx, num in enumerate(last_n_numbers):
            t = cls.validate_bet_type(pattern[idx])
            p_subset.append(t if t in win_types[num] else None)

            if tuple(p_subset) == pattern:
                return True

        return False

    @classmethod
    def get_bet_pattern(cls, bet_pattern: str) -> tuple:
        patterns = bet_pattern.split(':')

        if len(patterns) == 0:
            raise ValueError('invalid model pattern')

        for x in patterns:
            cls.validate_bet_type(x)

        return tuple(reversed([x for x in patterns if len(x) != 0]))

    @classmethod
    def analyze_last_n_numbers(cls, numbers, n=100):
        if len(numbers) < n:
            raise ValueError()

        return {
            RED: math.floor(len([_ for _ in numbers[-n:] if _ in cls.number_mapping[RED]]) / n * 100),
            BLACK: math.floor(len([_ for _ in numbers[-n:] if _ in cls.number_mapping[BLACK]]) / n * 100),
            EVEN: math.floor(len([_ for _ in numbers[-n:] if _ % 2 == 0]) / n * 100),
            ODD: math.floor(len([_ for _ in numbers[-n:] if _ % 2 == 1]) / n * 100),
            LOW: math.floor(len([_ for _ in numbers[-n:] if 0 < _ <= 18]) / n * 100),
            HIGH: math.floor(len([_ for _ in numbers[-n:] if _ > 18]) / n * 100)
        }

    @classmethod
    @cachetools.func.lfu_cache()
    def get_bet_types(cls) -> List[str]:
        bet_types = [RED, BLACK, EVEN, ODD, LOW, HIGH, FOUR]
        bet_types.extend([f'{STRAIGHT}_{x}' for x in range(37)])
        bet_types.extend([f'{SPLIT}_{x[0]}_{x[1]}' for x in cls.number_mapping[SPLIT]])
        bet_types.extend([f'{STREET}_{x[0]}_{x[1]}_{x[2]}' for x in cls.number_mapping[STREET]])
        bet_types.extend([f'{CORNER}_{x[0]}_{x[1]}_{x[2]}_{x[3]}' for x in cls.number_mapping[CORNER]])
        bet_types.extend([f'{LINE}_{x[0]}_{x[1]}_{x[2]}_{x[3]}_{x[4]}_{x[5]}' for x in cls.number_mapping[LINE]])
        bet_types.extend([f'{COLUMN}_bottom', f'{COLUMN}_center', f'{COLUMN}_top'])
        bet_types.extend([f'{DOZEN}_first', f'{DOZEN}_second', f'{DOZEN}_third'])

        return bet_types

    @classmethod
    @cachetools.func.lfu_cache()
    def get_win_types_all(cls) -> dict:
        return {n: cls.get_win_types(n) for n in (x for x in range(37))}

    @classmethod
    def get_win_types(cls, number: int) -> List[str]:
        win_types = [f'{STRAIGHT}_{number}', 'any']

        if number == 0:
            win_types.append(FOUR)

        elif number != 0:
            win_types.append(RED if number in cls.number_mapping[RED] else BLACK)
            win_types.append(EVEN if number % 2 == 0 else ODD)
            win_types.append(LOW if 1 <= number <= 18 else HIGH)

            win_types.append(
                f'{COLUMN}_bottom' if number % 3 == 1 else
                f'{COLUMN}_center' if number % 2 == 2 else
                f'{COLUMN}_top'
            )

            win_types.append(
                f'{DOZEN}_first' if 1 <= number <= 12 else
                f'{DOZEN}_second' if 13 <= number <= 24 else
                f'{DOZEN}_third'
            )

            if number in cls.number_mapping[FOUR]:
                win_types.append(FOUR)

            for x in cls.number_mapping[SPLIT]:
                if number in x:
                    win_types.append(f'{SPLIT}_{x[0]}_{x[1]}')

            for x in cls.number_mapping[STREET]:
                if number in x:
                    win_types.append(f'{STREET}_{x[0]}_{x[1]}_{x[2]}')

            for x in cls.number_mapping[CORNER]:
                if number in x:
                    win_types.append(f'{CORNER}_{x[0]}_{x[1]}_{x[2]}_{x[3]}')

            for x in cls.number_mapping[LINE]:
                if number in x:
                    win_types.append(f'{LINE}_{x[0]}_{x[1]}_{x[2]}_{x[3]}_{x[4]}_{x[5]}')

        return win_types

    @classmethod
    def validate_bet_type(cls, bet_type_name: str) -> str:
        if bet_type_name == 'any':
            return bet_type_name

        if bet_type_name not in cls.get_bet_types():
            raise ValueError(f'invalid model type - {bet_type_name}')

        return bet_type_name
