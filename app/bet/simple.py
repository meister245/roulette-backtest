from .common import BetCommon


class BetSimple(BetCommon):
    name = 'simple'

    def __init__(self, **kwargs):
        BetCommon.__init__(self, **kwargs)
