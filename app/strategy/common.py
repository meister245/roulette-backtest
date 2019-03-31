from random import randint
from tabulate import tabulate


class StrategyCommon(object):
    def __init__(self):
        pass

    @staticmethod
    def get_next_number(idx, backtest=None):
        return randint(0, 36) if backtest is None else backtest[idx]

    @staticmethod
    def get_aggregated_result_summary(results):
        avg_winning_streak = round(sum([x['longest_winning_streak'] for x in results]) / len(results), 2)
        avg_losing_streak = round(sum([x['longest_losing_streak'] for x in results]) / len(results), 2)

        aggregated_summary = {
            'total_games': len(results),
            'avg_win_ratio': round(sum([x['win_ratio'] for x in results]) / len(results), 2),
            'avg_streak': '{} / {}'.format(avg_winning_streak, avg_losing_streak),
        }

        return aggregated_summary

    def get_result_summary(self, results):
        longest_win, longest_lose = self.eval_longest_streak(results)
        start_balance = results[0]['balance']
        close_balance = results[-1]['balance']

        summary = {
            'cycles': len(results),
            'balance': '{} / {}'.format(start_balance, close_balance),
            'balance_starting': start_balance,
            'balance_closing': close_balance,
            'largest_bet': max([x['bet_amount'] for x in results]),
            'total_profit': round(close_balance - start_balance, 2),
            'win_ratio': round(len([x for x in results if x['status'] == 'win']) / len(results), 2) * 100,
            'longest_streaks': '{} / {}'.format(longest_win, longest_lose),
            'longest_winning_streak': longest_win,
            'longest_losing_streak': longest_lose,
        }

        return summary

    def print_aggregated_result_summary(self, results):
        aggr_summary = self.get_aggregated_result_summary(results)

        t_headers = [
            'Total Games', 'Average Win Ratio', 'Average Streaks (W / L)', 'Average Profit Ratio'
        ]

        t_data = [[
            aggr_summary['total_games'], aggr_summary['avg_win_ratio'], aggr_summary['avg_streak']
        ]]

        t = tabulate(t_data, t_headers, tablefmt='grid')

        print(t)

    def print_result_summary(self, results):
        summary = self.get_result_summary(results)

        t_headers = [
            'Balance (S/C)', 'Total Profit', 'Streaks (W/L)', 'Win Ratio', 'Largest Bet',
        ]

        t_data = [[
            summary['balance'], summary['total_profit'], summary['longest_streaks'],
            summary['win_ratio'], summary['largest_bet']
        ]]

        t = tabulate(t_data, t_headers, tablefmt='grid')

        print(t)

    @staticmethod
    def print_result_details(results):
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
