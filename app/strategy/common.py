from random import randint
from tabulate import tabulate


class StrategyCommon(object):
    def __init__(self):
        pass

    def get_next_number(self, idx, backtest=None):
        return randint(0, 36) if backtest is None else backtest[idx]

    def get_result_summary(self, results):
        longest_win, longest_lose = self.eval_longest_streak(results)

        summary = {
            'cycles': len(results),
            'starting_balance': results[0]['balance'],
            'closing_balance': results[-1]['balance'],
            'largest_bet': max([x['bet_amount'] for x in results]),
            'longest_winning_streak': longest_win,
            'longest_losing_streak': longest_lose
        }

        return summary

    def print_result_summary(self, results):
        summary = self.get_result_summary(results)

        t_headers = [
            'Starting Balance', 'Closing Balance', 'Largest Bet', 'Longest Winning Streak',
            'Longest Losing Streak'
        ]

        t_data = [[
            summary['starting_balance'], summary['closing_balance'], summary['largest_bet'],
            summary['longest_winning_streak'], summary['longest_losing_streak']
        ]]

        t = tabulate(t_data, t_headers, tablefmt='grid')

        print(t)

    def print_result_details(self, results):
        t_headers = [
            'Balance', 'Bet Type', 'Bet Amount', 'Number', 'Result', 'Profit'
        ]

        t_data = []

        for x in results:
            t_data.append([
                x['balance'], x['bet_type'], x['bet_amount'], x['number'], x['status'], x['win']
            ])

        t = tabulate(t_data, t_headers, tablefmt='grid')

        print(t)

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

            elif x['status'] == 'lost':
                t_lose += 1

                if t_win >= longest_win:
                    longest_win = t_win

                t_win = 0

        return longest_win, longest_losing
