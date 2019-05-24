import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from dash._utils import create_callback_id
import dash

from marconpa.gui.waveform.components import waveform_table, waveform_plot
from marconpa.gui.waveform.callback import callback_tablechanged
from marconpa.gui.utils import IdHandler
from marconpa.gui.app import app
def waveform_layout(waveform, waveform_name, parent_id):
    """
    Constructs content for the waveform part
    :param waveform_id:
    :param waveform_name:
    :param waveform:
    :param app:
    :return:
    """
    waveform_id = IdHandler(name=waveform_name, kind="Waveform", parent=parent_id)
    table_id = IdHandler(name="table", kind="Waveform", parent=waveform_id)
    plot_id = IdHandler(name="plot", kind="Waveform", parent=waveform_id)
    table = dbc.Col(
        html.Div([waveform_table(id=table_id.id, setpoints=waveform.return_SetPoints())]),
        style={"width": "150px"},
    )

    graph = dbc.Col(
        html.Div([waveform_plot(id=plot_id.id, setpoints=waveform.return_SetPoints())])
    )

    return_div = html.Details(
        [html.Summary(waveform_name), html.Div(dbc.Row([table, graph]))], id=waveform_id.id
    )
    # add callback for change in table
    output = Output(plot_id.id, "figure")
    if not create_callback_id(output) in app.callback_map:
        app.callback(output, [Input(table_id.id, "data")])(callback_tablechanged)

    return return_div, [table_id, plot_id]


