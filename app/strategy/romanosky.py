from app.strategy.common import StrategyCommon


class RomanoskyStrategy(StrategyCommon):
    bet_combinations = [
        ('corner_2_3_5_6', 'corner_7_8_10_11', 'dozen_middle', 'dozen_right'),
        ('corner_1_2_4_5', 'corner_8_9_11_12', 'dozen_middle', 'dozen_right'),
        ('corner_14_15_17_18', 'corner_19_20_22_23', 'dozen_left', 'dozen_right'),
        ('corner_13_14_16_17', 'corner_20_21_23_24', 'dozen_left', 'dozen_right'),
        ('corner_26_27_29_30', 'corner_31_32_34_35', 'dozen_left', 'dozen_middle'),
        ('corner_25_26_28_29', 'corner_32_33_35_36', 'dozen_left', 'dozen_middle'),
    ]

    def __init__(self, backtest):
        StrategyCommon.__init__(self, backtest)

    def run_single(self, bets, **kwargs):
        store = self.get_result_model()

        if not isinstance(bets, (int, float)):
            exit('invalid bet structure for strategy')

        current_bets = self.get_romanosky_bets(bets)

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
    def get_romanosky_bets(cls, bet_amount):
        bets = {}

        combination = cls.bet_combinations[0]

        for x in combination:
            if x.startswith('corner'):
                bets[x] = round(bet_amount * 1, 2)

            elif x.startswith('dozen'):
                bets[x] = round(bet_amount * 3, 2)

        return bets
