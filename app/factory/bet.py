from app.bet.homerun import BetHomerun
from app.bet.martingale import BetMartingale
from app.bet.paroli import BetParoli
from app.bet.simple import BetSimple


class BetFactory(object):
    bet_mapping = {
        'simple': BetSimple, 'martingale': BetMartingale, 'paroli': BetParoli, 'homerun': BetHomerun
    }

    def __init__(self):
        self.bets = []

    def set_bet(self, name, **kwargs):
        self.bets.append(self.bet_mapping[name](**kwargs))

    @classmethod
    def validate_bet_strategy(cls, name) -> None:
        if name not in cls.bet_mapping.keys():
            raise ValueError('invalid bet strategy name - {}'.format(name))
