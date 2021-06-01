from .simple import BetSimple


class BetMartingale(BetSimple):
    name = 'martingale'

    def __init__(self, config):
        BetSimple.__init__(self, config)

    def update_bet_size(self, result, **kwargs):
        table_limit = kwargs.get('tableLimit', 150.0)

        if result['success']:
            self.size_current = self.size_original

        elif not result['success'] and self.size_current * self.config['progressionMultiplier'] <= table_limit:
            self.size_current *= self.config['progressionMultiplier']

        elif not result['success'] and self.size_current * self.config['progressionMultiplier'] > table_limit:
            pass
