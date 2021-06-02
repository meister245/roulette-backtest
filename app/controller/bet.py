from ..bet import get_bet
from ..roulette import Roulette


class BetController:
    roulette = Roulette()

    def __init__(self):
        self.bets = []
        self.results = []
        self.configs = []

    def run_simulation(self, numbers, **kwargs):
        balance = kwargs.pop('balance', 1000.0)

        for idx, number in enumerate(numbers):
            current_numbers = [x['number'] for x in self.results]

            for config in self.configs:
                active_bets = self.get_bets_active()

                if len(active_bets) >= config['concurrentBetsLimit']:
                    break

                if self.is_strategy_match(config, current_numbers):
                    bet_obj = get_bet(config)
                    self.bets.append(bet_obj)

            if self.get_bets_total_size() > balance:
                break

            bet_results = []

            for bet_obj in self.get_bets_active():
                result = bet_obj.run_bet(number, **kwargs)

                result['spin'] = idx + 1
                balance += result['profit']

                bet_results.append(result)

            self.results.append(
                {'results': bet_results, 'balance': balance, 'number': number})

        return tuple(self.results)

    def get_bets_active(self):
        return [bet for bet in self.bets if bet.status == bet.STATUS_ACTIVE]

    def get_bets_total_size(self):
        return sum([bet.size_current for bet in self.get_bets_active()])

    def is_strategy_match(self, config, numbers):
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
