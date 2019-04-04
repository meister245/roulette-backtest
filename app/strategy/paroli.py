from app.strategy.martingale import StrategyCommon


class StrategyParoli(StrategyCommon):
    def __init__(self, backtest):
        StrategyCommon.__init__(self, backtest)

    @staticmethod
    def set_new_bets(status, current_bets, original_bets, **kwargs):
        if status == 'lose':
            return original_bets

        elif status == 'null':
            return current_bets

        if sum([x for x in current_bets.values()]) * 2 > kwargs.get('table_limit', 150.0):
            return current_bets

        else:
            return {k: round(v * 2, 2) for k, v in current_bets.items()}
