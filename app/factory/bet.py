from ..model.martingale import BetMartingale
from ..model.paroli import BetParoli
from ..model.simple import BetSimple


class BetFactory(object):
    bet_mapping = {
        'simple': BetSimple, 'martingale': BetMartingale, 'paroli': BetParoli
    }

    @classmethod
    def get_bet(cls, name, **kwargs):
        cls.validate_bet_strategy(name)
        return cls.bet_mapping[name](**kwargs)

    @classmethod
    def validate_bet_strategy(cls, name) -> None:
        if name not in cls.bet_mapping.keys():
            raise ValueError(f'invalid model strategy name - {name}')
