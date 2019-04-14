from app.model.bet import BetModel
from app.model.result import ResultModel


class BetController(object):
    bet_model = BetModel()

    @classmethod
    def run_simulation(cls, bets, **kwargs):
        bets = [cls.bet_model.parse_bet_pattern(x) for x in bets]

        balance, target_profit = kwargs.pop('balance', 1000.0), kwargs.pop('target_profit', None)
        cycles, backtest = kwargs.pop('cycles', None), kwargs.pop('backtest', None)

        if cycles is None and target_profit is None:
            exit('cycles OR target_profit parameter required')

        elif cycles is not None and target_profit is not None:
            exit('simulation does not support fixed cycles AND fixed target_profit')

        store = cls.get_result_model(backtest=backtest)

        if isinstance(cycles, (int, float)):
            cycles = len(backtest) if backtest is not None and len(backtest) < cycles else cycles
            return cls.run_fixed_cycles(store, bets, cycles, balance, **kwargs)

        elif isinstance(target_profit, (int, float)):
            return cls.run_fixed_profit(store, bets, target_profit, balance, **kwargs)

        else:
            exit('invalid parameters')

    @classmethod
    def run_fixed_cycles(cls, store, bets, cycles, balance, **kwargs):
        for cycle_count in range(cycles):
            if cls.bet_model.get_bets_sum(bets) > balance:
                break

            number = store.get_next_number(cycle_count, **kwargs)
            balance, bets = store.get_result(number, bets, balance, **kwargs)

            if kwargs['mode'] == 'live':
                cls.bet_model.print_bets(bets)

        return store

    @classmethod
    def run_fixed_profit(cls, store, bets, target_profit, balance, **kwargs):
        target_balance, cycle_count = balance + target_profit, 0

        while True:
            if cls.bet_model.get_bets_sum(bets) > balance:
                break

            number = store.get_next_number(cycle_count, **kwargs)
            balance, bets = store.get_result(number, bets, balance, **kwargs)

            if kwargs['mode'] == 'live':
                cls.bet_model.print_bets(bets)

            if balance >= target_balance:
                return store

            cycle_count += 1

        return store

    @staticmethod
    def get_result_model(**kwargs):
        return ResultModel(**kwargs)
