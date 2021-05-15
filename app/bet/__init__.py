from .martingale import BetMartingale
from .paroli import BetParoli
from .simple import BetSimple

BETS = (
    BetMartingale, BetParoli, BetSimple
)


def get_bet(name: str, **kwargs) -> BETS:
    for bet_cls in BETS:
        if bet_cls.name == name:
            return bet_cls(**kwargs)

    raise ValueError(f'invalid bet strategy name - {name}')
