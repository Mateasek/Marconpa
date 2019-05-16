import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import base64

from Marconpa.core.gui.waveform.components import waveform_table, waveform_plot

from Marconpa.core.parser.lark import MarteConfigParser
from Marconpa.core.configs.configfile import Density


def add_callback(app, outp, inp, action):
    try:
        app.callback(outp, inp)(action)
    except dash.exceptions.DuplicateCallbackOutput:
        pass


def callback_tablechanged(rows, columns):
    #df = pd.DataFrame(rows, columns=[c["name"] for c in columns])
    return {"data": [{"x": [row["x0"], row["x1"]], "y": [row["y0"], row["y1"]], "type": "line"} for row in rows]}



# @app.callback(
#    Output("table-editing-simple-output", "figure"),
#    [Input("table-editing-simple", "data"), Input("table-editing-simple", "columns")],
# )
# def display_output(rows, columns):
#    df = pd.DataFrame(rows, columns=[c["name"] for c in columns])
#    return {"data": [{"x": [row["x0"], row["x1"]], "y": [row["y0"], row["y1"]], "type": "line"} for row in rows]}
