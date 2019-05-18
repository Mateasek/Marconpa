import warnings
import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
from Marconpa.core.utils.conversions import dict2stringlist

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
        """
        read and check wave form
        :param wave_form_dict:
        """
        try:
            self.waveform = pd.DataFrame.from_dict(wave_form_dict['Waveform'], orient='index')
            if np.any(self.waveform.iloc[:]['x0'] != self.waveform.sort_values(by=['x0']).iloc[:]['x0']):
                warnings.warn("Time intervals are not sorted ")
                if np.any(self.waveform[1:]['x0'].values != self.waveform[:-1]['x1'].values):
                    warnings.warn("check the set points - they are not continuous")
                    indexOfConflicts = np.nonzero(self.waveform[1:]['x0'].values - self.waveform[:-1]['x1'].values)
                    for i in range(len(indexOfConflicts)):
                        if self.waveform.iloc[indexOfConflicts[i + 1]]['x0'].values > \
                                self.waveform.iloc[indexOfConflicts[i]]['x1'].values:
                            print('Times subinterval number {ni} ends latter than the next interval starts. \
                            End time {t_end} of this interval set to  the time {t_begin} when next interval\
                            starts.'.format(ni=indexOfConflicts[i],
                                            t_end=self.waveform.iloc[indexOfConflicts[i + 1]]['x0'].values[0],
                                            t_begin=self.waveform.iloc[indexOfConflicts[i]]['x1'].values[0]))
                            self.waveform.at[indexOfConflicts[i], 'x1'] = self.waveform.iloc[i + 1][['x0']].values[0]
                        else:
                            print('Times subinterval number {ni} ends earlier than the next interval starts. Gap filled\
                                                    by zeros'.format(ni=indexOfConflicts[i]))
                            if wave_form_dict['NumberOfIntervals'] < len(self.waveform.index):
                                wave_form_dict['NumberOfIntervals'] = len(self.waveform.index)
                                pokus = self.waveform.set_index('x0')





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
        """
        gives y value for given time point
        :param t_value:  requested time point
        :return: y_value
        """
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
        """
        gives set points of time intervals in waveform
        :return: x_axis = set_points
        """
        # x_axis = [row[1][col] for row in self.waveform.iterrows() for col in ['x0', 'x1']]
        # y_axis = [row[1][col] for row in self.waveform.iterrows() for col in ['y0', 'y1']]
        set_points = {'x0': self.waveform[:]['x0'].values, 'x1': self.waveform[:]['x1'].values, \
                      'y0': self.waveform[:]['y0'].values, 'y1': self.waveform[:]['y1'].values,
                      "Interpolation": self.waveform[:]["Interpolation"][:]}
        return set_points

    def export_waveform(self):
        """
        write pandas to dictionary
        :return:
        """
        return self.waveform.to_dict(orient='index')

    def export_as_listofstring(self, depth=0):
        listofstrings = ["\t" * depth + "NumberOfIntervals = {0:d}".format(self.NofIntervals)]
        listofstrings.append("\t" * depth + "Waveform =")
        listofstrings.append("\t" * depth + "{")
        listofstrings += dict2stringlist(self.export_waveform(), depth=depth+1)
        listofstrings.append("\t" * depth + "}")
        return listofstrings

    def export_as_string(self, depth=0):
        return "\n".join(self.export_as_listofstring(depth=depth))


