import random

from app.factory.bet import BetFactory
from app.model.roulette import RouletteModel


class BetController(object):
    roulette_mdl = RouletteModel()

    def __init__(self):
        self.results = []
        self.bet_configs = []

        self.bet_fctr = BetFactory()

    @staticmethod
    def get_bet_size(size, balance, ratio=50):
        return round(balance / ratio, 1) if size == 'dynamic' else size

    def get_bets_total_size(self):
        total_size = 0

        for x in self.bet_fctr.bets:
            total_size += x.size_current if x.is_bet_active() else 0

        return total_size

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
            numbers = [x['number'] for x in self.results]

            self.set_bets(numbers, balance)

            if self.get_bets_total_size() > balance:
                break

            for bet in self.bet_fctr.bets:
                balance, result = bet.run_bet(number, spin_count, balance, numbers, **kwargs)

                if len(result) != 0:
                    bet_results.append(result)

            self.results.append({'results': bet_results, 'balance': balance, 'number': number})

        return tuple(self.results)

    def run_fixed_profit(self, target_profit, balance, **kwargs):
        target_balance, spin_count = balance + target_profit, 0

        while True:
            bet_results = []
            number = self.get_next_number(**kwargs)
            numbers = [x['number'] for x in self.results]

            self.set_bets(numbers, balance)

            if self.get_bets_total_size() > balance:
                break

            for bet in self.bet_fctr.bets:
                kwargs['numbers'] = [x['number'] for x in self.results]
                balance, result = bet.run_bet(number, spin_count, balance, numbers, **kwargs)

                if len(result) != 0:
                    bet_results.append(result)

            self.results.append({'results': bet_results, 'balance': balance, 'number': number})

            if balance >= target_balance:
                break

            spin_count += 1

        return tuple(self.results)

    def set_bet_config(self, config: str) -> None:
        elements = [x for x in config.split(',') if len(x) != 0]

        if len(elements) < 5:
            raise ValueError('invalid bet config - {}'.format(config))

        self.bet_fctr.validate_bet_strategy(elements[0])
        self.roulette_mdl.validate_bet_type(elements[3])

        config = {
            'strategy': elements[0],
            'pattern': self.roulette_mdl.get_bet_pattern(elements[1]),
            'size': elements[2],
            'type': elements[3],
            'limit_lose': elements[4] if 4 <= len(elements) else 0,
            'limit_win': elements[5] if 5 <= len(elements) else 0
        }

        self.bet_configs.append(config)

    def set_bets(self, numbers, balance):
        for config in self.bet_configs:
            name = config['strategy']
            config['size'] = self.get_bet_size(config['size'], balance)

            if self.roulette_mdl.is_pattern_match(config['pattern'], numbers):
                self.bet_fctr.set_bet(name, **config)
