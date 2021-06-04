from ..bet import get_bet
from ..roulette import Roulette


class BetController:
    roulette = Roulette()

    MODE_NORMAL = 'normal'
    MODE_SUSPENDED = 'suspended'

    def __init__(self):
        self.configs = []
        self.results = []

        self.active_bet = None
        self.last_bet_size = 0

        self.mode = self.MODE_NORMAL

    def run_simulation(self, numbers, **kwargs):
        balance = kwargs.pop('balance', 1000.0)

        for idx, number in enumerate(numbers):
            result, current_numbers = {}, numbers[:idx]

            if self.active_bet is None:
                self.active_bet = self.get_next_bet(current_numbers)

            if self.active_bet and self.active_bet.size_current < balance:
                result = self.active_bet.run(number, **kwargs)

                if self.active_bet and self.active_bet.status == self.active_bet.STATUS_COMPLETE:
                    self.last_bet_size = 0
                    self.mode = self.MODE_NORMAL

                if self.active_bet and self.active_bet.status == self.active_bet.STATUS_SUSPENDED:
                    self.last_bet_size = float(self.active_bet.size_current)
                    self.mode = self.MODE_SUSPENDED

                if self.active_bet and self.active_bet.status != self.active_bet.STATUS_ACTIVE:
                    self.active_bet = None

                balance += result['profit']

            self.results.append(
                {'results': result, 'balance': balance, 'number': number, 'spin': idx + 1})

        return tuple(self.results)

    def get_next_bet(self, current_numbers):
        for config in self.configs:
            if self.is_strategy_match(config, current_numbers):
                return get_bet(config=config, bet_size=float(self.last_bet_size))

        return None

    def is_strategy_match(self, config, numbers):
        if self.mode == self.MODE_SUSPENDED and 'suspended' not in config['trigger']:
            return False

        if 'pattern' in config['trigger']:
            matched = self.roulette.is_pattern_match(
                config['trigger']['pattern'], numbers)

            if not matched:
                return False

        if 'distribution' in config['trigger']:
            bet_type, sample_size, percentage, action = config['trigger']['distribution']

            matched = self.roulette.is_distribution_match(
                bet_type, action, percentage, numbers, n=sample_size
            )

            if not matched:
                return False

        return True
