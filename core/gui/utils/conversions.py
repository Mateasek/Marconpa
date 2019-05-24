from marconpa.core.configs.wave_form import Waveform
from marconpa.core.utils.conversions import list2string

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
        waveform_dict["Waveform"][str(interval)] = {
            "Interpolation": str(row["Interpolation"]),
            "x0": row["x0"],
            "x1": row["x1"],
            "y0": row["y0"],
            "y1": row["y1"],
        }

    return Waveform.from_waveform_dict(waveform_dict)

def channelattributes2tabledata(attributes):
    """
    Attribute attributes of class channel converted into an output for data  property for dash_table
    :param attributes: channel attributes
    :return:
    """
    table = []
    for key, item in attributes.items():
        table.append({"attribute name": key, "value": item})
    return table

def waveformsetpoints2tabledata(setpoints):
    """
    Tranforms output of waveform.return_setpoints() into an output for data property of dash_table component
    :param setpoints: waveform.return_setpoints() output
    :return: data property of dash_table
    """

    data = [
        {
            "index": index,
            "x0": setpoints["x0"][index],
            "x1": setpoints["x1"][index],
            "y0": setpoints["y0"][index],
            "y1": setpoints["y1"][index],
            "Interpolation": setpoints["Interpolation"][index],
        }
        for index in range(setpoints["x0"].shape[0])
    ]

    return data

def tabledata2channelattributes(tabledata):

    attributes = {}
    for i in tabledata:
        if isinstance(i["value"], list):
            i["value"] = list2string(i["value"])
        attributes[i["attribute name"]] = i["value"]

    return attributes

