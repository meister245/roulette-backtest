from tabulate import tabulate


class DisplayModel(object):
    def __init__(self):
        pass

    @classmethod
    def get_result_summary(cls, results):
        balance_start = results[0]['balance_start']
        balance_close = results[-1]['balance_close']
        win_ratio = cls.get_win_ratio(results)

        summary = {
            'cycles': len(results),
            'balance': '{} / {}'.format(balance_start, balance_close),
            'balance_start': balance_start,
            'balance_close': balance_close,
            'largest_bet': max([x['bet_amount'] for x in results]),
            'profit_total': round(balance_close - balance_start, 2),
            'profit_ratio': round(balance_close / balance_start - 1, 3) * 100,
            'win_ratio': round(win_ratio, 3)
        }

        return summary

    @staticmethod
    def get_result_summary_aggregated(summaries):
        avg_profit_ratio = round(sum([x['profit_ratio'] for x in summaries]) / len(summaries), 3)
        avg_profit_total = round(sum([x['profit_total'] for x in summaries]) / len(summaries), 2)
        avg_win_ratio = round(sum([x['win_ratio'] for x in summaries]) / len(summaries), 3)
        avg_cycles = round(sum([x['cycles'] for x in summaries]) / len(summaries), 2)

        aggregated_summary = {
            'total_games': len(summaries),
            'avg_cycles': avg_cycles,
            'avg_profit_ratio': avg_profit_ratio,
            'avg_profit_total': avg_profit_total,
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
            if isinstance(x['bet_result'], list):
                b_row = []

                for r in x['bet_result']:
                    b_row.append('{} - {} - {}'.format('W' if r['win'] else 'L', r['bet_amount'], r['bet_type']))

                b_row = '\n'.join(b_row)

            else:
                b_row = '---'

            if x['status'] is None:
                t_row = [x['balance_close'], b_row, '---', x['number'], x['status'], '---']

            else:
                t_row = [x['balance_close'], b_row, x['bet_amount'], x['number'], x['status'], x['profit']]

            data.append(t_row)

        t = cls.tabulate_data(headers, data)
        print('\n' + t + '\n')

    @classmethod
    def print_result_summary(cls, results):
        summary = cls.get_result_summary(results)

        headers = [
            'Total Games', 'Balance (S/C)', 'Total Profit', 'Win Ratio (%)', 'Largest Bet',
        ]

        data = [[
            summary['cycles'], summary['balance'], summary['profit_total'], summary['win_ratio'], summary['largest_bet']
        ]]

        t = cls.tabulate_data(headers, data, table_format='simple')
        print('\n' + t)

    @classmethod
    def print_result_summary_aggregated(cls, summaries):
        aggr_summary = cls.get_result_summary_aggregated(summaries)

        headers = [
            'Total Games', 'Avg. Win Ratio (%)', 'Avg. Profit Total', 'Avg. Profit Ratio (%)', 'Avg. Cycle Count'
        ]

        data = [[
            aggr_summary['total_games'], aggr_summary['avg_win_ratio'], aggr_summary['avg_profit_total'],
            aggr_summary['avg_profit_ratio'], aggr_summary['avg_cycles']
        ]]

        t = cls.tabulate_data(headers, data, table_format='simple')
        print('\n' + t + '\n')

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
