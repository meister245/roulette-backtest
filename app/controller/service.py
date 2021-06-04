import collections
import json
import os
import os.path
import random
import re

from ..roulette import Roulette
from . import BetController, DisplayController


class ServiceController:
    roulette = Roulette()
    display_ctrl = DisplayController()

    def __init__(self, strategy_dir, backtest_dir) -> None:
        self.strategy_dir = strategy_dir
        self.backtest_dir = backtest_dir

    def run_simulation(self, **kwargs) -> None:
        mode, spins = kwargs.pop('mode', 'rng'), kwargs.pop('spins', 0)

        backtest_filename = kwargs.pop('backtest', False)
        strategy_filename = kwargs.pop('strategy', 'sample')

        bet_configs = self.get_strategy(strategy_filename)

        if mode == 'rng':
            spins = 50 if spins == 0 else spins
            numbers = self.get_rng_numbers(spins)
            self.run_simulation_single(bet_configs, numbers, **kwargs)

        elif backtest_filename and mode == 'backtest':
            numbers = self.get_backtest_number(
                backtest_filename=backtest_filename, spins=spins)

            self.run_simulation_single(bet_configs, numbers, **kwargs)

        elif mode == 'backtest':
            backtest_filter = kwargs.pop('backtest_filter', False)

            backtest_numbers = self.get_backtest_numbers(
                backtest_filter=backtest_filter, spins=spins)

            self.run_simulation_backtest(
                bet_configs, backtest_numbers, **kwargs)

    @classmethod
    def run_simulation_single(cls, bet_configs: dict, numbers: list, **kwargs):
        bet_ctrl = BetController()

        for config in bet_configs.values():
            bet_ctrl.configs.append(config)

        results = bet_ctrl.run_simulation(numbers, **kwargs)

        cls.display_ctrl.print_result_summary(results)
        cls.display_ctrl.print_result_details(results)

    @classmethod
    def run_simulation_backtest(cls, bet_configs: list, backtest_numbers: dict, **kwargs):
        bet_configs = [bet_configs] if isinstance(
            bet_configs, str) else bet_configs

        results = {}

        for filename, numbers in backtest_numbers.items():
            bet_ctrl = BetController()

            for config in bet_configs.values():
                bet_ctrl.configs.append(config)

            results[filename] = bet_ctrl.run_simulation(numbers, **kwargs)

        cls.display_ctrl.print_result_summary_backtest(results)

    @staticmethod
    def get_rng_numbers(spins):
        if spins == 0:
            raise ValueError('invalid spin number for RNG mode')

        return tuple([random.randint(0, 36) for x in range(spins)])

    def get_strategy(self, strategy_filename: str):
        for root, __, files in os.walk(self.strategy_dir):
            for name in files:
                filepath = os.path.join(root, name)

                if filepath.endswith(f'{strategy_filename}.json'):
                    return self.parse_strategy_file(filepath)

        raise Exception(
            f'no filename matched for keyword {strategy_filename} found for strategy')

    def get_backtest_number(self, backtest_filename: str, spins: int = 0):
        for root, __, files in os.walk(self.backtest_dir):
            for name in files:
                filepath = os.path.join(root, name)

                if backtest_filename in filepath:
                    numbers = self.parse_backtest_file(filepath)
                    return numbers[:spins] if spins != 0 else numbers

        raise Exception(
            f'no filename matched for keyword {backtest_filename} found for backtest data')

    def get_backtest_numbers(self, backtest_filter: str = False, spins: int = 0):
        backtest_numbers = {}

        for root, _, files in os.walk(self.backtest_dir):
            for name in files:
                filepath = os.path.join(root, name)

                if backtest_filter and backtest_filter not in filepath:
                    break

                numbers = self.parse_backtest_file(filepath)
                numbers = numbers[:spins] if spins != 0 else numbers

                filepath = re.sub(self.backtest_dir, '', filepath)
                backtest_numbers[filepath] = numbers

        return collections.OrderedDict(sorted(backtest_numbers.items()))

    @staticmethod
    def parse_strategy_file(filepath):
        strategies = {}

        with open(filepath, 'r') as f:
            data = json.loads(f.read())
            common = data.pop('common')

            for strategy, config in data['strategies'].items():
                strategies[strategy] = {
                    'strategyName': strategy,
                    **common,
                    **config,
                }

            return strategies

    @staticmethod
    def parse_backtest_file(filepath, spins=0):
        with open(filepath, 'r') as f:
            numbers = []

            for row in f.read().split('\n'):
                if not re.search(r'^([0-9]{1,2}(?:,)?)+$', row):
                    raise ValueError(
                        f'invalid data format in file - {filepath}')

                numbers.extend([int(x) for x in row.split(',')])

                if spins != 0 and len(numbers) >= spins:
                    break

            return numbers
