import os
import json


class Config(object):
    bet_types = ['red', 'black', 'row_top', 'row_middle', 'row_bottom', 'column_left', 'column_middle',
                 'column_right', 'even', 'odd', 'half_left', 'half_right']

    bet_types.extend(['number_{}'.format(x) for x in range(36)])

    strategies = ['martingale', 'paroli', 'd_alembert', 'fibonacci', 'james_bond']

    def __init__(self, src_dir):
        self.params = None
        self.backtest = None

        self.src_dir = src_dir
        self.resource_dir = self.get_resources_dir(src_dir)

        self.casino = self.get_application_config('casino')
        self.logging = self.get_application_config('logging')

    @staticmethod
    def get_resources_dir(src_dir):
        if os.path.isdir(src_dir + '/resources'):
            return os.path.realpath(src_dir + '/resources')

        else:
            exit('resources directory not found')

    def get_application_config(self, key_name=None):
        app_config_path = self.resource_dir + '/config/application_config.json'

        try:
            with open(os.path.realpath(app_config_path), 'r') as f:
                config = json.loads(f.read())

            return config if key_name is None else config[key_name]

        except (OSError, KeyError) as e:
            exit('error occured during loading config: {}'.format(str(e)))

    def get_backtest_file(self, file_name):
        file_path = self.resource_dir + '/backtest/{}'.format(file_name)

        try:
            with open(os.path.relpath(file_path)) as f:
                return f.read()

        except OSError:
            exit('invalid path for backtest file: {}'.format(file_path))

    def set_params(self, type, **kwargs):
        if type == 'test':
            self.set_test_params(**kwargs)

        elif type == 'collect':
            self.set_collection_params(**kwargs)

        else:
            exit('invalid type - {}'.format(type))

    def set_test_params(self, **kwargs):
        self.params = {
            'mode': kwargs['mode'],
            'strategy': kwargs['strategy'],
            'bet_type': kwargs['bet_type'],
            'bet_amount': round(kwargs.get('bet_amount', 0.20), 2),
            'balance': round(kwargs.get('balance', 500), 2),
            'table_limit': round(kwargs.get('table_limit', 150), 2),
            'cycles': kwargs.get('cycles', 100)
        }

        file_name = kwargs.get('backtest', None)

        if isinstance(file_name, str):
            self.backtest = self.get_backtest_file(file_name).split(',')

    def set_collection_params(self, **kwargs):
        self.params = {
            'casino': kwargs['casino'],
            'collect': kwargs.get('collect', 100)
        }
