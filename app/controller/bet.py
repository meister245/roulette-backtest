import random

from app.factory.bet import BetFactory
from app.model.roulette import RouletteModel


class BetController(object):
    bet_fctr = BetFactory()
    roulette_mdl = RouletteModel()

    def __init__(self, bet_configs):
        self.bets = []
        self.results = []
        self.bet_configs = [self.get_bet_config(x) for x in bet_configs]

    @classmethod
    def get_bet_config(cls, config: str) -> dict:
        elements = [x for x in config.split(',') if len(x) != 0]

        if len(elements) < 5:
            raise ValueError('invalid bet config - {}'.format(config))

        cls.bet_fctr.validate_bet_strategy(elements[0])
        cls.roulette_mdl.validate_bet_type(elements[3])

        config = {
            'strategy': elements[0],
            'pattern': cls.roulette_mdl.get_bet_pattern(elements[1]),
            'size': elements[2],
            'type': elements[3],
            'limit_lose': elements[4] if 4 <= len(elements) else 0,
            'limit_win': elements[5] if 5 <= len(elements) else 0
        }

        return config

    @staticmethod
    def get_bet_size(size, balance, ratio=50):
        return round(balance / ratio, 1) if size == 'dynamic' else size

    def get_bets_total_size(self):
        return sum([x.size_current if x.is_bet_active() else 0 for x in self.bets]) if len(self.bets) > 0 else 0

    @staticmethod
    def get_next_number(**kwargs):
        if kwargs['mode'] == 'live':

            while True:
                try:
                    number = int(input('Next Number: '))

                    if abs(number) > 36:
                        raise ValueError()

                    return number

                except ValueError:
                    print('invalid value')

        else:
            return random.randint(0, 36)

    def run_simulation(self, **kwargs):
        balance, target_profit = kwargs.pop('balance', 1000.0), kwargs.pop('target_profit', None)
        spins, backtest = kwargs.pop('spins', None), kwargs.pop('backtest', None)

        if spins is None and target_profit is None:
            raise ValueError('spins OR target_profit parameter required')

        elif spins is not None and target_profit is not None:
            raise ValueError('simulation does not support fixed spins AND fixed target_profit')

        if isinstance(spins, (int, float)):
            return self.run_fixed_spins(spins, balance, **kwargs)

        elif isinstance(target_profit, (int, float)):
            return self.run_fixed_profit(target_profit, balance, **kwargs)

        else:
            raise ValueError('invalid parameters')

    def run_fixed_spins(self, spins, balance, **kwargs):
        for spin_count in range(spins):
            bet_results = []
            number = self.get_next_number(**kwargs)

            if self.get_bets_total_size() > balance:
                break

            for bet in self.bets:
                balance, result = bet.run_bet(number, spin_count, balance, **kwargs)

                if len(result) != 0:
                    bet_results.append(result)

            self.results.append({'results': bet_results, 'balance': balance, 'number': number})

            self.set_new_bets(balance)

        return tuple(self.results)

    def run_fixed_profit(self, target_profit, balance, **kwargs):
        target_balance, spin_count = balance + target_profit, 0

        while True:
            bet_results = []
            number = self.get_next_number(**kwargs)

            if self.get_bets_total_size() > balance:
                break

            for bet in self.bets:
                balance, result = bet.run_bet(number, spin_count, balance, **kwargs)
                bet_results.append(result)

            self.results.append({'results': bet_results, 'balance': balance, 'number': number})

            self.set_new_bets(balance)

            if balance >= target_balance:
                break

            spin_count += 1

        return tuple(self.results)

    def set_new_bets(self, balance):
        numbers = [x['number'] for x in self.results]

        for config in self.bet_configs:
            if self.roulette_mdl.is_pattern_match(config['pattern'], numbers):
                config['size'] = self.get_bet_size(config['size'], balance)
                self.bets.append(self.bet_fctr.get_bet(config['strategy'], **config))
