import re
from typing import List

from tabulate import tabulate

TIER, ORPHELINS, VOISONS, ZERO = 'tier', 'orphelins', 'voisons', 'zero'
RED, BLACK, EVEN, ODD, LOW, HIGH = 'red', 'black', 'even', 'odd', 'low', 'high'
COLUMN_TOP, COLUMN_MIDDLE, COLUMN_BOTTOM = 'column_top', 'column_center', 'column_bottom'
DOZEN_LEFT, DOZEN_MIDDLE, DOZEN_RIGHT = 'dozen_left', 'dozen_middle', 'dozen_right'
LINE, CORNER, FOUR, STREET, SPLIT, STRAIGHT = 'line', 'corner', 'four', 'street', 'split', 'straight'


class ResultModel(object):
    __slots__ = ['results']

    bet_mapping = {
        COLUMN_TOP: [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
        COLUMN_MIDDLE: [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
        COLUMN_BOTTOM: [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
        RED: [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 27, 30, 32, 34, 36],
        BLACK: [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35],
        TIER: [27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33],
        ORPHELINS: [17, 34, 6, 1, 20, 14, 31, 9],
        VOISONS: [22, 18, 29, 7, 28, 19, 4, 21, 2, 25],
        ZERO: [12, 35, 3, 26, 0, 32, 15],

        FOUR: [(0, 1, 2, 3)],

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

    result_mapping = {
        'win': 'W', 'lose': 'L', 'win_idle': 'WI', 'lose_idle': 'LI', 'null': 'N', 'null_idle': 'NI'
    }

    def __init__(self):
        self.results = []

    def get_result(self, number: int, bets: dict, balance: float, idle: bool) -> dict:
        win_types = self.get_win_types(number)

        bet_amount = sum([x for x in bets.values()])
        bet_result = ['{} - {} - {}'.format(round(v, 2), 'W' if k in win_types else 'L', k) for k, v in bets.items()]

        profit = self.calculate_profit(bets, win_types)
        status = self.get_result_status(profit, idle)

        result = {
            'number': number,
            'balance_start': balance,
            'balance_close': balance if idle else round(balance + profit, 2),
            'bet_amount': bet_amount,
            'bet_result': bet_result,
            'profit': profit,
            'status': status,
            'win_types': win_types
        }

        self.results.append(result)

        return result

    @staticmethod
    def get_result_status(profit, idle):
        if profit == 0:
            return 'null_idle' if idle else 'null'

        elif profit < 0:
            return 'lose_idle' if idle else 'lose'

        else:
            return 'win_idle' if idle else 'win'

    def get_result_summary(self):
        balance_start = self.results[0]['balance_start']
        balance_close = self.results[-1]['balance_close']
        longest_win, longest_lose = self.eval_longest_streak(self.results)
        win_ratio = self.get_win_ratio()

        summary = {
            'cycles': len(self.results),
            'balance': '{} / {}'.format(balance_start, balance_close),
            'balance_start': balance_start,
            'balance_close': balance_close,
            'largest_bet': max([x['bet_amount'] for x in self.results]),
            'longest_streaks': '{} / {}'.format(longest_win, longest_lose),
            'longest_win_streak': longest_win,
            'longest_lose_streak': longest_lose,
            'profit_total': round(balance_close - balance_start, 2),
            'profit_ratio': round(balance_close / balance_start - 1, 2) * 100,
            'win_ratio': round(win_ratio, 2)
        }

        return summary

    @classmethod
    def calculate_profit(cls, bets: dict, win_bet_types: List[str]) -> float:
        profit = 0 - sum([x for x in bets.values()])

        for bet_type, amount in bets.items():
            if bet_type in win_bet_types:
                name = bet_type.split('_', 1).pop(0)

                if name in ['street', 'line', 'corner', 'split', 'four']:
                    profit += amount * cls.payout_mapping[name]

                else:
                    profit += amount * cls.payout_mapping[bet_type]

                profit += amount

        return round(profit, 2)

    def print_result_summary(self):
        summary = self.get_result_summary()

        headers = [
            'Total Games', 'Balance (S/C)', 'Total Profit', 'Streaks (W/L)', 'Win Ratio (%)', 'Largest Bet',
        ]

        data = [[
            summary['cycles'], summary['balance'], summary['profit_total'], summary['longest_streaks'],
            summary['win_ratio'], summary['largest_bet']
        ]]

        print(self.tabulate_data(headers, data))

    def print_result_details(self):
        headers = [
            'Balance', 'Bet Result', 'Bet Amount', 'Number', 'Result', 'Profit'
        ]

        data = []

        for x in self.results:
            if 'idle' in x['status']:
                x['profit'] = 0
                x['bet_amount'] = 0
                x['bet_result'] = [re.sub(r'[0-9]{,5}\.[0-9]{,2}', '0', x) for x in x['bet_result']]

            data.append([
                x['balance_close'], '\n'.join(x['bet_result']), x['bet_amount'], x['number'], x['status'], x['profit']
            ])

        print(self.tabulate_data(headers, data))

    def get_result_pattern(self):
        pattern = []

        for x in self.results:
            pattern.append(self.result_mapping[x['status']])

        return tuple(pattern)

    def get_win_ratio(self):
        win_results_count = len([x for x in self.results if x['status'] == 'win'])
        all_results_count = len([x for x in self.results if x['status'] in ('win', 'lose', 'null')])

        if all_results_count == 0:
            return 0
        else:
            return win_results_count / all_results_count * 100

    @classmethod
    def get_win_types(cls, number: int) -> List[str]:
        win_bet_types = ['{}_{}'.format(STRAIGHT, number)]

        if number in cls.bet_mapping[RED]:
            win_bet_types.append(RED)

        elif number in cls.bet_mapping[BLACK]:
            win_bet_types.append(BLACK)

        if number != 0 and number % 2 == 0:
            win_bet_types.append(EVEN)

        elif number % 2 == 1:
            win_bet_types.append(ODD)

        if 1 <= number <= 18:
            win_bet_types.append(LOW)

        elif 19 <= number <= 36:
            win_bet_types.append(HIGH)

        if number in cls.bet_mapping[COLUMN_TOP]:
            win_bet_types.append(COLUMN_TOP)

        elif number in cls.bet_mapping[COLUMN_MIDDLE]:
            win_bet_types.append(COLUMN_MIDDLE)

        elif number in cls.bet_mapping[COLUMN_BOTTOM]:
            win_bet_types.append(COLUMN_BOTTOM)

        if 1 <= number <= 12:
            win_bet_types.append(DOZEN_LEFT)

        elif 13 <= number <= 22:
            win_bet_types.append(DOZEN_MIDDLE)

        elif 23 <= number <= 36:
            win_bet_types.append(DOZEN_RIGHT)

        if number in cls.bet_mapping[TIER]:
            win_bet_types.append(TIER)

        elif number in cls.bet_mapping[ORPHELINS]:
            win_bet_types.append(ORPHELINS)

        elif number in cls.bet_mapping[VOISONS]:
            win_bet_types.append(VOISONS)

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

        return win_bet_types

    @staticmethod
    def tabulate_data(headers, data, table_format='grid'):
        return tabulate(data, headers, tablefmt=table_format)

    @staticmethod
    def eval_longest_streak(results):
        longest_win = 0
        longest_losing = 0

        t_win = 0
        t_lose = 0

        for x in results:
            if x['status'] == 'win':
                t_win += 1

                if t_lose >= longest_losing:
                    longest_losing = t_lose

                t_lose = 0

            elif x['status'] == 'lose':
                t_lose += 1

                if t_win >= longest_win:
                    longest_win = t_win

                t_win = 0

        return longest_win, longest_losing
