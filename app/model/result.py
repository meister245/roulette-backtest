from typing import List

from tabulate import tabulate

DOZEN_TOP, DOZEN_MIDDLE, DOZEN_BOTTOM = 'dozen_top', 'dozen_center', 'dozen_bottom'
RED, BLACK, EVEN, ODD, HALF_LEFT, HALF_RIGHT = 'red', 'black', 'even', 'odd', 'half_left', 'half_right'
COLUMN_LEFT, COLUMN_MIDDLE, COLUMN_RIGHT = 'column_left', 'column_middle', 'column_right'
LINE, CORNER, FOUR, STREET, SPLIT, STRAIGHT = 'line', 'corner', 'four', 'street', 'split', 'straight'
TIER, ORPHELINS, VOISONS, ZERO = 'tier', 'orphelins', 'voisons', 'zero'


class ResultModel(object):
    __slots__ = ['results']

    bet_mapping = {
        DOZEN_TOP: [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
        DOZEN_MIDDLE: [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
        DOZEN_BOTTOM: [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
        RED: [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 27, 30, 32, 34, 36],
        BLACK: [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35],
        TIER: [27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33],
        ORPHELINS: [17, 34, 6, 1, 20, 14, 31, 9],
        VOISONS: [22, 18, 29, 7, 28, 19, 4, 21, 2, 25],
        ZERO: [12, 35, 3, 26, 0, 32, 15]
    }

    payout_mapping = {
        RED: 1, BLACK: 1, EVEN: 1, ODD: 1, HALF_LEFT: 1, HALF_RIGHT: 1, COLUMN_LEFT: 2,
        COLUMN_MIDDLE: 2, COLUMN_RIGHT: 2, DOZEN_TOP: 2, DOZEN_MIDDLE: 2, DOZEN_BOTTOM: 2,
        LINE: 5, CORNER: 11, FOUR: 11, STREET: 17, STRAIGHT: 35
    }

    def __init__(self):
        self.results = []

    def get_result(self, number: int, bets: dict, balance: float) -> dict:
        win_types = self.get_win_types(number)
        profit = self.calculate_profit(bets, win_types)
        status = 'null' if profit == 0 else 'lose' if profit <= 0 else 'win'

        result = {
            'number': number,
            'balance_start': balance,
            'balance_close': round(balance + profit, 2),
            'bet_amount': sum([x for x in bets.values()]),
            'bet_result': ['{} - {} - {}'.format(round(v, 2), 'W' if k in win_types else 'L', k) for k, v in
                           bets.items()],
            'profit': profit,
            'status': status,
            'win_types': win_types,
        }

        self.results.append(result)

        return result

    def get_result_summary(self):
        balance_start = self.results[0]['balance_start']
        balance_close = self.results[-1]['balance_close']
        longest_win, longest_lose = self.eval_longest_streak(self.results)
        win_ratio = len([x for x in self.results if x['status'] == 'win']) / len(self.results) * 100

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
            'profit_ratio': round(balance_close / balance_start * 100, 2),
            'win_ratio': round(win_ratio, 2)
        }

        return summary

    @classmethod
    def calculate_profit(cls, bets: dict, win_bet_types: List[str]) -> float:
        profit = 0 - sum([x for x in bets.values()])

        for bet_type, amount in bets.items():
            if bet_type in win_bet_types:
                profit += amount * cls.payout_mapping[bet_type]
                profit += amount

        return round(profit, 2)

    def print_result_summary(self):
        summary = self.get_result_summary()

        headers = [
            'Balance (S/C)', 'Total Profit', 'Streaks (W/L)', 'Win Ratio (%)', 'Largest Bet',
        ]

        data = [[
            summary['balance'], summary['profit_total'], summary['longest_streaks'],
            summary['win_ratio'], summary['largest_bet']
        ]]

        print(self.tabulate_data(headers, data))

    def print_result_details(self):
        headers = [
            'Balance', 'Bet Result', 'Bet Amount', 'Number', 'Result', 'Profit'
        ]

        data = []

        for x in self.results:
            data.append([
                x['balance_close'], '\n'.join(x['bet_result']), x['bet_amount'], x['number'], x['status'], x['profit']
            ])

        print(self.tabulate_data(headers, data))

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
            win_bet_types.append(HALF_LEFT)

        elif 19 <= number <= 36:
            win_bet_types.append(HALF_RIGHT)

        if number in cls.bet_mapping[DOZEN_TOP]:
            win_bet_types.append(DOZEN_TOP)

        elif number in cls.bet_mapping[DOZEN_MIDDLE]:
            win_bet_types.append(DOZEN_MIDDLE)

        elif number in cls.bet_mapping[DOZEN_BOTTOM]:
            win_bet_types.append(DOZEN_BOTTOM)

        if 1 <= number <= 12:
            win_bet_types.append(COLUMN_LEFT)

        elif 13 <= number <= 22:
            win_bet_types.append(COLUMN_MIDDLE)

        elif 23 <= number <= 36:
            win_bet_types.append(COLUMN_RIGHT)

        if number in cls.bet_mapping[TIER]:
            win_bet_types.append(TIER)

        elif number in cls.bet_mapping[ORPHELINS]:
            win_bet_types.append(ORPHELINS)

        elif number in cls.bet_mapping[VOISONS]:
            win_bet_types.append(VOISONS)

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
