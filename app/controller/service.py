import random

from app.controller.bet import BetController
from app.model.display import DisplayModel


class ServiceController(object):
    display_model = DisplayModel()

    def run_simulation(self, bet_configs, file_path, **kwargs) -> None:
        mode = kwargs.get('mode', 'single')

        if mode in ['single', 'live']:
            results = self.run_simulation_single(bet_configs, file_path, **kwargs)
            self.display_model.print_result_summary(results)
            self.display_model.print_result_details(results)

        elif mode in ['aggregate']:
            summaries = self.run_simulation_aggregate(bet_configs, file_path, **kwargs)
            self.display_model.print_result_summary_aggregated(summaries)

        else:
            exit('invalid game mode - {}'.format(kwargs['mode']))

    def run_simulation_single(self, bet_configs, file_path, **kwargs):
        bet_ctrl = BetController()

        if isinstance(file_path, str):
            bet_ctrl.set_backest_numbers(self.get_backtest_numbers(file_path, **kwargs))

        for c in bet_configs:
            bet_ctrl.set_bet_config(c)

        return bet_ctrl.run_simulation(**kwargs)

    def run_simulation_aggregate(self, bet_configs, file_path, **kwargs):
        summaries = []

        for x in range(kwargs.pop('cycles', 500)):
            results = self.run_simulation_single(bet_configs, file_path, **kwargs)
            summaries.append(self.display_model.get_result_summary(results))

        return summaries

    @staticmethod
    def get_backtest_numbers(file_path, **kwargs):
        numbers = []
        spins = kwargs.get('spins', 50)

        try:
            with open(file_path, 'r') as f:
                rows = [x.split(',') for x in f.read().split('\n')]

                while len(numbers) < spins:
                    numbers.extend(random.choice(rows))

        except OSError:
            raise ValueError('invalid file path - {}'.format(file_path))

        return [int(x) for x in numbers]
