import random
from typing import Union

from app.model.bet import BetModel


class ResultModel(object):
    bet_model = BetModel()

    __slots__ = ['results', 'backtest', 'numbers']

    def __init__(self, **kwargs):
        self.results = []
        self.backtest = kwargs.get('backtest', None)

    def get_result(self, number: int, bets: list, balance: float, **kwargs) -> [float, dict]:
        bets_sum = self.bet_model.get_bets_sum(bets)
        win_types = self.bet_model.get_win_bet_types(number)
        bets_result = self.bet_model.get_bets_result(bets, win_types)

        profit = self.calculate_profit(bets_result)
        status = 'W' if profit > 0 else 'L' if profit < 0 else None

        result = {
            'number': number,
            'balance_start': balance,
            'balance_close': round(balance + profit, 2),
            'bet_amount': bets_sum,
            'bet_result': bets_result,
            'profit': profit,
            'status': status,
            'win_types': win_types
        }

        self.results.append(result)

        bets = self.bet_model.update_bets(bets, result, self.results, **kwargs)

        return result['balance_close'], bets

    @classmethod
    def calculate_profit(cls, bets_result: Union[type(None), dict]) -> float:
        if bets_result is None:
            return 0

        profit = 0 - sum([x['bet_amount'] for x in bets_result])

        for x in bets_result:
            if x['win']:
                name = x['bet_type'].split('_', 1).pop(0)
                profit += x['bet_amount']
                profit += x['bet_amount'] * cls.bet_model.payout_mapping[name]

        return round(profit, 2)

    def get_next_number(self, idx):
        try:
            if self.backtest is None:
                return random.randint(0, 36)

            else:
                return self.backtest[idx]

        except IndexError:
            exit('insufficient backtest numbers to complete simulation')
