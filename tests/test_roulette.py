from app.roulette import Roulette

import pytest


@pytest.fixture(scope='class')
def roulette():
    return Roulette()


class TestRouletteController:
    def test_is_pattern_match(self, roulette):
        assert roulette.is_pattern_match(('red', 'red'), (1, 1))
        assert roulette.is_pattern_match(('straight_1', 'straight_1'), (2, 2, 1, 1))
        assert roulette.is_pattern_match(('four', 'corner_1_2_4_5', 'high'), (1, 5, 6, 22, 0, 4, 36))

        assert roulette.is_pattern_match(('any',), (1, 1))
        assert roulette.is_pattern_match(('straight_22', 'any', 'black'), (22, 1, 2))

        assert not roulette.is_pattern_match(('red', 'red', 'red'), (1, 1))
        assert not roulette.is_pattern_match(('red', 'red', 'red'), (1, 1, 2))

        with pytest.raises(ValueError):
            roulette.is_pattern_match(('asd', 'asd'), (1, 1))

    def test_get_bet_types(self, roulette):
        assert len(roulette.get_bet_types()) == 153

    def test_get_bet_pattern(self, roulette):
        assert roulette.get_bet_pattern('four:red:black') == ('black', 'red', 'four')

        with pytest.raises(ValueError):
            roulette.get_bet_pattern(':')
            roulette.get_bet_pattern('black:four:')

    def test_get_win_types(self, roulette):
        assert 'straight_0' in roulette.get_win_types(0)
        assert 'four' in roulette.get_win_types(0)
        assert 'red' in roulette.get_win_types(1)
        assert 'black' in roulette.get_win_types(2)
        assert 'any' in roulette.get_win_types(1)

    def test_get_win_types_all(self, roulette):
        assert len(roulette.get_win_types_all()) == 37

    def test_validate_bet_type(self, roulette):
        roulette.validate_bet_type('red')
        roulette.validate_bet_type('dozen_first')
        roulette.validate_bet_type('column_top')
        roulette.validate_bet_type('straight_0')
        roulette.validate_bet_type('split_1_2')
        roulette.validate_bet_type('street_1_2_3')
        roulette.validate_bet_type('corner_1_2_4_5')
        roulette.validate_bet_type('line_1_2_3_4_5_6')

        with pytest.raises(ValueError):
            roulette.validate_bet_type('orange')
