import re
import os
import os.path
import random

from app.model.analyze import AnalyzeModel
from app.model.display import DisplayModel
from app.controller.bet import BetController


class ServiceController(object):
    ana_mdl = AnalyzeModel()
    display_model = DisplayModel()

    def run_simulation(self, bet_configs, backtest_path, **kwargs) -> None:
        mode, spins = kwargs['mode'], kwargs['spins']

        if mode in ['rgn']:
            numbers = self.get_rng_numbers(spins)
            results = self.run_simulation_single(bet_configs, numbers, **kwargs)
            self.display_model.print_result_summary_rgn(results)
            self.display_model.print_result_details(results)

        elif mode in ['backtest']:
            backtest_data = self.get_backtest_numbers(backtest_path, spins)
            results = self.run_simulation_backtest(bet_configs, backtest_data, **kwargs)
            self.display_model.print_result_summary_backtest(results)

    def run_bruteforce(self, backtest_path, **kwargs):
        mode, spins = kwargs['mode'], kwargs['spins']

        if mode in ['rgn']:
            numbers = self.get_rng_numbers(spins)
            result = self.run_bruteforce_rng(numbers, **kwargs)
            return sorted(result, key=lambda k: k['profit'], reverse=True)

        elif mode in ['backtest']:
            backtest_data = self.get_backtest_numbers(backtest_path, spins)
            result = self.run_bruteforce_backtest(backtest_data, **kwargs)
            return sorted(result, key=lambda k: k['avg_profit'], reverse=True)

    def run_bruteforce_rng(self, numbers, **kwargs):
        pl, bl = kwargs['patterns_list'], kwargs['bets_list']
        pc, bc = kwargs['patterns_complexity'], kwargs['bets_complexity']

        counter = 1
        total_results = []

        options = {x.split(':')[0]: x.split(':')[1] for x in kwargs['custom'].split(',')} if kwargs['custom'] else {}

        strategy = options.get('strategy', 'simple')
        win_limit = options.get('win_limit', '1')
        loss_limit = options.get('loss_limit', '1')

        print('generating bet configurations')

        bet_types_combos = self.ana_mdl.get_bet_types_combinations(bc, custom_list=bl)
        bet_patterns_combos = self.ana_mdl.get_bet_patterns_combinations(pc, custom_list=pl)

        for b in bet_types_combos:
            for p in bet_patterns_combos:
                print('processing combination {0}\r'.format(counter), end='')

                config = '{},{},1,{},{},{}'.format(strategy, p, b, loss_limit, win_limit)
                s_results = self.run_simulation_single(config, numbers, **kwargs)
                profit = s_results[-1]['balance'] - s_results[0]['balance']

                counter += 1

                if profit < kwargs['min_profit']:
                    continue

                total_results.append({'config': config, 'profit': profit})

                print(total_results[-1])

        print('processed {} combinations'.format(counter))

        return total_results

    def run_bruteforce_backtest(self, backtest_data, **kwargs):
        pl, bl = kwargs['patterns_list'], kwargs['bets_list']
        pc, bc = kwargs['patterns_complexity'], kwargs['bets_complexity']

        counter = 1
        total_results = []

        options = {x.split(':')[0]: x.split(':')[1] for x in kwargs['custom'].split(',')} if kwargs['custom'] else {}

        strategy = options.get('strategy', 'simple')
        win_limit = options.get('win_limit', '1')
        loss_limit = options.get('loss_limit', '1')

        print('generating bet configurations')

        bet_types_combos = self.ana_mdl.get_bet_types_combinations(bc, custom_list=bl)
        bet_patterns_combos = self.ana_mdl.get_bet_patterns_combinations(pc, custom_list=pl)

        for b in bet_types_combos:
            for p in bet_patterns_combos:
                print('processing combination {0}\r'.format(counter), end='')

                config = '{},{},1,{},{},{}'.format(strategy, p, b, loss_limit, win_limit)
                avg_profit = self.get_backtest_avg_profit(backtest_data, config, **kwargs)

                counter += 1

                if avg_profit == 0:
                    continue

                total_results.append({'config': config, 'avg_profit': avg_profit})

                print(total_results[-1])

        print('processed {} combinations'.format(counter))

        return total_results

    @staticmethod
    def run_simulation_single(bet_configs, numbers, **kwargs):
        bet_ctrl = BetController(numbers)

        if isinstance(bet_configs, str):
            bet_configs = [bet_configs]

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

    def get_backtest_avg_profit(self, backtest_data, bet_config, **kwargs):
        profits = []

        for filename, numbers in backtest_data.items():
            s_results = self.run_simulation_single(bet_config, numbers, **kwargs)

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
