from app.strategy.martingale import StrategyMartingale


class StrategyParoli(StrategyMartingale):
    def __init__(self, backtest):
        self.backtest = backtest

        StrategyMartingale.__init__(self, backtest)

    @staticmethod
    def set_new_bet_amount(res, bet_amount, test_params):
        return bet_amount * 2 if res['status'] == 'win' else test_params['bet_amount']
