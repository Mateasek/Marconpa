import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import base64
from typing import Dict
from collections import OrderedDict

from Marconpa.core.gui.waveform.layout import waveform_layout
from Marconpa.core.configs.wave_form import Waveform

def get_waveforms(channel):
    """
    Extract wavefroms into an ordered dict
    :param channel: Channel from configuration file class
    :return:
    """
    waveforms = OrderedDict()
    for attrib in channel.__attrs_attrs__:
        attrib_value = getattr(channel, attrib.name)
        if isinstance(attrib_value,Waveform) and attrib.name is "Enabled":
            waveforms["Enabled"] = attrib_value

    for attrib in channel.__attrs_attrs__:
        attrib_value = getattr(channel, attrib.name)
        if isinstance(attrib_value, dict):
            for j in attrib_value.items():
                if isinstance(j[1], Waveform):
                    waveforms[j[0]] = j[1]

    return waveforms

def channel_layout(channel_id, channel_name, channel, app):
    """
    Generates content of the channel
    :param channel_id: Id for the channel
    :param channel_name: Chanel name
    :param channel: Instance of the channel class
    :param app: marta instance
    :return:
    """
    waveforms = get_waveforms(channel)

    if bool(waveforms):
        list_content = [html.Li(waveform_layout(channel_id + "_" + i[0], i[0], i[1], app)) for i in waveforms.items()]
        contents = html.Div(html.Ol(list_content, style={"listStyle": "none"}))
        #contents = html.Div([waveform_layout(channel_id + "_" + i[0], i[0], i[1], app) for i in waveforms.items()])
        return html.Details([html.Summary(channel_name), contents])
    else:
        return html.Div()

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

    layout = channel_layout("test_channel", "SP", density.FeedbackChannel, marta)


    marta.app.layout =  layout
    marta.app.run_server(debug=True)
