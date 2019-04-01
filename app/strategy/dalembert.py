from app.strategy.martingale import StrategyMartingale


class StrategyDalembert(StrategyMartingale):
    def __init__(self, backtest):
        self.backtest = backtest

        StrategyMartingale.__init__(self, backtest)

    @staticmethod
    def set_new_bet_amount(res, bet_amount, test_params):
        if res['status'] == 'win':

            if bet_amount == test_params['bet_amount']:
                return test_params['bet_amount']

            else:
                return bet_amount - test_params['bet_amount']

        else:
            return bet_amount + test_params['bet_amount']
