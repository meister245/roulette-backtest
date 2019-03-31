import time
import collections

from app.factory.task import TaskFactory


class ServiceController(object):
    def __init__(self, config):
        self.config = config

        self.factory = TaskFactory(config)

    def run_strategy_test(self):
        strategy_obj = self.factory.generate_strategy_object(self.config.params['strategy'])

        if self.config.params['mode'] == 'single':
            self.run_strategy_test_single(strategy_obj)

        elif self.config.params['mode'] == 'aggregate':
            self.run_strategy_test_aggregate(strategy_obj)

        else:
            exit('invalid game mode - {}'.format(self.config.params['mode']))

    def run_strategy_test_single(self, strategy_obj):
        results = strategy_obj.run_single(self.config.params)
        strategy_obj.print_result_summary(results)
        strategy_obj.print_result_details(results)

    def run_strategy_test_aggregate(self, strategy_obj):
        results = strategy_obj.run_aggregate(self.config.params)
        strategy_obj.print_aggregated_result_summary(results)

    def run_data_collection(self):
        numbers = {}

        casino_obj = self.factory.get_casino(self.config.params['casino'])
        table_name = self.config.casino[self.config.params['casino']]['table_name']
        backtest_dir = self.config.resource_dir + '/backtest'

        file_name = '{}_{}_{}'.format(
            self.config.params['casino'], int(self.config.params['collect']), int(time.time())
        )

        while True:
            current_numbers = {x['ts']: x['number'] for x in casino_obj.get_table_results(table_name)}

            for k in current_numbers.keys():
                if k not in numbers.keys():
                    numbers[k] = current_numbers[k]

            with open(backtest_dir + '/{}'.format(file_name), 'w') as f:
                sorted_dict = collections.OrderedDict(sorted(numbers.items()))
                f.write(','.join([str(x) for x in sorted_dict.values()]))

            if len(numbers) >= self.config.params['collect']:
                break

            time.sleep(60)

        print('finished collecting')
