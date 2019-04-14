from app.strategy.common import StrategyCommon


class StrategySimple(StrategyCommon):
    def __init__(self):
        StrategyCommon.__init__(self)

    @staticmethod
    def get_new_bet(bet, bet_result, table_limit=150.0):
        return bet['size_current']
