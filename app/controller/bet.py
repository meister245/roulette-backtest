from ..bet import Bet
from ..roulette import Roulette


class BetController:
    roulette = Roulette()

    MODE_NORMAL = 'normal'
    MODE_SUSPENDED = 'suspended'

    def __init__(self):
        self.configs = []
        self.results = []

        self.active_bet = None
        self.progression_count = 1

        self.last_bet_strategy = None

        self.mode = self.MODE_NORMAL

    def run_simulation(self, numbers, **kwargs):
        balance = kwargs.pop('balance', 1000.0)

        for idx, number in enumerate(numbers):
            result, current_numbers = {}, numbers[:idx]

            if self.active_bet is None:
                self.active_bet = self.get_next_bet(current_numbers)

            if self.active_bet and self.active_bet.size_current < balance:
                progression_count = int(self.progression_count)
                result = self.active_bet.run(number, progression_count, **kwargs)

                if self.active_bet.status == self.active_bet.STATUS_ACTIVE:
                    self.progression_count += 1

                elif self.active_bet.status == self.active_bet.STATUS_COMPLETE:
                    self.progression_count = 1

                if self.active_bet and self.active_bet.status == self.active_bet.STATUS_COMPLETE:
                    self.mode = self.MODE_NORMAL
                    self.last_bet_strategy = None

                if self.active_bet and self.active_bet.status == self.active_bet.STATUS_SUSPENDED:
                    self.mode = self.MODE_SUSPENDED
                    self.last_bet_strategy = str(self.active_bet.strategy_name)

                if self.active_bet and self.active_bet.status != self.active_bet.STATUS_ACTIVE:
                    self.active_bet = None

                balance += result['profit']

            self.results.append(
                {'results': result, 'balance': balance, 'number': number, 'spin': idx + 1})

        return tuple(self.results)

    def get_next_bet(self, current_numbers):
        for config in self.configs:
            if self.is_strategy_match(config, current_numbers):
                return Bet(config=config)

        return None

    def is_strategy_match(self, config, numbers):
        if self.mode == self.MODE_SUSPENDED:
            parents = config['trigger'].get('parent', [])

            if self.last_bet_strategy not in parents:
                return False

        if 'pattern' in config['trigger']:
            matched = self.roulette.is_pattern_match(
                config['trigger']['pattern'], numbers)

            if not matched:
                return False

        if 'distribution' in config['trigger']:
            matched = self.roulette.is_distribution_match(
                config['trigger']['distribution'], numbers
            )

            if not matched:
                return False

        return True
