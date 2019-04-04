import time
import collections

from app.factory.task import TaskFactory


class ServiceController(object):
    def __init__(self, config):
        self.config = config

        self.factory = TaskFactory(config)

    def run_strategy_test(self, bets: dict, mode: str, strategy: str, **kwargs) -> None:
        strategy_obj = self.factory.generate_strategy_object(strategy)

        if mode == 'single':
            self.run_strategy_test_single(strategy_obj, bets, **kwargs)

        elif mode == 'aggregate':
            self.run_strategy_test_aggregate(strategy_obj, bets, **kwargs)

        else:
            exit('invalid game mode - {}'.format(self.config.params['mode']))

    def run_strategy_test_single(self, strategy_obj, bets, **kwargs):
        store = strategy_obj.run_single(bets, **kwargs)
        store.print_result_summary()
        store.print_result_details()

    def run_strategy_test_aggregate(self, strategy_obj, bets, **kwargs):
        result_summaries = strategy_obj.run_aggregate(bets, **kwargs)
        results = strategy_obj.get_aggregated_result_summary(result_summaries)
        strategy_obj.print_aggregated_result_summary(results)

    def run_data_collection(self, **kwargs):
        numbers = {}

        casino_obj = self.factory.get_casino(kwargs['casino'])
        table_name = self.config.casino[kwargs['casino']]['table_name']
        backtest_dir = self.config.resource_dir + '/backtest'

        file_name = '{}_{}_{}'.format(
            kwargs['casino'], int(kwargs['collect']), int(time.time())
        )

        while True:
            current_numbers = {x['ts']: x['number'] for x in casino_obj.get_table_results(table_name)}

            for k in current_numbers.keys():
                if k not in numbers.keys():
                    numbers[k] = current_numbers[k]

            with open(backtest_dir + '/{}'.format(file_name), 'w') as f:
                sorted_dict = collections.OrderedDict(sorted(numbers.items()))
                f.write(','.join([str(x) for x in sorted_dict.values()]))

            if len(numbers) >= kwargs['collect']:
                break

            time.sleep(60)

        print('finished collecting')
