import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import base64

from marconpa.core.gui.waveform.layout import waveform_layout
from marconpa.core.gui.channel.layout import channel_layout
from marconpa.core.parser.lark import MarteConfigParser
from marconpa.core.configs.configfile import Density
from marconpa.examples.example import parse_density
from marconpa.core.configs.configfile import Density
from marconpa.core.configs.channel import Channel


def config_layout_channels(config_id, config, app):
    """
    Constructs content of configuration file tab containing multiple channels
    :param config_id: Id to use for the children
    :param config: Conficuration class instance
    :param app: Link to Marta instance
    :return: contents of the tab for configuration file
    """
    channels = get_channels(config)
    row = html.Div(
        [
            channel_layout(config_id + "_" + i[0], i[0], i[1], app)
            for i in channels.items()
        ]
    )

    return row


def config_layout_waveform(config_id, config, app):
    """
    Constructs content of configuration file tab containing a single waveform
    :param config_id:
    :param config:
    :param app:
    :return:
    """
    contents = html.Div(
        waveform_layout(config_id + "_waveform", "waveform", config.waveform, app)
    )
    return html.Div([contents])


def get_channels(conf):
    """
    Extracts channels from the configuration file
    :param conf:
    :return:
    """
    channels = {}

    for attrib in conf.__attrs_attrs__:
        if attrib.type is Channel:
            channels[attrib.name] = getattr(conf, attrib.name)

    return channels


if __name__ == "__main__":

    from marconpa.core.configs.configfile import get_config_object

    class Marta:
        def __init__(self):

            self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
            self.callback_list = []
            self.app.config["suppress_callback_exceptions"] = True

    def generate_upload_layout():
        """
        Returns html.Div containing dcc.Upload, which server for file selection and upload.
        :return: Div
        """
        layout = html.Div(
            [
                dcc.Upload(
                    id="upload-data",
                    children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
                    style={
                        "width": "100%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "margin": "10px",
                    },
                    # Allow multiple files to be uploaded
                    multiple=True,
                )
            ]
        )

        return layout

    def setlayout(input, filename, modified):
        tabcontent = config_layout_channels("Density", density, marta)

        tab = [dcc.Tab(label="Density", id="Density", children=[tabcontent])]
        tabs = dcc.Tabs(id="config_tabs", value="Density", children=tab)
        return tabs

    configtype = "Density"
    configfolder = "/home/maajk/configs/original/"

    density = get_config_object(configtype, configfolder)

    marta = Marta()

    loading = generate_upload_layout()

    # tabs = setlayout(None, None, None)

    layout = html.Div(
        [html.Div(loading), html.Div(id="div_tabs"), html.Div(id="hidden")]
    )

    marta.app.layout = layout

    marta.app.callback(
        Output("div_tabs", "children"),
        [Input("upload-data", "contents")],
        [State("upload-data", "filename"), State("upload-data", "last_modified")],
    )(setlayout)

    # def register_callbacks(inout):
    #    for callback in marta.callback_list:
    #        marta.app.callback(**callback["parameters"])(callback["action"])
    # marta.app.callback(Output("hidden", "children"), [Input("div_tabs", "children")])(register_callbacks)

    marta.app.run_server(debug=True)
