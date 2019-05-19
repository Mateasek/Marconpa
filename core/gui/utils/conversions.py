from Marconpa.core.configs.wave_form import Waveform

def callback_table_as_waveform(table_data):
    """
     Transforming data table into dictionary to be used as input into waveform class
    {'NumberOfIntervals': 4,
     'Waveform': {0: {'Interpolation': 'Constant',
                      'x0': 0.0,
                      'x1': 975000.0,
                      'y0': 0.0,
                      'y1': 0.0},
    :param table_data:
    :return:
    """

    waveform_dict = {"NumberOfIntervals": len(table_data)}
    waveform_dict["Waveform"] = {}
    for interval, row in enumerate(table_data):
        waveform_dict["Waveform"][str(interval)] = {"Interpolation": str(row["Interpolation"]),
                                                    "x0": row["x0"], "x1": row["x1"], "y0": row["y0"], "y1": row["y1"]}

    return Waveform(waveform_dict)


