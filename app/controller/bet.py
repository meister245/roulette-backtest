from ..bet import get_bet, BETS
from ..roulette import Roulette


class BetController:
    roulette = Roulette()

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
        balance = kwargs.pop('balance', 1000.0)

        for spin_count in range(len(self.numbers)):
            bet_results = []
            number = self.numbers[spin_count - 1]
            numbers = [x['number'] for x in self.results]

            self.set_bets(numbers)

            if self.get_bets_total_size() > balance:
                break

            for bet in self.bets:
                balance, result = bet.run_bet(
                    number, spin_count, balance, **kwargs)

                if len(result) != 0:
                    bet_results.append(result)

            self.results.append(
                {'results': bet_results, 'balance': balance, 'number': number})

        return tuple(self.results)

    @classmethod
    def parse_bet_config(cls, config: str) -> dict:
        elements = [x for x in config.split(',') if len(x) != 0]

        if len(elements) < 5:
            raise ValueError(f'invalid model config - {config}')

        if elements[0] not in [bet_cls.name for bet_cls in BETS]:
            raise ValueError(f'invalid strategy name - {elements[0]}')

        config = {
            'strategy': elements[0],
            'pattern': cls.roulette.get_bet_pattern(elements[1]),
            'size': elements[2],
            'types': [cls.roulette.validate_bet_type(x) for x in elements[3].split(':')],
            'limit_lose': elements[4] if len(elements) >= 4 else 0,
            'limit_win': elements[5] if len(elements) >= 5 else 0
        }

        return config

    def set_bets(self, numbers):
        for config in self.bet_configs:
            name = config['strategy']
            config['size'] = config['size']

            if self.roulette.is_pattern_match(config['pattern'], numbers):
                bet = get_bet(name, **config)
                self.bets.append(bet)
