import warnings
import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
from marconpa.core.utils.conversions import dict2stringlist
import attr


@attr.s
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

    _waveform = attr.ib(default=None)
    _numberofintervals = attr.ib(default=None, type=int)

    @_waveform.validator
    def validate_waveform(self, attribute, value):

        if value is None:
           value = pd.DataFrame({
                "Waveform": {
                    0: dict(
                        Interpolation="Constant",
                        x0=0.0,
                        x1=1500000.0,
                        y0=0.0006,
                        y1=0.0006,
                    )
                }
            })
        elif not isinstance(value, pd.DataFrame):
            raise ValueError("Waveform has to be pandas.Dataframe")

    def __init__(self, waveform, numberofintervals):
        """
        read and check wave form
        :param wave_form_dict:
        """
        self._waveform = waveform
        self.numberofintervals = numberofintervals


    @classmethod
    def from_waveform_dict(cls, wave_form_dict):

        try:
            waveform = wave_form_dict["Waveform"]
        except KeyError:
            warnings.warn("Missing key Waveform. Set to one interval with y=0")
            waveform = {
                "Waveform": {
                    0: dict(
                        Interpolation="Constant",
                        x0=0.0,
                        x1=1500000.0,
                        y0=0.0006,
                        y1=0.0006,
                    )
                }
            }
        finally:
            waveform = pd.DataFrame.from_dict(waveform, orient="index")

        try:
            numberofintervals = wave_form_dict["NumberOfIntervals"]
        except KeyError:
            warnings.warn("NumberOfIntervals is missing. Setting to 0.")
            numberofintervals = 0

        return cls(waveform, numberofintervals)

    @property
    def waveform(self):
        return self._waveform

    @waveform.setter
    def waveform(self, value):
        if not isinstance(value, pd.DataFrame):
            raise ValueError("waveform has to be pandas.DataFrame")
        self._waveform = value

    @property
    def numberofintervals(self):
        return self._numberofintervals

    @numberofintervals.setter
    def numberofintervals(self, value):
        if value < 0:
            warnings.warn("numberofintervals set to 0 because value < 0")
            self._numberofintervals = 0
        else:
            self._numberofintervals = value

    def iscontinupus(self):
        state = True
        message = ""
        if np.any(
                self.waveform[1:]["x0"].values != self.waveform[:-1]["x1"].values
        ):
            state = False
            message = "check the set points - they are not continuous"

        return state, message
    
    def unknown_magic(self):

        if np.any(
                self.waveform[1:]["x0"].values != self.waveform[:-1]["x1"].values
        ):
            warnings.warn("check the set points - they are not continuous")
            indexOfConflicts = np.nonzero(
                self.waveform[1:]["x0"].values - self.waveform[:-1]["x1"].values
            )
            for i in range(len(indexOfConflicts)):
                if (
                        self.waveform.iloc[indexOfConflicts[i + 1]]["x0"].values
                        > self.waveform.iloc[indexOfConflicts[i]]["x1"].values
                ):
                    print(
                        "Times subinterval number {ni} ends latter than the next interval starts. \
                    End time {t_end} of this interval set to  the time {t_begin} when next interval\
                    starts.".format(
                            ni=indexOfConflicts[i],
                            t_end=self.waveform.iloc[indexOfConflicts[i + 1]][
                                "x0"
                            ].values[0],
                            t_begin=self.waveform.iloc[indexOfConflicts[i]][
                                "x1"
                            ].values[0],
                        )
                    )
                    self.waveform.at[
                        indexOfConflicts[i], "x1"
                    ] = self.waveform.iloc[i + 1][["x0"]].values[0]
                else:
                    print(
                        "Times subinterval number {ni} ends earlier than the next interval starts. Gap filled\
                                            by zeros".format(
                            ni=indexOfConflicts[i]
                        )
                    )
                    if numberofintervals < len(
                            self.waveform.index
                    ):
                        numberofintervals = len(
                            self.waveform.index
                        )
                        pokus = self.waveform.set_index("x0")


    def issorted(self):
        state = True
        message = ""
        if np.any(
                self.waveform.iloc[:]["x0"]
                != self.waveform.sort_values(by=["x0"]).iloc[:]["x0"]
        ):
            message = "Time intervals are not sorted "
            state = False

        return state, message

    def numberofintervals_match_waveform(self):

        state = True
        message = ""
        if self.numberofintervals < len(self.waveform.index):
            message = "NumberOfIntervals is lower than number of time intervals inserted by pilot"
            warnings.warn(message)
            state = False

        elif self.numberofintervals > len(self.waveform.index):
            message = "NumberOfIntervals is larger than number of time intervals inserted by pilot"
            warnings.warn(message)
            state = False

        return state, message

    def return_value(self, t_value):
        """
        gives y value for given time point
        :param t_value:  requested time point
        :return: y_value
        """
        x_axis = [
            row[1][col] for row in self.waveform.iterrows() for col in ["x0", "x1"]
        ]
        y_axis = [
            row[1][col] for row in self.waveform.iterrows() for col in ["y0", "y1"]
        ]
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
                method = self.waveform["Interpolation"].values
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
        set_points = {
            "x0": self.waveform[:]["x0"].values,
            "x1": self.waveform[:]["x1"].values,
            "y0": self.waveform[:]["y0"].values,
            "y1": self.waveform[:]["y1"].values,
            "Interpolation": self.waveform[:]["Interpolation"][:],
        }
        return set_points

    def export_waveform(self):
        """
        write pandas to dictionary
        :return:
        """
        return self.waveform.to_dict(orient="index")

    def export_as_listofstring(self, depth=0):
        listofstrings = [
            "\t" * depth + "NumberOfIntervals = {0:d}".format(self._numberofintervals)
        ]
        listofstrings.append("\t" * depth + "Waveform =")
        listofstrings.append("\t" * depth + "{")
        listofstrings += dict2stringlist(self.export_waveform(), depth=depth + 1)
        listofstrings.append("\t" * depth + "}")
        return listofstrings

    def export_as_string(self, depth=0):
        return "\n".join(self.export_as_listofstring(depth=depth))
