import h5py
import numpy as np
from matplotlib import pyplot
import ols
from instrument import FinancialInstrument
from correlation import correlate
from multivariate_regression import *

from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed("Dropping to IPython shell")

filename = "SPY-VXX-20090507-20100427.hdf5"


def slice_iterator(lst, slice_length):
    for i in range(len(lst) - slice_length + 1):
        yield lst[i:i + slice_length]

cost_per_share = .020

start_day = 1
end_day = 245

days = end_day - start_day
