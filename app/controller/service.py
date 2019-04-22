from app.controller.bet import BetController
from app.model.display import DisplayModel


class ServiceController(object):
    display_model = DisplayModel()

    def __init__(self):
        self.bet_ctrl = BetController()

    def run_simulation(self, bet_configs, **kwargs) -> None:
        mode = kwargs.get('mode', 'single')

        for c in bet_configs:
            self.bet_ctrl.set_bet_config(c)

        if mode in ['single', 'live']:
            self.run_simulation_single(**kwargs)

        elif mode in ['aggregate']:
            self.run_simulation_aggregate(**kwargs)

        else:
            exit('invalid game mode - {}'.format(kwargs['mode']))

    def run_simulation_single(self, **kwargs):
        results = self.bet_ctrl.run_simulation(**kwargs)
        self.display_model.print_result_summary(results)

        if kwargs.get('verbose', False):
            self.display_model.print_result_details(results)

    def run_simulation_aggregate(self, **kwargs):
        summaries = []

        for x in range(kwargs.pop('cycles', 500)):
            results = self.bet_ctrl.run_simulation(**kwargs)
            summaries.append(self.display_model.get_result_summary(results))

        self.display_model.print_result_summary_aggregated(summaries)
