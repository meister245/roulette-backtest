class StrategyMartingale(object):
    def __init__(self):
        pass

    @staticmethod
    def set_new_bet(bet, bet_result, table_limit=150.0):
        if bet['type'] in bet_result['win_types']:
            return bet['size_original']

        elif bet['size_current'] * 2 > table_limit:
            return bet['size_current']

        else:
            return bet['size_current'] * 2
