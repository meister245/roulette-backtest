from .martingale import BetMartingale
from .paroli import BetParoli
from .simple import BetSimple

BETS = (
    BetMartingale, BetParoli, BetSimple
)


def get_bet(config, bet_size) -> BETS:
    strategy_name = config.get('strategy')

    for bet_cls in BETS:
        if bet_cls.name == strategy_name:
            return bet_cls(config, bet_size)

    raise ValueError(f'invalid bet strategy name - {strategy_name}')
