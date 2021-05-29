from .simple import BetSimple


class BetParoli(BetSimple):
    name = 'paroli'

    def __init__(self, config):
        BetSimple.__init__(self, config)

    def update_bet_size(self, result, **kwargs):
        table_limit = kwargs.get('tableLimit', 150.0)

        if result['win'] and self.size_current * self.config['progressionMultiplier'] <= table_limit:
            self.size_current *= self.config['progressionMultiplier']

        elif result['win'] and self.size_current * self.config['progressionMultiplier'] > table_limit:
            pass

        elif not result['win']:
            self.size_current = self.size_original
