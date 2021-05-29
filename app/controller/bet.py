from ..bet import get_bet
from ..roulette import Roulette


class BetController:
    roulette = Roulette()

    def __init__(self):
        self.bets = []
        self.results = []
        self.configs = []

    def get_bets_active(self):
        return [bet for bet in self.bets if bet.is_bet_active()]

    def get_bets_total_size(self):
        total_size = 0

        for bet in self.bets:
            total_size += bet.size_current if bet.is_bet_active() else 0

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

    def set_bets(self, numbers):
        for config in self.configs:
            matched = False

            if 'pattern' in config['trigger']:
                matched = self.roulette.is_pattern_match(
                    config['trigger']['pattern'], numbers)

                if not matched:
                    continue

            if 'distribution' in config['trigger']:
                bet_type, sample_size, percentage, action = config['trigger']['distribution']

                matched = self.roulette.is_distribution_match(
                    bet_type, action, percentage, numbers, n=sample_size
                )

                if not matched:
                    continue

            if matched and len(self.get_bets_active()) < config['concurrentBetsLimit'] :
                self.bets.append(get_bet(config))
