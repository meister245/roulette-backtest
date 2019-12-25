from app.factory.bet import BetFactory
from app.controller.roulette import RouletteController


class BetController(object):
    bet_fctr = BetFactory()
    roulette_ctrl = RouletteController()

    def __init__(self, numbers):
        self.bets = []
        self.results = []
        self.bet_configs = []
        self.numbers = numbers

    def get_bets_total_size(self):
        total_size = 0

        for x in self.bets:
            total_size += x.size_current if x.is_bet_active() else 0

        return total_size

    def run_simulation(self, **kwargs):
        balance, target_profit = kwargs.pop('balance', 1000.0), kwargs.pop('target_profit', None)

        for spin_count in range(len(self.numbers)):
            bet_results = []
            number = self.numbers[spin_count - 1]
            numbers = [x['number'] for x in self.results]

            self.set_bets(numbers)

            if self.get_bets_total_size() > balance:
                break

            for bet in self.bets:
                balance, result = bet.run_bet(number, spin_count, balance, **kwargs)

                if len(result) != 0:
                    bet_results.append(result)

            self.results.append({'results': bet_results, 'balance': balance, 'number': number})

        return tuple(self.results)

    @classmethod
    def parse_bet_config(cls, config: str) -> dict:
        elements = [x for x in config.split(',') if len(x) != 0]

        if len(elements) < 5:
            raise ValueError(f'invalid model config - {config}')

        cls.bet_fctr.validate_bet_strategy(elements[0])

        config = {
            'strategy': elements[0],
            'pattern': cls.roulette_ctrl.get_bet_pattern(elements[1]),
            'size': elements[2],
            'types': [cls.roulette_ctrl.validate_bet_type(x) for x in elements[3].split(':')],
            'limit_lose': elements[4] if 4 <= len(elements) else 0,
            'limit_win': elements[5] if 5 <= len(elements) else 0
        }

        return config

    def set_bets(self, numbers):
        for config in self.bet_configs:
            name = config['strategy']
            config['size'] = config['size']

            if self.roulette_ctrl.is_pattern_match(config['pattern'], numbers):
                self.bets.append(self.bet_fctr.get_bet(name, **config))
