import dash_core_components as dcc
import dash_table
from marconpa.gui.utils.conversions import waveformsetpoints2tabledata
import dash_html_components as html
from marconpa.gui.utils import IdHandler

def waveform_table(parent_id, setpoints):
    """
    Constructs table for waveform display
    :param table_id: Table ID
    :param setpoints: Setpoints from waveform to fill the table
    :return:
    """
    data = waveformsetpoints2tabledata(setpoints)

    table_id = IdHandler(name="table", kind="Waveform", parent=parent_id)

    table = dash_table.DataTable(
        id=table_id.id,
        columns=[ {"name": i, "id": i}
            for i in ["index", "x0", "x1", "y0", "y1", "Interpolation"]
        ],
        data=data,
        editable=True,
    )

    return table, table_id

def insert_row_table(parent_id):

    row_table_id = IdHandler(name="insertrowTable", kind="Waveform", parent=parent_id)

    columns = [{"name": i, "id": i}
              for i in ["index", "x0", "x1", "y0", "y1", "Interpolation"]
              ]
    data = [{"index": 0, "x0": 0, "x1": 0, "y0": 0, "y1": 0, "Interpolation": "Linear"}]

    table =html.Div(dash_table.DataTable(
        id=row_table_id.id,
        columns= columns,
        data=data,
        editable=True,
    ))
    return table, row_table_id

def insert_row_button(parent_id):

    button_id = IdHandler(name="insertRowButton", kind="Waveform", parent=parent_id)

    button = html.Div(
        html.Button("Insert Row", accessKey="z", title="ctrl+z", id=button_id.id)
    )
    return button, button_id


def dropdown_delete_row(parent_id):
    dropdown_id = IdHandler(name="deleteRowDropdown", kind="Waveform", parent=parent_id)

    dropdown = html.Div([dcc.Dropdown(id=dropdown_id.id, options=[{"label": 0, "value": 0}], value=0)],
                        )

    return dropdown, dropdown_id

def deleterow_button(parent_id):

    button_id = IdHandler(name="deleteRowButton", kind="Waveform", parent=parent_id)

    button = html.Div(
        html.Button("Delete Row", accessKey="z", title="ctrl+z", id=button_id.id)
    )

    return button, button_id

def waveform_plot(parent_id, setpoints):
    """
    Constructs figure
    :param id:
    :param setpoints:
    :return:
    """

    plot_id = IdHandler(name="plot", kind="Waveform", parent=parent_id)

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

    graph = dcc.Graph(id=plot_id.id, figure=data)
    return graph, plot_id
