import dash_html_components as html

from marconpa.gui.waveform.layout import waveform_layout
from marconpa.gui.channel.layout import channel_layout
from marconpa.core import Channel


def config_layout_channels(config, config_id):
    """
    Constructs content of configuration file tab containing multiple channels
    :param config_id: Id to use for the children
    :param config: Conficuration class instance
    :param app: Link to Marta instance
    :return: contents of the tab for configuration file
    """
    channels = get_channels(config)
    contents = []
    callback_list = []
    for key, item in channels.items():
        content, callback = channel_layout(item, key, config_id)
        callback_list +=callback
        contents.append(content)

    row = html.Div( contents)

    return row, callback_list


def config_layout_waveform(config, config_id):
    """
    Constructs content of configuration file tab containing a single waveform
    :param config_id:
    :param config:
    :param app:
    :return:
    """

    content, callback = waveform_layout(config.waveform, "Waveform", config_id)

    contents = html.Div(content)
    return html.Div([contents]), callback


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

