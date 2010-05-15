from common import *

# offset describes the number of periods the second name lags the first

def correlate(x, y, offset=0):
    '''return correlation of x with offset y'''
    if offset > 0:
        x_ = x[:-offset]
        y_ = y[offset:]
    if offset < 0:
        offset = -offset
        x_ = x[offset:]
        y_ = y[:-offset]
    if offset == 0:
        x_ = x
        y_ = y
    return np.corrcoef(x_, y_)[0,1]

def main():
    correlations0 = []
    correlations1 = []
    correlations2 = []
    with h5py.File(filename) as root:
        for trade_date in list(root)[start_day:end_day]:
            names = root[trade_date]["names"].value
            prices = root[trade_date]["prices"].value
            epoch_times = root[trade_date]["dates"].value
            yields = np.diff(np.log(prices), axis=0)
            # [SPY, VXX] for this hdf5 file
            SPY_prices = yields[:, 0]
            VXX_prices = yields[:, 1]
            correlations0.append(correlate(SPY_prices, VXX_prices, offset=0))
            correlations1.append(correlate(SPY_prices, VXX_prices, offset=1))
            correlations2.append(correlate(SPY_prices, VXX_prices, offset=2))
    pyplot.plot(correlations0)
    pyplot.plot(correlations1)
    pyplot.plot(correlations2)
    pyplot.show()

if __name__ == "__main__":
    main()
