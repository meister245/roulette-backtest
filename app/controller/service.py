from app.controller.bet import BetController
from app.model.display import DisplayModel


class ServiceController(object):
    bet_ctrl = BetController()
    display_model = DisplayModel()

    def run_simulation(self, bets: list, **kwargs) -> None:
        mode = kwargs.get('mode', 'single')

        if mode in ['single', 'live']:
            self.run_simulation_single(bets, **kwargs)

        elif mode == 'aggregate':
            self.run_simulation_aggregate(bets, **kwargs)

        else:
            exit('invalid game mode - {}'.format(kwargs['mode']))

    @classmethod
    def run_simulation_single(cls, bets, **kwargs):
        store = cls.bet_ctrl.run_simulation(bets, **kwargs)
        cls.display_model.print_result_summary(store.results)
        cls.display_model.print_result_details(store.results)

    @classmethod
    def run_simulation_aggregate(cls, bets, **kwargs):
        summaries = []

        for x in range(kwargs.pop('cycles_aggregate', 500)):
            store = cls.bet_ctrl.run_simulation(bets, **kwargs)
            summaries.append(cls.display_model.get_result_summary(store.results))

        cls.display_model.print_result_summary_aggregated(summaries)
