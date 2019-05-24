import dash_core_components as dcc
import dash_table
from marconpa.gui.utils.conversions import waveformsetpoints2tabledata

def waveform_table(id, setpoints):
    """
    Constructs table for waveform display
    :param id: Table ID
    :param setpoints: Setpoints from waveform to fill the table
    :return:
    """
    data = waveformsetpoints2tabledata(setpoints)

    return dash_table.DataTable(
        id=id,
        columns=[
            {"name": i, "id": i}
            for i in ["index", "x0", "x1", "y0", "y1", "Interpolation"]
        ],
        data=data,
        editable=True,
    )


def waveform_plot(id, setpoints):
    """
    Constructs figure
    :param id:
    :param setpoints:
    :return:
    """
    data = {
        "data": [
            {
                "x": [setpoints["x0"][index], setpoints["x1"][index]],
                "y": [setpoints["y0"][index], setpoints["y1"][index]],
                "type": "line",
            }
            for index in range(setpoints["x0"].shape[0])
        ]
    }
    return dcc.Graph(id=id, figure=data)
