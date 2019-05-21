import dash_core_components as dcc
import dash_html_components as html
import base64
import json

from marconpa.core.parser.lark import MarteConfigParser
from marconpa.core.configs.configfile import (
    config_types,
    StandartConfig,
    WaveformConfig,
    EFPS,
)

from marconpa.core.gui.components import generate_tab_channels, generate_tab_waveform
from marconpa.core.gui.utils import IdHandler

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
            to_store = json.dumps({"config_type":key, "content": decoded})

            parsed = parser.parse_config(decoded)
            config_instance = config_types[key].from_parsed(parsed)
            datastorage_id = IdHandler(name=key, component_type="DataStorage")
            if isinstance(config_instance, StandartConfig) or isinstance(
                config_instance, EFPS
            ):
                contents, callback_list = generate_tab_channels(app, config_instance, key)
                tab.append(contents)
                data.append(html.Div(id=datastorage_id.id, children=to_store))

            if isinstance(config_instance, WaveformConfig):
                contents, callback_list =generate_tab_waveform(app, config_instance, key)
                tab.append(contents)
                data.append(html.Div(id=datastorage_id.id, children=to_store))

            #register_callbacks_datastorage(app, datastorage_id, callback_list)

    tabs = dcc.Tabs(id="config_tabs", children=tab)
    return tabs, data

def register_callbacks_datastorage(app, storage, callback_list):

    print("1")