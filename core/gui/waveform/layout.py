import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from dash._utils import create_callback_id
import dash

from Marconpa.core.gui.waveform.components import waveform_table, waveform_plot
from Marconpa.core.gui.waveform.callback import callback_tablechanged


def waveform_layout(waveform_id, waveform_name, waveform, app):
    """
    Constructs content for the waveform part
    :param waveform_id:
    :param waveform_name:
    :param waveform:
    :param app:
    :return:
    """
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


    return_div = html.Details([html.Summary(waveform_name),
        html.Div(dbc.Row(
        [
            table,
            graph,
        ]
    ))]
    )
    # add callback for change in table
    output = Output(plot_id, "figure")
    if not create_callback_id(output) in app.app.callback_map:
        app.app.callback(output, [Input(table_id,"data")])(callback_tablechanged)

    return return_div



if __name__ == "__main__":
    from Marconpa.core.configs.configfile import get_config_object

    class Marta():

        def __init__(self):

            self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    configtype = "Density"
    configfolder = "/home/maajk/configs/original/"

    density = get_config_object(configtype, configfolder)

    marta = Marta()
    marta.app.config['suppress_callback_exceptions'] = True

    layout = waveform_layout("test_wf", "sp", density.FeedbackChannel.waveforms["SpWaveform"], marta)


    marta.app.layout =  layout
    marta.app.run_server(debug=True)
    #wf = layou