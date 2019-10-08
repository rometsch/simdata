# scalar quantities and time series
# data is stored as Ntimes x Ndata
import numpy as np
import astropy.units as u

class Scalar:

    def __init__(self, time, data, axes=[], time_dim=0, name=""):
        self.time = time
        self.data = data
        self.name = name
        self.axes_dim = axes_dim
        self.time_dim = time_dim
        for v in [time, data]:
            if not isinstance(v, u.Quantity):
                raise TypeError("'{}' is a physical value but not an astropy quantity!".format(v))

    def __getitem__(self, key):
        return self.get(key)

    def get(self, key=None, return_time=False):
        if key is not None:
            rv = self.data[key]
            t = self.time[key]
        else:
            rv = self.data
            t = self.time
        if return_time:
            rv = (t, rv)
        return rv

    def get_time_interval(self, tmin, tmax, **kwargs):
        for t in [tmin, tmax]:
            if not isinstance(t, u.Quantity):
                raise TypeError("'{}' does not have a unit!".format(t))
        inds = np.logical_and( tmin <= self.time, tmax >= self.time)
        key = np.arange(len(inds))[inds]
        return self.get(key)

    def get_time_closest(self, t, **kwargs):
        if not isinstance(t, u.Quantity):
            raise TypeError("'{}' does not have a unit!".format(t))
        ind = np.argmin( np.abs(self.time-t))
        return self.get(key=ind, **kwargs)