from app.strategy.martingale import StrategyMartingale
from app.strategy.paroli import StrategyParoli
from app.strategy.simple import StrategySimple


class StrategyFactory(object):
    strategy_mapping = {
        'martingale': StrategyMartingale, 'paroli': StrategyParoli, 'simple': StrategySimple
    }

    def __init__(self):
        self.martingale = StrategyMartingale()
        self.paroli = StrategyParoli()
        self.simple = StrategySimple()

    def get_strategy(self, strategy_name):
        if strategy_name.lower() not in self.strategy_mapping.keys():
            exit('invalid strategy name - {}'.format(strategy_name))

        return getattr(self, strategy_name)
