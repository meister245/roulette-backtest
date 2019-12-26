import re
import os
import os.path
import random
import itertools

from ..controller.bet import BetController
from ..controller.display import DisplayController
from ..controller.roulette import RouletteController


class ServiceController(object):
    roulette_ctrl = RouletteController()
    display_ctrl = DisplayController()

    def run_simulation(self, bet_configs, backtest_path, **kwargs) -> None:
        mode, spins = kwargs.pop('mode', 'rng'), kwargs.pop('spin', 50)

        if mode == 'rng':
            data = self.get_rng_numbers(spins)
            results = self.__simulation_single(bet_configs, data, **kwargs)
            self.display_ctrl.print_result_summary_rng(results)
            self.display_ctrl.print_result_details(results)

        elif mode == 'backtest':
            data = self.get_backtest_numbers(backtest_path, spins)
            results = self.__simulation_backtest(bet_configs, data, **kwargs)
            self.display_ctrl.print_result_summary_backtest(results)

    def run_bruteforce(self, backtest_path, **kwargs):
        mode, spins = kwargs.pop('mode', 'rng'), kwargs.pop('spin', 50)
        sort_key = 'profit' if mode == 'rng' else 'avg_profit'

        if mode == 'rng':
            data = self.get_rng_numbers(spins)
            result = self.__bruteforce(mode, data, **kwargs)

        elif mode == 'backtest':
            data = self.get_backtest_numbers(backtest_path, spins)
            result = self.__bruteforce(mode, data, **kwargs)

        else:
            raise ValueError(f'invalid mode - {mode}')

        return sorted(result, key=lambda k: k[sort_key], reverse=True)

    @staticmethod
    def __simulation_single(bet_configs, numbers, **kwargs):
        bet_ctrl = BetController(numbers)

        if isinstance(bet_configs, str):
            bet_configs = [bet_configs]

        for c in bet_configs:
            parsed = bet_ctrl.parse_bet_config(c)
            bet_ctrl.bet_configs.append(parsed)

        return bet_ctrl.run_simulation(**kwargs)

    @staticmethod
    def __simulation_backtest(bet_configs, backtest_data, **kwargs):
        results = {}

        for filename, numbers in backtest_data.items():
            bet_ctrl = BetController(numbers)

            for c in bet_configs:
                parsed = bet_ctrl.parse_bet_config(c)
                bet_ctrl.bet_configs.append(parsed)

            results[filename] = bet_ctrl.run_simulation(**kwargs)

        return results

    def __bruteforce(self, mode, data, **kwargs):
        counter, total_results = 0, []
        pl, bl = kwargs['patterns_list'], kwargs['bets_list']
        strategy, win_limit, lose_limit = kwargs['strategy'], kwargs['win_limit'], kwargs['lose_limit']

        print(f'generating bet configurations - strategy: {strategy} - min profit: {kwargs["min_profit"]}')

        f = self.__bruteforce_rng if mode == 'rng' else self.__bruteforce_backtest

        for b in self.generate_bet_types_combinations(bl, repl=False):
            for p in self.generate_bet_types_combinations(pl, repl=True):
                counter += 1
                config = f'{strategy},{p},1,{b},{lose_limit},{win_limit}'
                print(f'processing combination {counter}\r', end='')

                result = f(config, data, **kwargs)

                if not result:
                    continue

                print(result)
                total_results.append(result)

        print(f'processed {counter} combinations')

        return total_results

    def __bruteforce_rng(self, config, data, **kwargs):
        s_results = self.__simulation_single(config, data, **kwargs)
        profit = s_results[-1]['balance'] - s_results[0]['balance']

        if profit < kwargs['min_profit']:
            return False

        return {'config': config, 'profit': profit}

    def __bruteforce_backtest(self, config, data, **kwargs):
        profits = []

        for filename, numbers in data.items():
            s_results = self.__simulation_single(config, numbers, **kwargs)
            profit = s_results[-1]['balance'] - s_results[0]['balance']
            profits.append(profit if profit > 0 else 0)

        avg_profit = sum(profits) / len(profits)

        if avg_profit < kwargs['min_profit']:
            return False

        return {'config': config, 'avg_profit': avg_profit}

    @staticmethod
    def get_rng_numbers(spins):
        if spins == 0:
            raise ValueError('invalid spin number for RNG mode')

        return tuple([random.randint(0, 36) for x in range(spins)])

    @classmethod
    def generate_bet_types_combinations(cls, bet_types, repl=False):
        f = itertools.combinations_with_replacement if repl else itertools.combinations

        if isinstance(bet_types, str) and len(bet_types) > 0:
            bet_types = set(bet_types.split(','))
        else:
            bet_types = cls.roulette_ctrl.get_bet_types()

        for l in range(1, len(bet_types) + 1):
            for combo in f(bet_types, l):
                yield ':'.join(combo)

    @staticmethod
    def get_backtest_numbers(dir_path, spins):
        backtest_numbers = {}

        for filename in os.listdir(dir_path):
            file_path = os.path.realpath(f'{dir_path}/{filename}')

            with open(file_path, 'r') as f:
                numbers = []

                for row in f.read().split('\n'):
                    if not re.search(r'^([0-9]{1,2}(?:,)?)+$', row):
                        raise ValueError(f'invalid data format in file - {filename}')

                    numbers.extend([int(x) for x in row.split(',')])

                    if spins != 0 and len(numbers) >= spins:
                        break

            backtest_numbers[filename] = numbers[:spins] if spins != 0 else numbers

        return backtest_numbers
