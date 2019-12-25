from ..model.bet import BetModel


class BetSimple(BetModel):
    def __init__(self, **kwargs):
        BetModel.__init__(self, **kwargs)
