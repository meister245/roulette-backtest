from ..bet import get_bet, BETS
from ..roulette import Roulette


class BetController:
    roulette = Roulette()

    def __init__(self):
        self.bets = []
        self.results = []
        self.bet_configs = []

    def get_bets_total_size(self):
        total_size = 0

        for x in self.bets:
            total_size += x.size_current if x.is_bet_active() else 0

        return total_size

    def run_simulation(self, numbers, **kwargs):
        balance = kwargs.pop('balance', 1000.0)

        for idx, number in enumerate(numbers):
            bet_results = []
            current_numbers = [x['number'] for x in self.results]

            self.set_bets(current_numbers)

            if self.get_bets_total_size() > balance:
                break

            for bet in self.bets:
                balance, result = bet.run_bet(number, idx, balance, **kwargs)

                if len(result) != 0:
                    bet_results.append(result)

            self.results.append(
                {'results': bet_results, 'balance': balance, 'number': number})

        return tuple(self.results)

    @classmethod
    def parse_bet_distribution(cls, elements):

        if elements[7] not in ['equal', 'lower_equal', 'higher_equal']:
            raise ValueError(f'invalid distribution action - {elements[7]}')

        if not elements[8].isdigit() or not 0 <= int(elements[8]) <= 100:
            raise ValueError(
                f'invalid distribution percentage - {elements[8]}')

        if not elements[9].isdigit():
            raise ValueError(
                f'invalid distribution sample_size - {elements[9]}')

        return (
            cls.roulette.validate_bet_type(elements[6]),
            elements[7], int(elements[8]), int(elements[9])
        )

    def process_bet_config(self, config: str) -> dict:
        elements = [x for x in config.split(',') if len(x) != 0]

        if len(elements) < 5:
            raise ValueError(f'invalid model config - {config}')

        if elements[0] not in [bet_cls.name for bet_cls in BETS]:
            raise ValueError(f'invalid strategy name - {elements[0]}')

        config = {
            'strategy': elements[0],
            'pattern': self.roulette.get_bet_pattern(elements[1]),
            'size': elements[2],
            'types': [self.roulette.validate_bet_type(x) for x in elements[3].split(':')],
            'limit_lose': elements[4] if len(elements) >= 4 else 0,
            'limit_win': elements[5] if len(elements) >= 5 else 0
        }

        if len(elements) >= 9:
            config['distribution'] = self.parse_bet_distribution(elements)

        self.bet_configs.append(config)

    def set_bets(self, numbers):
        for config in self.bet_configs:
            name = config['strategy']
            config['size'] = config['size']

            matched = None

            if 'pattern' in config:
                matched = self.roulette.is_pattern_match(
                    config['pattern'], numbers)

                if not matched:
                    continue

            if 'distribution' in config:
                bet_type, action, percentage, n = config['distribution']

                matched = self.roulette.is_distribution_match(
                    bet_type, action, percentage, numbers, n=n
                )

                if not matched:
                    continue

            if matched:
                bet = get_bet(name, **config)
                self.bets.append(bet)
