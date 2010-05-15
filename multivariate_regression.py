from common import *

def find_model_results(trailing_periods=3, exclude_concurrent=0):
    with h5py.File(filename) as root:
        pnl = list()
        cost = list()
        VXX_close = list()
        VXX_vol = list()
        SPY_close = list()
        trade_count = list()
        coeffs = list()
        R2 = list()
        for trade_date in list(root)[start_day:end_day]:

            # print trade_date
            names = root[trade_date]["names"].value
            SPY = FinancialInstrument(root[trade_date][("prices")].value[:, 0][:])
            VXX = FinancialInstrument(root[trade_date][("prices")].value[:, 1][:])
            epoch_times = root[trade_date]["dates"].value
            independent_var_names = ["SPY-%s" %i for i in range(trailing_periods, -1 + exclude_concurrent, -1)]
            independent_vars = np.array([slice for slice in slice_iterator(SPY.log_yields, len(SPY.prices) - trailing_periods)][:trailing_periods + 1 - exclude_concurrent]).T
            dependent_var = VXX.log_yields[trailing_periods:]
            mymodel = ols.ols(dependent_var, independent_vars, "VXX yield", independent_var_names)
            coeffs.append(mymodel.b)
            R2.append(mymodel.R2)

        pyplot.plot(1)
        pyplot.show()
        for i in range(len(mymodel.x_varnm)):
            pyplot.plot( [c[i] for c in coeffs], label=mymodel.x_varnm[i] )
        pyplot.plot(R2, label="R2")

        pyplot.legend(loc=0)
        pyplot.show()
        return np.array(R2)

if __name__ == "__main__":
    find_model_results()

if __name__ == "__main_44_":
    for lower_entry_bound in range(5,6):
        for upper_entry_bound in range(9, 10):
            for max_signal_reversal in range(10):
                backtest_period(leb=lower_entry_bound,
                                ueb=upper_entry_bound,
                                msr=max_signal_reversal)
#     backtest_period()

