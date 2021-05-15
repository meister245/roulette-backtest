import tabulate


class DisplayController:
    @staticmethod
    def get_result_details(results):
        t_data = []

        for x in results:
            bets = [f"{'W' if r['win'] else 'N' if r['win'] is None else 'F'} - {r['size']} - {','.join(r['type'])}"
                    for r in x['results']]

            bets = '---' if len(bets) == 0 else '\n'.join(bets)

            profit = sum([p['profit'] for p in x['results']])

            size = sum([s['size'] for s in x['results']])
            size = size if size > 0 else '---'

            status = 'W' if profit > 0 else 'L' if profit < 0 else '---'

            t_data.append([x['balance'], bets, size, x['number'], status, profit])

        return t_data

    @classmethod
    def get_result_summary_rng(cls, results):
        balance_start = results[0]['balance']
        balance_close = results[-1]['balance']
        win_ratio = cls.get_win_ratio(results)

        summary = {
            'spins': len(results),
            'balance': f'{balance_start} / {balance_close}',
            'balance_start': balance_start,
            'balance_close': balance_close,
            'profit_total': round(balance_close - balance_start, 2),
            'profit_ratio': round(balance_close / balance_start - 1, 3) * 100,
            'win_ratio': round(win_ratio, 3)
        }

        return summary

    @classmethod
    def get_result_summary_backtest(cls, results):
        t_data = []

        for filename, data in results.items():
            total_bets = len([x for x in data if len(x['results']) > 0])
            total_profit = data[-1]['balance'] - data[0]['balance']
            win_ratio = round(cls.get_win_ratio(data), 2)

            t_data.append([filename, len(data), total_bets, total_profit, win_ratio])

        return t_data

    @classmethod
    def print_result_details(cls, bet_results):
        t_headers = ['Balance', 'Bets', 'Bet Amount', 'Number', 'Status', 'Profit']
        t_data = cls.get_result_details(bet_results)

        t = cls.tabulate_data(t_headers, t_data)
        print(t + '\n')

    @classmethod
    def print_result_summary_rng(cls, bet_objects):
        summary = cls.get_result_summary_rng(bet_objects)

        t_headers = [
            'Total Spins', 'Balance (S/C)', 'Total Profit', 'Profit Ratio (%)',
        ]

        t_data = [[
            summary['spins'], summary['balance'], summary['profit_total'], summary['profit_ratio']
        ]]

        t = cls.tabulate_data(t_headers, t_data, table_format='simple')
        print('\n' + t + '\n')

    @classmethod
    def print_result_summary_backtest(cls, results):
        t_headers = ['Filename', 'Total Spins', 'Total Bets', 'Total Profit', 'Win Ratio (%)']
        t_data = cls.get_result_summary_backtest(results)

        t = cls.tabulate_data(t_headers, t_data)
        print(t + '\n')

    @staticmethod
    def get_win_ratio(results):
        results_total = []

        for b in results:
            if len(b['results']) != 0:
                results_total.extend(b['results'])

        win_results_count = len([k for k in results_total if k['win']])

        if len(results_total) == 0:
            return 0

        else:
            return win_results_count / len(results_total) * 100

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
        return tabulate.tabulate(data, headers, tablefmt=table_format)
