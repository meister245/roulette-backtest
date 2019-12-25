import re
import os
import os.path
import random

from ..controller.analyze import AnalyzeController
from ..controller.bet import BetController
from ..controller.display import DisplayController


class ServiceController(object):
    ana_ctrl = AnalyzeController()
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
        pl, bl = kwargs['patterns_list'], kwargs['bets_list']
        pc, bc = kwargs['patterns_complexity'], kwargs['bets_complexity']

        counter = 1
        total_results = []

        options = {x.split(':')[0]: x.split(':')[1] for x in kwargs['custom'].split(',')} if kwargs['custom'] else {}

        strategy = options.get('strategy', 'simple')
        win_limit = options.get('win_limit', '1')
        loss_limit = options.get('loss_limit', '1')

        print('generating bet configurations')

        f = self.__bruteforce_rng if mode == 'rng' else self.__bruteforce_backtest

        for b in self.ana_ctrl.generate_bet_types_combinations(bc, custom_list=bl):
            for p in self.ana_ctrl.generate_bet_patterns_combinations(pc, custom_list=pl):
                counter += 1
                config = f'{strategy},{p},1,{b},{loss_limit},{win_limit}'

                print('processing combination {0}\r'.format(counter), end='')
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
        avg_profit = self.get_backtest_avg_profit(data, config, **kwargs)

        if avg_profit == 0:
            return False

        return {'config': config, 'avg_profit': avg_profit}

    @staticmethod
    def get_rng_numbers(spins):
        if spins == 0:
            raise ValueError('invalid spin number for RNG mode')

        return tuple([random.randint(0, 36) for x in range(spins)])

    def get_backtest_avg_profit(self, backtest_data, bet_config, **kwargs):
        profits = []

        for filename, numbers in backtest_data.items():
            s_results = self.__simulation_single(bet_config, numbers, **kwargs)

            profit = s_results[-1]['balance'] - s_results[0]['balance']

            if profit < 30 * -1:
                return 0

            profits.append(profit)

        avg_profit = sum(profits) / len(profits)

        if avg_profit < kwargs['min_profit']:
            return 0

        return avg_profit

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
