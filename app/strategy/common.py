from random import randint

from app.model.result import ResultModel

from tabulate import tabulate


class StrategyCommon(object):
    switch_idle_start = True

    strategies = ('martingale', 'paroli', 'dalembert', 'fibonacci', 'james_bond', 'romanosky', 'kavouras')

    def __init__(self, backtest):
        self.backtest = backtest

    def run_single(self, bets, **kwargs):
        store = self.get_result_model()

        if not isinstance(bets, dict):
            exit('invalid bet structure for strategy')

        original_bets, current_bets = bets, bets

        balance = kwargs['balance']
        cycles = self.get_cycles(kwargs['cycles'])
        idle_start, idle_lose = kwargs.get('idle_start', 0), kwargs.get('idle_lose', 0)

        if current_bets is None or sum(current_bets.values()) <= 0:
            exit('invalid bet - {}'.format(bets))

        for idx, x in enumerate(range(cycles)):
            if sum([v for v in current_bets.values()]) > balance:
                break

            number = self.get_next_number(idx)
            idle = self.get_idle_status(store, idle_start, idle_lose)
            result = store.get_result(number, current_bets, balance, idle)

            balance = result['balance_close']
            current_bets = self.set_new_bets(result['status'], current_bets, original_bets, **kwargs)

        return store

    @classmethod
    def get_idle_status(cls, store, idle_start, idle_lose):
        if idle_start > 0 and cls.switch_idle_start:
            if len(store.results) < idle_start:
                return True

            lose_consecutive = 0

            for x in store.results:
                if x['status'] in ['lose_idle', 'lose']:
                    lose_consecutive += 1
                else:
                    lose_consecutive -= lose_consecutive

                if lose_consecutive > idle_start:
                    break

            if lose_consecutive < idle_start:
                return True

            cls.switch_idle_start = False

        if idle_lose > 0:
            last_n_results = [x for x in store.results[-idle_lose:] if x['status'] in ['lose_idle', 'lose']]

            if len(last_n_results) < idle_lose:
                return True

        return False

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
        avg_profit_ratio = round(sum([x['profit_ratio'] for x in results]) / len(results), 2)
        avg_profit_total = round(sum([x['profit_total'] for x in results]) / len(results), 2)
        avg_losing_streak = round(sum([x['longest_lose_streak'] for x in results]) / len(results), 2)
        avg_winning_streak = round(sum([x['longest_win_streak'] for x in results]) / len(results), 2)
        avg_win_ratio = round(sum([x['win_ratio'] for x in results]) / len(results), 2)

        aggregated_summary = {
            'total_games': len(results),
            'avg_win_ratio': avg_win_ratio,
            'avg_streak': '{} / {}'.format(avg_winning_streak, avg_losing_streak),
            'avg_profit_ratio': avg_profit_ratio,
            'avg_profit_total': avg_profit_total
        }

        return aggregated_summary

    def get_cycles(self, cycles):
        return len(self.backtest) if self.backtest is not None and len(self.backtest) < cycles else cycles

    def get_next_number(self, idx):
        return self.get_random_number() if self.backtest is None else self.backtest[idx]

    @staticmethod
    def get_random_number():
        return randint(0, 36)

    @staticmethod
    def get_result_model():
        return ResultModel()

    @classmethod
    def print_aggregated_result_summary(cls, aggr_summary):
        headers = [
            'Total Games', 'Avg. Win Ratio (%)', 'Avg. Streaks (W/L)', 'Avg. Profit Ratio (%)', 'Avg. Profit'
        ]

        data = [[
            aggr_summary['total_games'], aggr_summary['avg_win_ratio'], aggr_summary['avg_streak'],
            aggr_summary['avg_profit_ratio'], aggr_summary['avg_profit_total']
        ]]

        print(cls.tabulate_data(headers, data))

    @staticmethod
    def set_new_bets(status, current_bets, original_bets, **kwargs):
        raise NotImplementedError()
