from random import randint

from app.model.result import ResultModel

from tabulate import tabulate


class StrategyCommon(object):
    def __init__(self, backtest):
        self.backtest = backtest

    def run_single(self, bets, **kwargs):
        store = ResultModel()

        original_bets, current_bets = bets, bets

        balance = kwargs['balance']
        cycles = self.get_cycles(kwargs['cycles'])

        if current_bets is None or sum(current_bets.values()) <= 0:
            exit('invalid bet - {}'.format(bets))

        for idx, x in enumerate(range(cycles)):
            if sum([v for v in current_bets.values()]) > balance:
                break

            number = self.get_next_number(idx)
            result = store.get_result(number, current_bets, balance)

            balance = result['balance_close']
            current_bets = self.set_new_bets(result['status'], current_bets, original_bets, **kwargs)

        return store

    def run_aggregate(self, bets, **kwargs):
        aggregate_results = []

        for x in range(500):
            store = self.run_single(bets, **kwargs)
            result_summary = store.get_result_summary()
            aggregate_results.append(result_summary)

        return aggregate_results

    @staticmethod
    def tabulate_data(headers, data, table_format='grid'):
        return tabulate(data, headers, tablefmt=table_format)

    @staticmethod
    def get_aggregated_result_summary(results):
        avg_winning_streak = round(sum([x['longest_win_streak'] for x in results]) / len(results), 2)
        avg_losing_streak = round(sum([x['longest_lose_streak'] for x in results]) / len(results), 2)

        aggregated_summary = {
            'total_games': len(results),
            'avg_win_ratio': round(sum([x['win_ratio'] for x in results]) / len(results), 2),
            'avg_streak': '{} / {}'.format(avg_winning_streak, avg_losing_streak),
            'avg_profit_ratio': round(sum([x['profit_ratio'] for x in results]) / len(results), 2)
        }

        return aggregated_summary

    @classmethod
    def print_aggregated_result_summary(cls, aggr_summary):
        headers = [
            'Total Games', 'Avg. Win Ratio (%)', 'Average Streaks (W/L)', 'Avg. Profit Ratio (%)'
        ]

        data = [[
            aggr_summary['total_games'], aggr_summary['avg_win_ratio'], aggr_summary['avg_streak'],
            aggr_summary['avg_profit_ratio']
        ]]

        print(cls.tabulate_data(headers, data))

    def get_next_number(self, idx):
        return self.get_random_number() if self.backtest is None else self.backtest[idx]

    def get_cycles(self, cycles):
        return len(self.backtest) if self.backtest is not None and len(self.backtest) < cycles else cycles

    @staticmethod
    def get_random_number():
        return randint(0, 36)

    @staticmethod
    def set_new_bets(status, current_bets, original_bets, **kwargs):
        raise NotImplementedError()
