import re
import os
import os.path
import random

from app.controller.bet import BetController
from app.model.display import DisplayModel


class ServiceController(object):
    display_model = DisplayModel()

    def run_simulation(self, bet_configs, backtest_path, **kwargs) -> None:
        mode, spins = kwargs['mode'], kwargs['spins']

        if mode in ['rgn']:
            numbers = self.get_rng_numbers(spins)
            results = self.run_simulation_rng(bet_configs, numbers, **kwargs)
            self.display_model.print_result_summary_rgn(results)
            self.display_model.print_result_details(results)

        elif mode in ['backtest']:
            backtest_data = self.get_backtest_numbers(backtest_path, spins)
            results = self.run_simulation_backtest(bet_configs, backtest_data, **kwargs)
            self.display_model.print_result_summary_backtest(results)

        else:
            exit('invalid game mode - {}'.format(kwargs['mode']))

    @staticmethod
    def run_simulation_rng(bet_configs, numbers, **kwargs):
        bet_ctrl = BetController(numbers)

        for c in bet_configs:
            bet_ctrl.set_bet_config(c)

        return bet_ctrl.run_simulation(**kwargs)

    @staticmethod
    def run_simulation_backtest(bet_configs, backtest_data, **kwargs):
        results = {}

        for filename, numbers in backtest_data.items():
            bet_ctrl = BetController(numbers)

            for c in bet_configs:
                bet_ctrl.set_bet_config(c)

            results[filename] = bet_ctrl.run_simulation(**kwargs)

        return results

    @staticmethod
    def get_rng_numbers(spins):
        if spins == 0:
            raise ValueError('invalid spin number for RGN mose')

        return [random.randint(0, 36) for x in range(spins)]

    @staticmethod
    def get_backtest_numbers(dir_path, spins):
        backtest_numbers = {}

        for filename in os.listdir(dir_path):
            file_path = os.path.realpath('{}/{}'.format(dir_path, filename))

            with open(file_path, 'r') as f:
                numbers = []

                for row in f.read().split('\n'):
                    if not re.search(r'^([0-9]{1,2}(?:,)?)+$', row):
                        raise ValueError('invalid data format in file - {}'.format(filename))

                    numbers.extend([int(x) for x in row.split(',')])

                    if spins != 0 and len(numbers) >= spins:
                        break

            backtest_numbers[filename] = numbers[:spins] if spins != 0 else numbers

        return backtest_numbers
