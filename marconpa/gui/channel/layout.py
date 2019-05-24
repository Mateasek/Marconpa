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

from marconpa.gui.waveform.layout import waveform_layout
from marconpa.core import Waveform
from marconpa.gui.channel.components import attributes_table
from marconpa.gui.utils import IdHandler

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


def channel_layout(channel, channel_name, parent_id):
    """
    Generates content of the channel
    :param channel_id: Id for the channel
    :param channel_name: Chanel name
    :param channel: Instance of the channel class
    :param app: marta instance
    :return:
    """
    channel_contents = get_waveforms(channel)
    channel_id = IdHandler(name=channel_name, kind="Channel", parent=parent_id)
    content_list = []
    callback_list = []
    if "attributes" in channel_contents.keys():
        content, callback = attributes_table(channel_contents["attributes"], channel_id)
        callback_list += callback
        content_list.append(
            html.Details(
                [
                    html.Summary("Attributes"),
                    content,
                ],
                id=channel_id.id
            )
        )

    if bool(channel_contents["waveforms"]):
        for key, item in channel_contents["waveforms"].items():
            content, callback =  waveform_layout(item, key, channel_id)
            content_list.append(html.Li(content))
            callback_list +=callback
        contents = html.Div(html.Ol(content_list, style={"listStyle": "none"}))
        # contents = html.Div([waveform_layout(channel_id + "_" + i[0], i[0], i[1], app) for i in waveforms.items()])
        return html.Details([html.Summary(channel_name), contents]), callback_list
    else:
        return html.Div(), callback_list


