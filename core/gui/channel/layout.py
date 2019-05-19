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
from Marconpa.core.gui.channel.components import attributes_table


def get_waveforms(channel):
    """
    Extract wavefroms into an ordered dict
    :param channel: Channel from configuration file class
    :return:
    """

    channel_content = {}

    channel_content["waveforms"] = OrderedDict()
    for attrib in channel.__attrs_attrs__:
        attrib_value = getattr(channel, attrib.name)
        if isinstance(attrib_value, Waveform) and attrib.name is "Enabled":
            channel_content["waveforms"]["Enabled"] = attrib_value

    for attrib in channel.__attrs_attrs__:
        attrib_value = getattr(channel, attrib.name)
        if attrib.name == "attributes":
            channel_content["attributes"] = getattr(channel, attrib.name)
        if isinstance(attrib_value, dict):
            for key, item in attrib_value.items():
                if isinstance(item, Waveform):
                    channel_content["waveforms"][key] = item

    return channel_content


def channel_layout(channel_id, channel_name, channel, app):
    """
    Generates content of the channel
    :param channel_id: Id for the channel
    :param channel_name: Chanel name
    :param channel: Instance of the channel class
    :param app: marta instance
    :return:
    """
    channel_contents = get_waveforms(channel)

    if "attributes" in channel_contents.keys():
        list_content = [
            html.Details(
                [
                    html.Summary("Attributes"),
                    attributes_table(
                        channel_id + "_attributes", channel_contents["attributes"]
                    ),
                ]
            )
        ]

    if bool(channel_contents["waveforms"]):
        list_content += [
            html.Li(waveform_layout(channel_id + "_" + i[0], i[0], i[1], app))
            for i in channel_contents["waveforms"].items()
        ]
        contents = html.Div(html.Ol(list_content, style={"listStyle": "none"}))
        # contents = html.Div([waveform_layout(channel_id + "_" + i[0], i[0], i[1], app) for i in waveforms.items()])
        return html.Details([html.Summary(channel_name), contents])
    else:
        return html.Div()


if __name__ == "__main__":

    from Marconpa.core.configs.configfile import get_config_object

    class Marta:
        def __init__(self):

            self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    configtype = "Density"
    configfolder = "/home/maajk/configs/original/"

    density = get_config_object(configtype, configfolder)

    marta = Marta()
    marta.app.config["suppress_callback_exceptions"] = True

    layout = channel_layout("test_channel", "SP", density.FeedbackChannel, marta)

    marta.app.layout = layout
    marta.app.run_server(debug=True)
