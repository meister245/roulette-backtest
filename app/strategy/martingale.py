from app.store.result import ResultStore
from app.strategy.common import StrategyCommon


class StrategyMartingale(StrategyCommon):
    def __init__(self, backtest):
        self.backtest = backtest

        StrategyCommon.__init__(self)

    def run_single(self, test_params):
        store = ResultStore()

        current_balance = test_params['balance']
        bet_amount = test_params['bet_amount']
        cycles = test_params['cycles']

        if self.backtest is not None:
            cycles = len(self.backtest) if len(self.backtest) < cycles else cycles

        for idx, x in enumerate(range(cycles)):
            if bet_amount > current_balance:
                break

            number = self.get_next_number(idx, self.backtest)
            res = store.process(number, test_params['bet_type'], bet_amount, current_balance)

            current_balance += res['win'] - bet_amount
            current_balance = round(current_balance, 2)

            if current_balance <= 0:
                break

            bet_amount = test_params['bet_amount'] if res['status'] == 'win' else bet_amount * 2

        return store.results

    def run_aggregate(self, test_params):
        aggregate_results = []

        for x in range(500):
            results = self.run_single(test_params)
            result_summary = self.get_result_summary(results)
            aggregate_results.append(result_summary)

        return aggregate_results
