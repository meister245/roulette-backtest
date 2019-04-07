from random import randint

from app.model.result import ResultModel
from app.model.display import DisplayModel

from tabulate import tabulate


class StrategyCommon(object):
    __slots__ = ['backtest']

    display = DisplayModel()

    switch_idle_start = True

    strategies = ('martingale', 'paroli', 'dalembert', 'fibonacci', 'james_bond', 'romanosky', 'kavouras')

    def __init__(self, backtest):
        self.backtest = backtest

    def run_single(self, bets, **kwargs):
        if not isinstance(bets, dict):
            exit('invalid bet structure for strategy')

        if sum(bets.values()) <= 0:
            exit('invalid bet amount - {}'.format(bets))

        cycles, target_profit = kwargs.pop('cycles', None), kwargs.pop('target_profit', None)

        if cycles is None and target_profit is None:
            exit('cycles OR target_profit parameter required')

        elif cycles is not None and target_profit is not None:
            exit('simulation does not support fixed cycles AND fixed target_profit')

        if isinstance(cycles, (int, float)):
            cycles = len(self.backtest) if self.backtest is not None and len(self.backtest) < cycles else cycles
            return self.run_simulation_fixed_cycles(bets, cycles, **kwargs)

        elif isinstance(target_profit, (int, float)):
            return self.run_simulation_fixed_profit(bets, target_profit, **kwargs)

        else:
            exit('invalid parameters')

    def run_simulation_fixed_cycles(cls, bets, cycles, **kwargs):
        store = cls.get_result_model()
        balance = kwargs.get('balance', 1000.0)

        original_bets, current_bets = bets, bets

        for x in range(cycles):
            if sum([v for v in current_bets.values()]) > balance:
                break

            number = cls.get_next_number(x)
            idle = cls.get_idle_status(store, **kwargs)
            result = store.get_result(number, current_bets, balance, idle)

            balance = result['balance_close']
            current_bets = cls.set_new_bets(result['status'], current_bets, original_bets, **kwargs)

        return store

    def run_simulation_fixed_profit(cls, bets, target_profit, **kwargs):
        store = cls.get_result_model()
        balance = kwargs.get('balance', 1000.0)
        target_balance = balance + target_profit

        original_bets, current_bets = bets, bets

        cycle_count = 0

        while True:
            if sum([v for v in current_bets.values()]) > balance:
                break

            number = cls.get_next_number(cycle_count)
            idle = cls.get_idle_status(store, **kwargs)
            result = store.get_result(number, current_bets, balance, idle)

            balance = result['balance_close']
            current_bets = cls.set_new_bets(result['status'], current_bets, original_bets, **kwargs)

            if balance >= target_balance:
                return store

            cycle_count += 1

        return store

    @classmethod
    def get_idle_status(cls, store, **kwargs):
        idle_win = kwargs.get('idle_win', 0)
        idle_lose = kwargs.get('idle_lose', 0)
        idle_start = kwargs.get('idle_start', 0)

        result_pattern = store.get_result_pattern()

        if idle_start > 0 and cls.switch_idle_start:
            if len(result_pattern) < idle_start:
                return True

            if result_pattern[-idle_start:] != tuple(['LI'] * idle_start):
                return True

            cls.switch_idle_start = False

        if idle_win > 1:
            for x in range(1, idle_win):
                if result_pattern[-x - 1:] == tuple(['LI'] + ['W'] * x):
                    return False

        if idle_lose > 0:
            if result_pattern[-idle_lose:] != tuple(['LI']) * idle_lose:
                return True

        return False

    def run_aggregate(self, bets, **kwargs):
        aggregate_results = []

        for x in range(500):
            store = self.run_single(bets, **kwargs)
            result_summary = self.display.get_result_summary(store.results)
            aggregate_results.append(result_summary)

        return aggregate_results

    @staticmethod
    def tabulate_data(headers, data, table_format='grid'):
        return tabulate(data, headers, tablefmt=table_format)

    def get_next_number(self, idx):
        try:
            if self.backtest is None:
                return self.get_random_number()

            else:
                return self.backtest[idx]

        except IndexError:
            exit('insufficient backtest numbers to complete simulation')

    @staticmethod
    def get_random_number():
        return randint(0, 36)

    @staticmethod
    def get_result_model():
        return ResultModel()

    @staticmethod
    def set_new_bets(status, current_bets, original_bets, **kwargs):
        raise NotImplementedError()
