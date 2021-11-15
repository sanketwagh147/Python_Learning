
class Ticker_NSE:
    def __init__(self):
        self.ltp = 1
        self.open = 2
        self.close = 3
        self.high = 4


class Ticker_BSE:
    def __init__(self):
        self.ltp = 11
        self.open = 132
        self.close = 132132
        self.high = 123
        self.low = 151
class Exchannge:


    def __init__(self):
        self.nse = Ticker_NSE()
        self.bse = Ticker_BSE()

it = Exchannge()


print(it.nse.ltp)
print(it.nse.ltp)
print(it.bse.close)
print(it.bse.ltp)
