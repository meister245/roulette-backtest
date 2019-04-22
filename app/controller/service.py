from app.controller.bet import BetController
from app.model.display import DisplayModel


class ServiceController(object):
    display_model = DisplayModel()

    def run_simulation(self, bet_configs, **kwargs) -> None:
        mode = kwargs.get('mode', 'single')

        if mode in ['single', 'live']:
            results = self.run_simulation_single(bet_configs, **kwargs)
            self.display_model.print_result_summary(results)

            if kwargs.get('verbose', False):
                self.display_model.print_result_details(results)

        elif mode in ['aggregate']:
            summaries = self.run_simulation_aggregate(bet_configs, **kwargs)
            self.display_model.print_result_summary_aggregated(summaries)

        else:
            exit('invalid game mode - {}'.format(kwargs['mode']))

    def run_simulation_single(self, bet_configs, **kwargs):
        bet_ctrl = BetController()

        for c in bet_configs:
            bet_ctrl.set_bet_config(c)

        results = bet_ctrl.run_simulation(**kwargs)

        return results

    def run_simulation_aggregate(self, bet_configs, **kwargs):
        summaries = []

        for x in range(kwargs.pop('cycles', 500)):
            results = self.run_simulation_single(bet_configs, **kwargs)
            summaries.append(self.display_model.get_result_summary(results))

        return summaries
