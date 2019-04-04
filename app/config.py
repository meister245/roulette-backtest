import os
import json

from app.model.result import ResultModel


class Config(object):
    bet_types = ResultModel.bet_mapping.keys()
    strategies = ['martingale', 'paroli', 'dalembert', 'fibonacci', 'james_bond']

    def __init__(self, src_dir):
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
