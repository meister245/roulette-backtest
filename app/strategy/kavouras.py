from app.strategy.common import StrategyCommon


class KavourasStrategy(StrategyCommon):
    bet_combination = ('four', 'line_31_32_33_34_35_36', 'split_8_11', 'split_13_14',
                       'split_15_18', 'split_17_20', 'split_27_30')

    def __init__(self, backtest):
        StrategyCommon.__init__(self, backtest)

    def run_single(self, bets, **kwargs):
        store = self.get_result_model()

        if not isinstance(bets, (int, float)):
            exit('invalid bet structure for strategy')

        current_bets = self.get_kavouras_bets(bets)

        balance = kwargs['balance']
        cycles = self.get_cycles(kwargs['cycles'])

        if current_bets is None or sum(current_bets.values()) <= 0:
            exit('invalid bet - {}'.format(bets))

        for idx, x in enumerate(range(cycles)):
            if sum([v for v in current_bets.values()]) > balance:
                break

            number = self.get_next_number(idx)
            idle = self.get_idle_status(store, **kwargs)
            result = store.get_result(number, current_bets, balance, idle)

            balance = result['balance_close']

        return store

    @classmethod
    def get_kavouras_bets(cls, bet_amount):
        bets = {}

        for x in cls.bet_combination:
            if x.startswith('four'):
                bets[x] = round(bet_amount * 1, 2)

            elif x.startswith('line'):
                bets[x] = round(bet_amount * 2, 2)

            elif x.startswith('split'):
                bets[x] = round(bet_amount * 1, 2)

        return bets
