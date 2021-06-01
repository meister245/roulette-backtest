from typing import Tuple

from ..roulette import Roulette


class BetSimple:
    name = 'simple'
    roulette = Roulette()

    def __init__(self, config):
        self.config = config

        self.size_current = float(config['chipSize'])
        self.size_original = float(config['chipSize'])

        self.limits = {
            'win': int(config.get('stopWinLimit', 0)),
            'lose': int(config.get('stopLossLimit', 0))
        }

        self.results = {
            'win': 0,
            'lose': 0
        }

    def run_bet(self, number, **kwargs):
        result = self.get_bet_result(number)

        if result['success']:
            self.results['win'] += 1

        elif not result['success']:
            self.results['lose'] += 1

        if result['size'] > 0:
            self.update_bet_size(result, **kwargs)

        return result

    def is_bet_active(self):
        if self.limits['lose'] != 0 and self.results['lose'] == self.limits['lose']:
            return False

        if self.limits['win'] != 0 and self.results['win'] == self.limits['win']:
            return False

        return True

    def get_bet_profit(self, number) -> Tuple[bool, float]:
        profit, win_types = 0, self.roulette.get_win_types(number)

        for bet_type in self.config['bets']:
            if bet_type in win_types:
                bet_type = bet_type.split('-', 1).pop(0)
                payout_multiplier = self.roulette.payout_mapping[bet_type]

                profit += self.size_current * payout_multiplier

            else:
                profit -= self.size_current

        status = True if profit > 0 else False if profit < 0 else None

        return status, round(profit, 2)

    def get_bet_result(self, number: int) -> dict:
        win_loss, profit = self.get_bet_profit(number)

        result = {
            'size': float(self.size_current),
            'profit': profit,
            'type': self.config['bets'],
            'success': win_loss
        }

        return result

    def update_bet_size(self, result, **kwargs):
        table_limit = kwargs.get('tableLimit', 150.0)

        if self.size_current < table_limit:
            self.size_current = self.size_current

        else:
            self.size_current = table_limit
