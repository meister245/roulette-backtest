class StrategyMartingale(object):
    def __init__(self):
        pass

    @staticmethod
    def get_new_bet(bet, bet_result, table_limit=150.0):
        if bet['type'] in bet_result['win_types']:
            return bet['size_original']

        elif bet['size_current'] * 2 > table_limit:
            return bet['size_current']

        else:
            return bet['size_current'] * 2

    @staticmethod
    def get_new_status(bet):
        if bet['limit_lose'] == bet['lose_current']:
            return False

        if bet['limit_win'] == bet['win_current']:
            return False

        return True
