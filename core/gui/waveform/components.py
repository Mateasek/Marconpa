import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import base64





def waveform_table(id, setpoints):
    data = [ {"index":index, "x0":setpoints["x0"][index], "x1":setpoints["x1"][index], "y0":setpoints["y0"][index],
            "y1":setpoints["y1"][index]} for index in range(setpoints["x0"].shape[0])]
    return dash_table.DataTable(
        id=id,
        columns=[
            {"name": i, "id": i} for i in ["index", "x0", "x1", "y0", "y1"]
        ],
        data= data,
        editable=True,
    )

def waveform_plot(id):
    return dcc.Graph(id=id)


if __name__ == "__main__":

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = dbc.Container([row])
    app.run_server(debug=True)
