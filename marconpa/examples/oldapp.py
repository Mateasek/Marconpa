import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output
from Marconpa.core.gui.utils.idhandler import IdHandler
import re

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config["suppress_callback_exceptions"] = True

parent = IdHandler(name="parent", component_type="pparent")

table_id = IdHandler(name="waveformtab", component_type="table", parent=parent)
plot_tab = IdHandler(name="waveformplot", component_type="plot", parent=parent)

exmpl = '{"component_type":"table","name":"waveformtab","parent":"{\\"component_type\\":\\"pparent\\",\\"name\\":\\"parent\\",\\"parent\\":null}"}'
#exmpl = re.sub("\s+","",exmpl)

ptid = table_id.id
#ptid = "aa3215432asd315534asdf"
ttid = "blabla"
row = html.Div(
    [
        dbc.Row(dbc.Col(html.Div("Waveform editor"))),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            dash_table.DataTable(
                                id=ptid,
                                columns=[
                                    {"name": i, "id": i} for i in ["time", "values"]
                                ],
                                data=[
                                    {"time": 1, "values": 10},
                                    {"time": 2, "values": 20},
                                    {"time": 4, "values": 15},
                                ],
                                editable=True,
                            )
                        ]
                    ),
                    style={"width": "150px"},
                ),
                dbc.Col(html.Div([dcc.Graph(id=ttid)])),
            ]
        ),
    ]
)


app.layout = dbc.Container([row])


@app.callback(
    Output(ttid, "figure"),
    [Input(ptid, "data"), Input(ptid, "columns")],
)
def display_output(rows, columns):
    df = pd.DataFrame(rows, columns=[c["name"] for c in columns])
    return {"data": [{"x": df[df.columns[0]], "y": df[df.columns[1]], "type": "line"}]}


if __name__ == "__main__":
    app.run_server(debug=True)