from typing import Tuple

from .roulette import Roulette


class Bet:
    roulette = Roulette()

    STATUS_ACTIVE = 'active'
    STATUS_COMPLETE = 'complete'
    STATUS_SUSPENDED = 'suspended'

    def __init__(self, config):
        self.config = config

        self.last_result = None
        self.status = self.STATUS_ACTIVE
        self.strategy_name = str(config['strategyName'])

        self.size_current = 0

        self.limits = {
            'win': int(config['limits'].get('stopWin', 0)),
            'lose': int(config['limits'].get('stopLoss', 0)),
            'suspend': int(config['limits'].get('suspendLoss', 0))
        }

        self.bet_results = {
            'win': 0,
            'lose': 0
        }

    def run(self, number, progression_count, **kwargs):
        self.update_bet_size(progression_count, **kwargs)

        result = self.get_bet_result(number)

        self.update_bet_results(result)
        self.update_bet_status()

        self.last_result = result

        return result

    def update_bet_results(self, result):
        if result['success']:
            self.bet_results['win'] += 1

        elif not result['success']:
            self.bet_results['lose'] += 1

    def update_bet_status(self):
        if self.limits['lose'] != 0 and self.bet_results['lose'] == self.limits['lose']:
            self.status = self.STATUS_COMPLETE

        elif self.limits['win'] != 0 and self.bet_results['win'] == self.limits['win']:
            self.status = self.STATUS_COMPLETE

        elif self.limits['suspend'] != 0 and self.bet_results['lose'] == self.limits['suspend']:
            self.status = self.STATUS_SUSPENDED

    def update_bet_size(self, progression_count, **kwargs):
        table_limit = kwargs.get('tableLimit', 150.0)
        self.size_current = self.config['progression'][progression_count - 1]

        if self.size_current > table_limit:
            self.size_current = table_limit

    def get_bet_profit(self, number) -> Tuple[bool, float]:
        is_any_bet_winning = False
        profit, win_types = 0, self.roulette.get_win_types(number)

        for bet_type in self.config['bets']:
            if bet_type in win_types:
                is_any_bet_winning = True
                bet_type = bet_type.split('-', 1).pop(0)
                payout_multiplier = self.roulette.payout_mapping[bet_type]

                profit += self.size_current * payout_multiplier

            else:
                profit -= self.size_current

        status = True if profit > 0 else False if profit < 0 else None

        if status is None and is_any_bet_winning:
            status = True

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
