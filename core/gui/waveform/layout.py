import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import base64

from Marconpa.core.gui.waveform.components import waveform_table, waveform_plot
from Marconpa.core.gui.waveform.callback import add_callback, callback_tablechanged

from Marconpa.core.parser.lark import MarteConfigParser
from Marconpa.core.configs.configfile import Density


def waveform_layout(waveform_id, waveform_name, waveform, app):

    table_id = waveform_id + "table"
    plot_id = waveform_id + "_plot"
    table = dbc.Col(
        html.Div(
            [
                waveform_table(id=table_id, setpoints=waveform.return_SetPoints())
            ]
        ),
        style={"width": "150px"},
    )

    graph = dbc.Col(html.Div([waveform_plot(id=plot_id)]))

    add_callback(app, Output(plot_id, "figure"), [Input(table_id, "data"), Input(table_id, "columns")], callback_tablechanged)


    return html.Details([html.Summary(waveform_name),
        html.Div(dbc.Row(
        [
            table,
            graph,
        ]
    ))]
    )



# @app.callback(Output("table-editing-simple", "data"),
#              [Input('upload-data', 'contents')])

# def select_config_file(contents):
#    #get file content
#    content_type, content_string = contents.split(',')
#    decoded = base64.b64decode(content_string).decode()
#    data_toplot = parse_config(decoded)
#    return data_toplot
