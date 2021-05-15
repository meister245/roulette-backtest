from typing import Tuple

from ..roulette import Roulette


class BetCommon:
    roulette = Roulette()

    def __init__(self, **kwargs):
        self.types = kwargs['types']
        self.size_current = float(kwargs['size'])
        self.size_original = float(kwargs['size'])
        self.limit_win = int(kwargs.get('limit_win', 0))
        self.limit_lose = int(kwargs.get('limit_lose', 0))

        self.win_current = 0
        self.lose_current = 0

    def run_bet(self, number, spin, balance, **kwargs):
        result = {}

        if self.is_bet_active():
            result = self.get_bet_result(number, spin)

            if result['win']:
                self.win_current += 1

            elif not result['win']:
                self.lose_current += 1

            if result['size'] > 0:
                self.update_bet_size(result, **kwargs)

            balance += result['profit']

        return round(balance, 2), result

    def is_bet_active(self):
        if self.limit_lose != 0 and self.lose_current == self.limit_lose:
            return False

        if self.limit_win != 0 and self.win_current == self.limit_win:
            return False

        return True

    def get_bet_profit(self, number) -> Tuple[bool, float]:
        profit = 0 - self.size_current * len(self.types)
        win_types = self.roulette.get_win_types(number)

        for t in self.types:
            if t in win_types:
                name = t.split('_', 1).pop(0)
                profit += round(self.size_current, 2)
                profit += round(self.size_current *
                                self.roulette.payout_mapping[name], 2)

        status = True if profit > 0 else False if profit < 0 else None

        return status, profit

    def get_bet_result(self, number: int, spin: int) -> dict:
        win_loss, profit = self.get_bet_profit(number)

        result = {
            'spin': spin + 1,
            'size': self.size_current,
            'profit': profit,
            'type': self.types,
            'win': win_loss
        }

        return result

    def update_bet_size(self, result, **kwargs):
        table_limit = kwargs.get('table_limit', 150.0)

        if self.size_current < table_limit:
            self.size_current = self.size_current

        else:
            self.size_current = table_limit
