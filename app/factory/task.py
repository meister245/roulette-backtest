from app.strategy.martingale import StrategyMartingale

from lib.betfair import Betfair


class TaskFactory(object):
    strategy_mapping = {'martingale': StrategyMartingale}
    casino_mapping = {'betfair': Betfair}

    def __init__(self, config):
        self.config = config

    def get_casino(self, casino_name):
        if casino_name.lower() not in self.config.casino.keys():
            exit('invalid casino name - {}'.format(casino_name))

        obj = TaskFactory.casino_mapping[casino_name]
        return obj(self.config.casino[casino_name]['api_url'])

    def generate_strategy_object(self, strategy_name):
        if strategy_name.lower() not in self.config.strategies:
            exit('invalid strategy name - {}'.format(strategy_name))

        obj = TaskFactory.strategy_mapping[strategy_name]
        return obj(self.config.backtest)
