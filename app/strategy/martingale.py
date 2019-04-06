from app.strategy.common import StrategyCommon


class StrategyMartingale(StrategyCommon):
    def __init__(self, backtest):
        StrategyCommon.__init__(self, backtest)

    @staticmethod
    def set_new_bets(status, current_bets, original_bets, **kwargs):
        if status in ['win', 'win_idle', 'lose_idle']:
            return original_bets

        elif status in ['null', 'null_idle']:
            return current_bets

        if sum([x for x in current_bets.values()]) * 2 > kwargs.get('table_limit', 150.0):
            return current_bets

        else:
            return {k: round(v * 2, 2) for k, v in current_bets.items()}
