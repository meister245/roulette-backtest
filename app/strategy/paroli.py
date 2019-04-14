from app.strategy.common import StrategyCommon


class StrategyParoli(StrategyCommon):
    def __init__(self):
        StrategyCommon.__init__(self)

    @staticmethod
    def get_new_bet(bet, bet_result, table_limit=150.0):
        if bet['type'] in bet_result['win_types']:

            if bet['size_current'] * 2 > table_limit:
                return bet['size_current']

            else:
                return bet['size_current'] * 2

        else:
            return bet['size_original']
