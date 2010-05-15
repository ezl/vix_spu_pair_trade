from common import *
from correlation import correlate

def retrieve_preceding_prices(symbol, window_length):
    with h5py.File(filename) as root:
        trade_dates = list(root)
        names = root[trade_dates[0]]["names"].value
        try:
            symbol_index = names.tolist().index(symbol)
        except ValueError, e:
            print "Symbol %s not found." % symbol
            return
        # epoch_times = root[trade_date]["dates"].value
        prices = reduce(lambda x, y: x + y,
                       [root[trade_date][("prices")].value[:, symbol_index][:].tolist() for trade_date in trade_dates]
                       )
        for i in range(len(prices) - window_length + 1):
            yield prices[i:i + window_length]


if __name__ == "__main__":
    window_length = 40
    prices = reduce(lambda x, y: x + y, [p for p in retrieve_preceding_prices("SPY", 1)])
    moving_average = np.array([w for w in retrieve_preceding_prices("SPY", window_length)]).mean
    pyplot.plot(range(len(prices)), prices)
    pyplot.plot(range(window_length, len(prices)), moving_average)
    pyplot.show()
