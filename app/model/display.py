import re

from tabulate import tabulate


class DisplayModel(object):
    def __init__(self):
        pass

    @classmethod
    def get_result_summary(cls, results):
        balance_start = results[0]['balance_start']
        balance_close = results[-1]['balance_close']
        longest_win, longest_lose = cls.get_longest_streak(results)
        win_ratio = cls.get_win_ratio(results)

        summary = {
            'cycles': len(results),
            'balance': '{} / {}'.format(balance_start, balance_close),
            'balance_start': balance_start,
            'balance_close': balance_close,
            'largest_bet': max([x['bet_amount'] for x in results]),
            'longest_streaks': '{} / {}'.format(longest_win, longest_lose),
            'longest_win_streak': longest_win,
            'longest_lose_streak': longest_lose,
            'profit_total': round(balance_close - balance_start, 2),
            'profit_ratio': round(balance_close / balance_start - 1, 2) * 100,
            'win_ratio': round(win_ratio, 2)
        }

        return summary

    @staticmethod
    def get_result_summary_aggregated(summaries):
        avg_profit_ratio = round(sum([x['profit_ratio'] for x in summaries]) / len(summaries), 2)
        avg_profit_total = round(sum([x['profit_total'] for x in summaries]) / len(summaries), 2)
        avg_losing_streak = round(sum([x['longest_lose_streak'] for x in summaries]) / len(summaries), 2)
        avg_winning_streak = round(sum([x['longest_win_streak'] for x in summaries]) / len(summaries), 2)
        avg_win_ratio = round(sum([x['win_ratio'] for x in summaries]) / len(summaries), 2)
        avg_cycles = ''

        aggregated_summary = {
            'total_games': len(summaries),
            'avg_cycles': avg_cycles,
            'avg_profit_ratio': avg_profit_ratio,
            'avg_profit_total': avg_profit_total,
            'avg_streak': '{} / {}'.format(avg_winning_streak, avg_losing_streak),
            'avg_win_ratio': avg_win_ratio
        }

        return aggregated_summary

    @classmethod
    def print_result_details(cls, results):
        headers = [
            'Balance', 'Bet Result', 'Bet Amount', 'Number', 'Result', 'Profit'
        ]

        data = []

        for x in results:
            if 'idle' in x['status']:
                x['profit'] = 0
                x['bet_amount'] = 0
                x['bet_result'] = [re.sub(r'[0-9]{,5}\.[0-9]{,2}', '0', x) for x in x['bet_result']]

            data.append([
                x['balance_close'], '\n'.join(x['bet_result']), x['bet_amount'], x['number'], x['status'], x['profit']
            ])

        print(cls.tabulate_data(headers, data))

    @classmethod
    def print_result_summary_aggregated(cls, summaries):
        aggr_summary = cls.get_result_summary_aggregated(summaries)

        headers = [
            'Total Games', 'Avg. Win Ratio (%)', 'Avg. Streaks (W/L)', 'Avg. Profit Ratio (%)', 'Avg. Profit'
        ]

        data = [[
            aggr_summary['total_games'], aggr_summary['avg_win_ratio'], aggr_summary['avg_streak'],
            aggr_summary['avg_profit_ratio'], aggr_summary['avg_profit_total']
        ]]

        print(cls.tabulate_data(headers, data))

    @classmethod
    def print_result_summary(cls, results):
        summary = cls.get_result_summary(results)

        headers = [
            'Total Games', 'Balance (S/C)', 'Total Profit', 'Streaks (W/L)', 'Win Ratio (%)', 'Largest Bet',
        ]

        data = [[
            summary['cycles'], summary['balance'], summary['profit_total'], summary['longest_streaks'],
            summary['win_ratio'], summary['largest_bet']
        ]]

        print(cls.tabulate_data(headers, data))

    @staticmethod
    def get_win_ratio(results):
        win_results_count = len([x for x in results if x['status'] == 'win'])
        all_results_count = len([x for x in results if x['status'] in ('win', 'lose', 'null')])

        if all_results_count == 0:
            return 0
        else:
            return win_results_count / all_results_count * 100

    @staticmethod
    def get_longest_streak(results):
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

    @staticmethod
    def tabulate_data(headers, data, table_format='grid'):
        return tabulate(data, headers, tablefmt=table_format)
