from app.strategy.common import StrategyCommon


class StrategyDalembert(StrategyCommon):
    def __init__(self, backtest):
        StrategyCommon.__init__(self, backtest)

    @staticmethod
    def set_new_bets(status, current_bets, original_bets, **kwargs):
        new_bets = {}

        if status == 'win' and current_bets == original_bets:
            return original_bets

        elif status == 'win' and current_bets != original_bets:
            for k, v in current_bets.items():
                new_bets[k] = round(v - original_bets[k], 2)

            return new_bets

        else:
            for k, v in current_bets.items():
                new_bets[k] = round(v + original_bets[k], 2)

            return new_bets
