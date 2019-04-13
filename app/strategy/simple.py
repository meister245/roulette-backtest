class StrategySimple(object):
    def __init__(self):
        pass

    @staticmethod
    def set_new_bet(bet, bet_result, table_limit=150.0):
        return bet['size_current']

    @staticmethod
    def get_new_status(bet, bet_result):
        return True
