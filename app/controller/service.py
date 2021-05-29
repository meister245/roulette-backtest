import collections
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
        backtest_filter = kwargs.pop('backtest_filter', False)
        backtest_filename = kwargs.pop('backtest_file', False)

        if mode == 'rng':
            numbers = self.get_rng_numbers(spins)
            self.run_simulation_single(bet_configs, numbers, **kwargs)

        elif backtest_filename and mode == 'backtest':
            numbers = self.get_backtest_number(
                dir_path=backtest_path, backtest_filename=backtest_filename, spins=spins)

            self.run_simulation_single(bet_configs, numbers, **kwargs)

        elif mode == 'backtest':
            backtest_numbers = self.get_backtest_numbers(
                dir_path=backtest_path, backtest_filter=backtest_filter, spins=spins)

            self.run_simulation_backtest(
                bet_configs, backtest_numbers, **kwargs)

    @classmethod
    def run_simulation_single(cls, bet_configs: list, numbers: list, **kwargs):
        bet_configs = [bet_configs] if isinstance(
            bet_configs, str) else bet_configs

        bet_ctrl = BetController()

        for config in bet_configs:
            bet_ctrl.process_bet_config(config)

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

            for config in bet_configs:
                bet_ctrl.process_bet_config(config)

            results[filename] = bet_ctrl.run_simulation(numbers, **kwargs)

        cls.display_ctrl.print_result_summary_backtest(results)

    @staticmethod
    def get_rng_numbers(spins):
        if spins == 0:
            raise ValueError('invalid spin number for RNG mode')

        return tuple([random.randint(0, 36) for x in range(spins)])

    @classmethod
    def get_backtest_number(cls, dir_path: str, backtest_filename: str, spins: int = 0):
        for root, __, files in os.walk(dir_path):
            for name in files:
                filepath = os.path.join(root, name)

                if backtest_filename in filepath:
                    numbers = cls.parse_backtest_file(filepath)
                    return numbers[:spins] if spins != 0 else numbers

        raise Exception(
            f'no filename matched for keyword {backtest_filename} found for backtest data')

    @classmethod
    def get_backtest_numbers(cls, dir_path: str, backtest_filter: str = False, spins: int = 0):
        backtest_numbers = {}

        for root, _, files in os.walk(dir_path):
            for name in files:
                filepath = os.path.join(root, name)

                if backtest_filter and backtest_filter not in filepath:
                    break

                numbers = cls.parse_backtest_file(filepath)
                numbers = numbers[:spins] if spins != 0 else numbers

                filepath = re.sub(dir_path, '', filepath)
                backtest_numbers[filepath] = numbers

        return collections.OrderedDict(sorted(backtest_numbers.items()))

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
