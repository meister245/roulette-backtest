class StrategyCommon(object):
    @staticmethod
    def get_new_bet(bet, bet_result, table_limit=150.0):
        raise NotImplementedError()

    @staticmethod
    def get_new_status(bet):
        if bet['limit_lose'] == bet['lose_current']:
            return False

        if bet['limit_win'] == bet['win_current']:
            return False

        return True
