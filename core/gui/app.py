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
from Marconpa.core.gui.config.layout import config_layout

class Marta:
    CONFIG_NAMES = ["Density", "EFPS", "FABR", "FABV", "SFPS", "TFPS"]

    def __init__(self):

        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.app.config['suppress_callback_exceptions'] = True
        self.config_files = {}

        upload_layout = self.generate_uploat_layout()

        tabs = html.Div([dcc.Tabs(id="config_tabs", value='density', children=[
        ]),
                         html.Div(id="tabs_content")
                         ])

        layout = html.Div([upload_layout, tabs])

        self.app.layout = dbc.Container([layout])
        self.add_callback(Output('tabs_content', 'children'),
                          [Input('config_tabs', 'value')],
                          [],
                          self.get_tab)

        self.add_callback(Output('config_tabs', 'children'),
                  [Input('upload-data', 'contents')],
                  [State('upload-data', 'filename'),
                   State('upload-data', 'last_modified')], self.process_files)

    def add_callback(self, outp, inp, state, action):
        self.app.callback(outp, inp, state)(action)

    def process_files(self, list_of_contents, list_of_names, list_of_dates):
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
                self.config_files[files[0]] = ConfigFile.from_parsed(parsed)
                tabs.append(dcc.Tab(label=files[0], value=files[0]))

        return tabs

    def get_tab(self, configname):
        if configname in self.config_files.keys():
            return config_layout(configname, self.config_files[configname], self.app)

    def generate_uploat_layout(self):
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

def parse_config(file_coontents):

    parser = MarteConfigParser()
    parsed = parser.parse_config(file_coontents)
    density = Density.from_parsed(parsed)

    waveform = density.FeedbackChannel.waveforms["SpWaveform"].return_SetPoints()

    data_toplot = []

    for index in range(waveform["x0"].shape[0]):
        data_toplot.append({"index": index, "x0": waveform["x0"][index], "x1":waveform["x1"][index], "y0":waveform["y0"][index], "y1":waveform["y1"][index]})
    return data_toplot


if __name__ == "__main__":
    marta = Marta()
    marta.app.run_server(debug=True)
