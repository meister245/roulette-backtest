from app.factory.task import TaskFactory


class ServiceController(object):
    def __init__(self, config):
        self.config = config

        self.factory = TaskFactory(config)

    def run_strategy_test(self):
        strategy_obj = self.factory.generate_strategy_object(self.config.params['strategy'])
        strategy_obj.run(self.config.params)

    def run_data_collection(self):
        raise NotImplementedError()
