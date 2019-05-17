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
    waveforms = OrderedDict()
    for attrib in channel[1].__attrs_attrs__:
        attrib_value = getattr(channel[1], attrib.name)
        if isinstance(attrib_value,Waveform) and attrib.name is "Enabled":
            waveforms["Enabled"] = attrib_value

    for attrib in channel[1].__attrs_attrs__:
        attrib_value = getattr(channel[1], attrib.name)
        if isinstance(attrib_value, dict):
            for j in attrib_value.items():
                if isinstance(j[1], Waveform):
                    waveforms[j[0]] = j[1]

    return waveforms

def channel_layout(channel_id, channel_name, channel, app):

    waveforms = get_waveforms(channel)

    if bool(waveforms):
        list_content = [html.Li(waveform_layout(channel_id + "_" + i[0], i[0], i[1], app)) for i in waveforms.items()]
        contents = html.Div(html.Ol(list_content, style={"listStyle": "none"}))
        #contents = html.Div([waveform_layout(channel_id + "_" + i[0], i[0], i[1], app) for i in waveforms.items()])
        return html.Details([html.Summary(channel_name), contents])
    else:
        return html.Div()