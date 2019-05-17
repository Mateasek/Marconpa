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
from Marconpa.core.gui.config.layout import config_layout_channels, config_layout_waveform
from Marconpa.core.configs.configfile import config_types, StandartConfig, WaveformConfig, EFPS
from dash._utils import create_callback_id

class Marta:
    CONFIG_NAMES = ["Density", "EFPS", "FABR", "FABV", "SFPS", "TFPS", "Density2"]

    def __init__(self):
        self.callback_list = []

        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        #self.app.config['suppress_callback_exceptions'] = True
        self.config_files = {}

        #generates clicking stuff to initiate file selection and upload
        upload_layout = self.generate_upload_layout()


        layout = html.Div([upload_layout, html.Div(id="div_tabs"), html.Div(id="invisible")])

        self.app.layout = dbc.Container([layout])

        self.app.callback(Output('div_tabs', 'children'),
                  [Input('upload-data', 'contents')],
                  [State('upload-data', 'filename'),
                   State('upload-data', 'last_modified')])(self.process_files)

        self.app.callback(Output("invisible", "children"), [Input("div_tabs", "children")])(self.tabchanged)

    def tabchanged(self, inp):
        #print(list(self.layout.keys()) + (
        #                    [] if not hasattr(layout, 'id') else
        #                    [layout.id]
        #                ))
        for callback in self.callback_list:
            if not create_callback_id(callback[0]["output"]) in list(self.app.callback_map.keys()):
                self.app.callback(**callback[0])(callback[1])
        self.callback_list = []
        return []


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
        tabs = []
        if list_of_contents is None:
            return

        parser = MarteConfigParser()

        for files in zip(list_of_names, list_of_contents):
            if files[0] in self.CONFIG_NAMES:
                content_type, content_string = files[1].split(',')
                decoded = base64.b64decode(content_string).decode()
                parsed = parser.parse_config(decoded)
                self.config_files[files[0]] = config_types[files[0]].from_parsed(parsed)
                tabs.append(dcc.Tab(label=files[0], id=files[0], children=[self.get_tab(files[0])]))

        tabs_config = dcc.Tabs(id="config_tabs", children=tabs)
        return tabs_config

    def get_tab(self, configname):
        if configname in self.config_files.keys():
            if isinstance(self.config_files[configname], StandartConfig) or isinstance(self.config_files[configname], EFPS):
                return config_layout_channels(configname, self.config_files[configname], self)
            if isinstance(self.config_files[configname], WaveformConfig):
                return config_layout_waveform(configname, self.config_files[configname], self)

    def generate_upload_layout(self):
        """
        Returns html.Div containing dcc.Upload, which server for file selection and upload.
        :return: Div
        """
        layout = html.Div([
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
                multiple=True
            ),
            html.Div(id='output-data-upload'),
        ])

        return layout

if __name__ == "__main__":
    marta = Marta()
    marta.app.run_server(debug=True)
