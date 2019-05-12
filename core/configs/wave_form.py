import warnings
import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline


class Waveform:
    """
    Waveform from dictionary
    {'NumberOfIntervals': 4,
     'Waveform': {0: {'Interpolation': 'Constant',
                      'x0': 0.0,
                      'x1': 975000.0,
                      'y0': 0.0,
                      'y1': 0.0},

    """

    def __init__(self, wave_form_dict):
        try:
            self.waveform = pd.DataFrame.from_dict(wave_form_dict['Waveform'], orient='index')
            if np.any(self.waveform[1:]['x0'].values != self.waveform[:-1]['x1'].values):
                warnings.warn("check the set points - they are not continuous")
                indexOfConflicts = np.nonzero(self.waveform[1:]['x0'].values - self.waveform[:-1]['x1'].values)
                for i in range(len(indexOfConflicts)):
                    if self.waveform.iloc[indexOfConflicts[i] + 1]['x0'].values > \
                            self.waveform.iloc[indexOfConflicts[i]]['x1'].values:
                        print('Times subinterval number {ni} ends latter than the next interval starts. End set to \
                        the smaller time'.format(ni=indexOfConflicts[i]))
                        self.waveform.at[indexOfConflicts[i], 'x1'] = self.waveform.iloc[1][['x0']].values[0]
                    else:
                        print('Times subinterval number {ni} ends earlier than the next interval starts. Gap filled \
                                                by zeros'.format(ni=indexOfConflicts[i]))
                        if wave_form_dict['NumberOfIntervals'] < len(self.waveform.index):
                            wave_form_dict['NumberOfIntervals'] = len(self.waveform.index)






        except KeyError:
            print("Missing key Waveform. Set to one interval with y=0")
            self.waveform = {'Waveform': {0: dict(Interpolation='Constant', x0=0.0, x1=1500000.0, y0=0.0006,
                                                  y1=0.0006)}}

        try:
            self.NofIntervals = wave_form_dict['NumberOfIntervals']
            if self.NofIntervals < len(self.waveform.index):
                warnings.warn("NumberOfIntervals is lower than number of time intervals inserted by pilot")
            elif self.NofIntervals > len(self.waveform.index):
                warnings.warn('NumberOfIntervals is larger than number of time intervals inserted by pilot')
        except KeyError:
            print('Missing key NumberOfIntervals. Set to 0')
            self.waveform = {'NumberOfIntervals': 0}

    def return_value(self, t_value):
        x_axis = [row[1][col] for row in self.waveform.iterrows() for col in ['x0', 'x1']]
        y_axis = [row[1][col] for row in self.waveform.iterrows() for col in ['y0', 'y1']]
        x_values = x_axis[::2]
        x_values.append(x_axis[-1])
        y_values = y_axis[::2]
        y_values.append(y_axis[-1])
        y_value = np.NaN
        if t_value >= min(x_values) and t_value >= max(x_values):
            print("you are out of the time interval")
        else:
            if min(y_values) == max(y_values):
                y_value = min(y_values)
            else:
                method = self.waveform['Interpolation'].values
                if np.any(method == "Linear"):
                    y_value = np.interp(t_value, x_values, y_values)
                elif np.any(method == "Cubic"):
                    cs = CubicSpline(x_values, y_values)
                    y_value = cs(t_value)
        return y_value

    def return_SetPoints(self):
        x_axis = [row[1][col] for row in self.waveform.iterrows() for col in ['x0', 'x1']]
        y_axis = [row[1][col] for row in self.waveform.iterrows() for col in ['y0', 'y1']]
        return x_axis, y_axis

    def export_waveform(self):
        return self.waveform.to_dict(orient='index')
