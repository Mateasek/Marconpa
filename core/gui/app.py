import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import base64


from Marconpa.core.parser.lark import MarteConfigParser
from Marconpa.core.configs.configfile import Density

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


row = html.Div(
    [
        html.Div([
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=False
            ),
            html.Div(id='output-data-upload'),
        ]),
        dbc.Row(dbc.Col(html.Div("Waveform editor"))),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            dash_table.DataTable(
                                id="table-editing-simple",
                                columns=[
                                    {"name": i, "id": i} for i in ["time", "values"]
                                ],
                                data=[
                                ],
                                editable=True,
                            )
                        ]
                    ),
                    style={"width": "150px"},
                ),
                dbc.Col(html.Div([dcc.Graph(id="table-editing-simple-output")])),
            ]
        ),
    ]
)


app.layout = dbc.Container([row])




@app.callback(
    Output("table-editing-simple-output", "figure"),
    [Input("table-editing-simple", "data"), Input("table-editing-simple", "columns")],
)
def display_output(rows, columns):
    df = pd.DataFrame(rows, columns=[c["name"] for c in columns])
    return {"data": [{"x": df[df.columns[0]], "y": df[df.columns[1]], "type": "line"}]}


@app.callback(Output("table-editing-simple", "data"),
              [Input('upload-data', 'contents')])

def select_config_file(contents):
    #get file content
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    data_toplot = parse_config(decoded)



def parse_config(file_coontents):

    parser = MarteConfigParser()
    parsed = parser.parse_config(file_coontents)
    density = Density.from_parsed(parsed)

    waveform = density.FeedbackChannel.waveforms["SpWaveform"].return_SetPoints()

    data_toplot = []

    for index in range(len(waveform)

    return data_toplot


if __name__ == "__main__":
    app.run_server(debug=True)
