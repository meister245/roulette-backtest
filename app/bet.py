from typing import Tuple

from .roulette import Roulette


class Bet:
    roulette = Roulette()

    STATUS_ACTIVE = 'active'
    STATUS_COMPLETE = 'complete'
    STATUS_SUSPENDED = 'suspended'

    def __init__(self, config, bet_size=0):
        self.config = config

        self.size_original = float(config['chipSize'])
        self.strategy_name = str(config['strategyName'])

        self.size_current = bet_size if bet_size > 0 else float(
            config['chipSize'])

        self.limits = {
            'win': int(config['limits'].get('stopWin', 0)),
            'lose': int(config['limits'].get('stopLoss', 0)),
            'suspend': int(config['limits'].get('suspendLoss', 0))
        }

        self.results = {
            'win': 0,
            'lose': 0
        }

        self.status = self.STATUS_ACTIVE

    def run(self, number, **kwargs):
        result = self.get_bet_result(number)

        if result['success']:
            self.results['win'] += 1

        elif not result['success']:
            self.results['lose'] += 1

        if result['size'] > 0:
            self.update_bet_size(result, **kwargs)

        self.update_bet_status()

        return result

    def update_bet_status(self):
        if self.limits['lose'] != 0 and self.results['lose'] == self.limits['lose']:
            self.status = self.STATUS_COMPLETE

        elif self.limits['win'] != 0 and self.results['win'] == self.limits['win']:
            self.status = self.STATUS_COMPLETE

        elif self.limits['suspend'] != 0 and self.results['lose'] == self.limits['suspend']:
            self.status = self.STATUS_SUSPENDED

    def update_bet_size(self, result, **kwargs):
        table_limit = kwargs.get('tableLimit', 150.0)

        if result['success']:
            self.size_current = self.size_original

        elif not result['success']:
            new_size = self.size_current * self.config['progressionMultiplier']

            if new_size <= table_limit:
                self.size_current = new_size

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
            'success': win_loss,
            'strategy': self.strategy_name
        }

        return result
