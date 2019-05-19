import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import base64

from Marconpa.core.gui.waveform.layout import waveform_layout
from Marconpa.core.gui.channel.layout import channel_layout
from Marconpa.core.parser.lark import MarteConfigParser
from Marconpa.core.configs.configfile import ConfigFile
from Marconpa.examples.example import parse_density
from Marconpa.core.configs.configfile import Density
from Marconpa.core.configs.channel import Channel
from Marconpa.core.gui.config.layout import (
    config_layout_channels,
    config_layout_waveform,
)
from Marconpa.core.configs.configfile import (
    config_types,
    StandartConfig,
    WaveformConfig,
    EFPS,
)
from dash._utils import create_callback_id


class Marta:
    CONFIG_NAMES = ["Density", "EFPS", "FABR", "FABV", "SFPS", "TFPS", "Density2"]

    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.app.config["suppress_callback_exceptions"] = True

        # generates clicking stuff to initiate file selection and upload
        upload_layout = self.generate_upload_layout()

        # compose general layout
        layout = html.Div([upload_layout, html.Div(id="div_tabs")])

        # set app layout
        self.app.layout = dbc.Container([layout])

        # calback initializing tabs and their content after upload
        self.app.callback(
            Output("div_tabs", "children"),
            [Input("upload-data", "contents")],
            [State("upload-data", "filename"), State("upload-data", "last_modified")],
        )(self.process_files)

    def process_files(self, list_of_contents, list_of_names, list_of_dates):
        """
        Processes selected files. Checks if the file is known config file and creates list of dcc.Tab for tabs environment.
        to the configfile type.
        :param list_of_contents: List of file contents
        :param list_of_names: List of file names
        :param list_of_dates: List of modification dates
        :return: list of dcc.Tab
        """

        self.config_files = {}
        tab = []
        if list_of_contents is None:
            return

        parser = MarteConfigParser()

        for key, item in zip(list_of_names, list_of_contents):
            if key in self.CONFIG_NAMES:
                content_type, content_string = item.split(",")
                decoded = base64.b64decode(content_string).decode()
                parsed = parser.parse_config(decoded)
                config_instance = config_types[key].from_parsed(parsed)

                if isinstance(config_instance, StandartConfig) or isinstance(
                    config_instance, EFPS
                ):
                    tab.append(
                        dcc.Tab(
                            label=key,
                            id=key,
                            children=[
                                config_layout_channels(key, config_instance, self)
                            ],
                        )
                    )
                if isinstance(config_instance, WaveformConfig):
                    tab.append(
                        dcc.Tab(
                            label=key,
                            id=key,
                            children=[
                                config_layout_waveform(key, config_instance, self)
                            ],
                        )
                    )

        tabs = dcc.Tabs(id="config_tabs", children=tab)
        return tabs

    def generate_upload_layout(self):
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
                ),
                html.Div(id="output-data-upload"),
            ]
        )

        return layout


if __name__ == "__main__":
    marta = Marta()
    marta.app.run_server(debug=True)
