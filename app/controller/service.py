import collections
import itertools
import os
import os.path
import random
import re

from ..roulette import Roulette
from . import BetController, DisplayController


class ServiceController:
    roulette = Roulette()
    display_ctrl = DisplayController()

    def run_simulation(self, bet_configs, backtest_path, **kwargs) -> None:
        mode, spins = kwargs.pop('mode', 'rng'), kwargs.pop('spins', 50)

        if mode == 'rng':
            numbers = self.get_rng_numbers(spins)
            results = self.run_simulation_rng(bet_configs, numbers, **kwargs)

            self.display_ctrl.print_result_summary_rng(results)
            self.display_ctrl.print_result_details(results)

        elif mode == 'backtest':
            backtest_numbers = self.get_backtest_numbers(backtest_path, spins)
            results = self.run_simulation_backtest(
                bet_configs, backtest_numbers, **kwargs)

            self.display_ctrl.print_result_summary_backtest(results)

    @classmethod
    def run_simulation_rng(cls, bet_configs: list, numbers: list, **kwargs):
        bet_configs = [bet_configs] if isinstance(
            bet_configs, str) else bet_configs

        bet_ctrl = BetController()

        for config in bet_configs:
            bet_ctrl.process_bet_config(config)

        return bet_ctrl.run_simulation(numbers, **kwargs)

    @classmethod
    def run_simulation_backtest(cls, bet_configs: list, backtest_numbers: dict, **kwargs):
        bet_configs = [bet_configs] if isinstance(
            bet_configs, str) else bet_configs

        results = {}

        for filename, numbers in backtest_numbers.items():
            bet_ctrl = BetController()

            for config in bet_configs:
                bet_ctrl.process_bet_config(config)

            results[filename] = bet_ctrl.run_simulation(numbers, **kwargs)

        return results

    def run_simulation_bruteforce(self, backtest_path, **kwargs):
        spins = kwargs.pop('spins', 50)
        backtest_numbers = self.get_backtest_numbers(backtest_path, spins)

        counter, total_results = 0, []
        pl, bl = kwargs['patterns_list'], kwargs['bets_list']
        strategy, win_limit, lose_limit = kwargs['strategy'], kwargs['win_limit'], kwargs['lose_limit']

        print(
            f'generating bet configurations - strategy: {strategy} - min profit: {kwargs["min_profit"]}')

        for b in self.generate_bet_types_combinations(bl, with_replacement=False):
            for p in self.generate_bet_types_combinations(pl, with_replacement=True):
                counter += 1
                profits = []
                config = f'{strategy},{p},1,{b},{lose_limit},{win_limit}'

                print(f'processing combination {counter}\r', end='')

                for _, numbers in backtest_numbers.items():
                    bet_ctrl = BetController()

                    bet_ctrl.process_bet_config(config)
                    s_results = bet_ctrl.run_simulation(numbers, **kwargs)

                    profit = s_results[-1]['balance'] - s_results[0]['balance']
                    profits.append(profit if profit > 0 else 0)

                avg_profit = sum(profits) / len(profits)

                if avg_profit < kwargs['min_profit']:
                    continue

                result = {'config': config, 'avg_profit': avg_profit}
                total_results.append(result)

                print(result)

        print(f'processed {counter} combinations')

        return total_results

    @staticmethod
    def get_rng_numbers(spins):
        if spins == 0:
            raise ValueError('invalid spin number for RNG mode')

        return tuple([random.randint(0, 36) for x in range(spins)])

    @classmethod
    def generate_bet_types_combinations(cls, bet_types, with_replacement=False):
        func = itertools.combinations_with_replacement if with_replacement \
            else itertools.combinations

        if isinstance(bet_types, str) and len(bet_types) > 0:
            bet_types = set(bet_types.split(','))
        else:
            bet_types = cls.roulette.get_bet_types()

        for i in range(1, len(bet_types) + 1):
            for combo in func(bet_types, i):
                yield ':'.join(combo)

    @staticmethod
    def get_backtest_numbers(dir_path, spins=0):
        backtest_numbers = {}

        for filename in os.listdir(dir_path):
            file_path = os.path.realpath(f'{dir_path}/{filename}')

            with open(file_path, 'r') as f:
                numbers = []

                for row in f.read().split('\n'):
                    if not re.search(r'^([0-9]{1,2}(?:,)?)+$', row):
                        raise ValueError(
                            f'invalid data format in file - {filename}')

                    numbers.extend([int(x) for x in row.split(',')])

                    if spins != 0 and len(numbers) >= spins:
                        break

            backtest_numbers[filename] = numbers[:spins] if spins != 0 else numbers

        return collections.OrderedDict(sorted(backtest_numbers.items()))
