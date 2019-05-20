import dash_core_components as dcc
import dash_html_components as html
import base64

from Marconpa.core.parser.lark import MarteConfigParser
from Marconpa.core.configs.configfile import (
    config_types,
    StandartConfig,
    WaveformConfig,
    EFPS,
)

from Marconpa.core.gui.components import generate_tab_channels, generate_tab_waveform


def tab_structure_from_files(app, list_of_contents, list_of_names):
    """
    Processes selected files. Checks if the file is known config file and creates list of dcc.Tab for tabs environment.
    to the configfile type.
    :param list_of_contents: List of file contents
    :param list_of_names: List of file names
    :param list_of_dates: List of modification dates
    :return: list of dcc.Tab
    """

    tab = []
    data = []
    if list_of_contents is None:
        return [], []

    parser = MarteConfigParser()

    for key, item in zip(list_of_names, list_of_contents):
        if key in app.CONFIG_NAMES:
            content_type, content_string = item.split(",")
            decoded = base64.b64decode(content_string).decode()
            parsed = parser.parse_config(decoded)
            config_instance = config_types[key].from_parsed(parsed)

            if isinstance(config_instance, StandartConfig) or isinstance(
                config_instance, EFPS
            ):
                tab.append(generate_tab_channels(app, config_instance, key))
                data.append(html.Div(id=key, children=decoded))
            if isinstance(config_instance, WaveformConfig):
                tab.append(generate_tab_waveform(app, config_instance, key))
                data.append(html.Div(id=key, children=decoded))

    tabs = dcc.Tabs(id="config_tabs", children=tab)
    return tabs, data
