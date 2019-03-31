class ResultStore(object):
    row_top = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
    row_middle = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
    row_bottom = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
    black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 25, 30, 32, 34, 36]

    def __init__(self):
        self.results = []

    def process(self, number, bet_type, bet_amount, balance):
        win = self.eval_number(number, bet_type, bet_amount)
        status = 'win' if win > 0 else 'lost'

        result = {'number': number, 'win': win, 'balance': balance,
                  'status': status, 'bet_amount': bet_amount, 'bet_type': bet_type}

        self.results.append(result)

        return result

    @classmethod
    def eval_number(cls, number, bet_type, bet_amount):
        win = 0

        if bet_type == 'red' and number in cls.red_numbers:
            win += bet_amount * 2

        elif bet_type == 'black' and number in cls.black_numbers:
            win += bet_amount * 2

        elif bet_type == 'even' and number != 0 and number % 2 == 0:
            win += bet_amount * 2

        elif bet_type == 'odd' and number % 2 == 1:
            win += bet_amount * 2

        elif bet_type == 'half_left' and 1 <= number <= 18:
            win += bet_amount * 2

        elif bet_type == 'half_right' and 19 <= number <= 36:
            win += bet_amount * 2

        elif bet_type == 'row_top' and number in cls.row_top:
            win += bet_amount * 3

        elif bet_type == 'row_middle' and number in cls.row_middle:
            win += bet_amount * 3

        elif bet_type == 'row_bottom' and number in cls.row_bottom:
            win += bet_amount * 3

        elif bet_type == 'column_left' and 1 <= number <= 12:
            win += bet_amount * 3

        elif bet_type == 'column_middle' and 13 <= number <= 22:
            win += bet_amount * 3

        elif bet_type == 'column_right' and 23 <= number <= 36:
            win += bet_amount * 3

        return win
