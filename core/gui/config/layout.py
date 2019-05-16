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
from Marconpa.core.configs.configfile import Density
from Marconpa.examples.example import parse_density
from Marconpa.core.configs.configfile import Density
from Marconpa.core.configs.channel import Channel


def config_layout(config_id, config, app):
    channels = get_channels(config)
    row = html.Div(
        [channel_layout(config_id + "_" + i[0], i[0], i, app) for i in channels.items()]
    )

    return row



def get_channels(conf):

    channels = {}

    for attrib in conf.__attrs_attrs__:
        if attrib.type is Channel:
            channels[attrib.name] = getattr(conf, attrib.name)

    return channels

