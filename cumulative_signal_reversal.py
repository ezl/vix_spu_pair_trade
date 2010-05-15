from common import *

def backtest_one_day(SPY, VXX, previous_day_std, leb=4, ueb=7, msr=1):
    '''
    initial backtest. use spy as an indicator for VXX. if spy 15 second yield is
    between $leb and $ueb standard deviations of its previous day's 15 second yields,
    then trade one unit of VXX.

    exit if the trade has moved msr units against you. "against" == if long VXX, positive
    SPY yields or if short VXX, negative SPY yields

    only have to trade one name, which is quite nice.
    '''
    trade_notional = 1.0
    lower_bound = leb
    upper_bound = ueb
    max_signal_reversal = msr

    pnl =[]
    transaction_cost = []
    pos = 0
    trade_count = 0
    signal_reversal = 0
    SPY_yields = np.hstack((0, np.diff(np.log(SPY))))
    VXX_yields = np.hstack((0, np.diff(np.log(VXX))))

    for i in range(len(SPY)):
        std = previous_day_std
        pnl.append(pos * VXX_yields[i])
        pos += pnl[-1]
        if lower_bound < abs(SPY_yields[i]) / std < upper_bound:
            desired_pos = -cmp(SPY_yields[i], 0) * trade_notional
            if not cmp(desired_pos, 0) * cmp(pos, 0) == 1:
                shares_transacted = abs((desired_pos - pos) / VXX[i])
                pos = desired_pos
                transaction_cost.append(cost_per_share * shares_transacted)
                signal_reversal = 0
                trade_count += 1
        if (pos > 0 and SPY_yields[i] > 0) or \
           (pos < 0 and SPY_yields[i] < 0):
            signal_reversal += abs(SPY_yields[i])
        elif not pos == 0:
            signal_reversal += -abs(SPY_yields[i])
            if signal_reversal < 0:
                signal_reversal = 0

        if (signal_reversal / std > max_signal_reversal):
            shares_transacted = abs(pos) / VXX[i]
            transaction_cost.append(cost_per_share * shares_transacted)
            trade_count += 1
            pos = 0
            signal_reversal = 0

    # close position out at end of day no matter what
    if not pos == 0:
        transaction_cost[-1] += abs(pos / VXX[i]) * (cost_per_share * 1)

    return sum(pnl), sum(transaction_cost), trade_count

def backtest_period(plot=False, f=None, **kwargs):
    with h5py.File(filename) as root:
        pnl = list()
        cost = list()
        VXX_close = list()
        VXX_vol = list()
        SPY_close = list()
        trade_count = list()
        lagging_correlation = list()
        threshold = 0.00015
        for trade_date in list(root)[start_day:end_day]:
            # print trade_date
            names = root[trade_date]["names"].value
            SPY = root[trade_date][("prices")].value[:, 0][:]
            SPY_close.append(SPY[-1])
            VXX = root[trade_date][("prices")].value[:, 1][:]
            VXX_close.append(VXX[-1])
            epoch_times = root[trade_date]["dates"].value
            raw_profit, raw_cost, tc = backtest_one_day(SPY, VXX,
                                                        threshold, **kwargs)
            pnl.append(raw_profit)
            cost.append(raw_cost)
            trade_count.append(tc)
            VXX_vol.append(np.std(np.diff(np.log(VXX))))
            lagging_correlation.append(correlate(SPY, VXX, offset=1))
            threshold = np.std(np.diff(np.log(SPY)))
        running_pnl = np.cumsum(pnl)
        running_cost = np.cumsum(cost)
        running_net = running_pnl - running_cost
        pnl = np.array(pnl)
        cost = np.array(cost)
        total_pnl = sum(pnl)
        total_cost = sum(cost)

        print "Net:%s," % (total_pnl - total_cost),
        print "Trade:%s," % total_pnl,
        print "Cost:%s," % total_cost,
        print "Avg:%s," % (np.mean(pnl) - np.mean(cost)),
        print "Std:%s," % np.std(pnl - cost),
        print "Trades/Day:%s," % np.mean(trade_count),
        for key in kwargs:
            print "%s:%s," % (key, kwargs[key]),
        print

        if not f is None:
            f.write("Net:%s," % (total_pnl - total_cost))
            f.write("Trade:%s," % total_pnl)
            f.write("Cost:%s," % total_cost)
            f.write("Avg:%s," % (np.mean(pnl) - np.mean(cost)))
            f.write("Std:%s," % np.std(pnl - cost))
            f.write("Trades/Day:%s," % np.mean(trade_count),)
            for key in kwargs:
                f.write("%s:%s," % (key, kwargs[key]))
            f.write("\n")

        if plot==True:
            ax1 = pyplot.subplot(3, 2, 1)
            pyplot.plot(VXX_close, "r")
            ax1.set_ylabel("V (red)")
            ax2 = pyplot.twinx()
            pyplot.plot(SPY_close, "k")
            ax2.set_ylabel("S (black)")
            pyplot.title("V and S Closing Px")

            pyplot.subplot(3, 2, 3)
            pyplot.plot(pnl)
            pyplot.plot(cost)
            pyplot.title("PnL v cost")

            pyplot.subplot(3, 2, 2)
            pyplot.plot(running_pnl)
            pyplot.plot(running_cost)
            pyplot.title("Running PnL v Cost")

            pyplot.subplot(3, 2, 4)
            pyplot.plot(running_net)
            pyplot.title("Running Net")

            pyplot.subplot(3, 2, 5)
            pyplot.plot(trade_count)
#            pyplot.bar(range(len(trade_count)), trade_count)
            pyplot.title("Trade Count")

            pyplot.subplot(3, 2, 6)
            pyplot.plot(lagging_correlation)
            pyplot.title("Correlation (1 period lag)")

#             pyplot.subplot(3, 2, 6)
#             pyplot.plot(VXX_vol)
#             pyplot.title("VXX vol")
            pyplot.show()

if __name__ == "__main__":
    backtest_period(leb=5,
                    ueb=8,
                    msr=9,
                    plot=True)

if __name__ == "__main_dd_":
    pairs = [(0, 245),
             (0, 120),
             (120, 245),
             (0, 60),
             (60, 120),
             (120, 180),
             (180, 245),
             (0, 30),
             (30, 60),
             (60, 90),
             (90, 120),
             (120, 150),
             (150, 180),
             (180, 210),
             (210, 245),]
    for start_day, end_day in pairs:
        outfile = "CSR_%s_%s.csv" % (start_day, end_day)
        print outfile
        with file(outfile, "w") as f:
            for lower_entry_bound in range(3,8):
                for upper_entry_bound in range(lower_entry_bound + 1, 10):
                    for max_signal_reversal in range(10):
                        backtest_period(f=f,
                                        leb=lower_entry_bound,
                                        ueb=upper_entry_bound,
                                        msr=max_signal_reversal)
