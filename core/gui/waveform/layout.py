import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from dash._utils import create_callback_id

from Marconpa.core.gui.waveform.components import waveform_table, waveform_plot
from Marconpa.core.gui.waveform.callback import callback_tablechanged


def waveform_layout(waveform_id, waveform_name, waveform, app):

    table_id = waveform_id + "_table"
    plot_id = waveform_id + "_plot"
    table = dbc.Col(
        html.Div(
            [
                waveform_table(id=table_id, setpoints=waveform.return_SetPoints())
            ]
        ),
        style={"width": "150px"},
    )

    graph = dbc.Col(html.Div([waveform_plot(id=plot_id, setpoints = waveform.return_SetPoints())]))


    if not create_callback_id(Output(plot_id, "figure")) in list(app.app.callback_map.keys()):

        app.callback_list.append([{"output": Output(plot_id, "figure"), "inputs": [Input(table_id, "data")]},
                                  callback_tablechanged])
        #app.app.callback(Output(plot_id, "figure"),
        #                 [Input(table_id, "data"), Input(table_id, "columns")])(callback_tablechanged)

        #@app.app.callback(
        #    Output(component_id=plot_id, component_property="figure"),
        #    [Input(component_id=table_id, component_property="data")],
        #)
        #def callback_tablechanged(rows):
            #df = pd.DataFrame(rows, columns=[c["name"] for c in columns])
        #    return {"data": [{"x": [row["x0"], row["x1"]], "y": [row["y0"], row["y1"]], "type": "line"} for row in rows]}


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
