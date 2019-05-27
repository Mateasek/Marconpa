import dash_core_components as dcc
import dash_html_components as html
import dash
import base64
import json
from dash._utils import create_callback_id
from dash.dependencies import Input, Output, State
from marconpa.core.parser.lark import MarteConfigParser
from marconpa.core import (
    config_types,
    StandartConfig,
    WaveformConfig,
    EFPS,
)

from marconpa.gui.components import generate_tab_channels, generate_tab_waveform
from marconpa.gui.utils import IdHandler, CallbackHandler
from marconpa.gui.utils.conversions import waveformsetpoints2tabledata, channelattributes2tabledata, tabledata2channelattributes, callback_table_as_waveform
from marconpa.gui.app import app, CONFIG_NAMES
from copy import copy, deepcopy

def tab_structure_from_files(list_of_contents, list_of_names):
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
        if key in CONFIG_NAMES:
            content_type, content_string = item.split(",")
            decoded = base64.b64decode(content_string).decode()
            to_store = json.dumps({"config_type":key, "content": decoded})

            parsed = parser.parse_config(decoded)
            config_instance = config_types[key].from_parsed(parsed)
            datastorage_id = IdHandler(name=key, kind="DataStorage")
            if isinstance(config_instance, StandartConfig) or isinstance(
                config_instance, EFPS
            ):
                contents, callback_list = generate_tab_channels(config_instance, key)
                tab.append(contents)
                data.append(html.Div(id=datastorage_id.id, children=to_store))

            if isinstance(config_instance, WaveformConfig):
                contents, callback_list =generate_tab_waveform(config_instance, key)
                tab.append(contents)
                data.append(html.Div(id=datastorage_id.id, children=to_store))

            register_callbacks_datastorage(callback_list)

    tabs = dcc.Tabs(id="config_tabs", children=tab)
    return tabs, data

def register_callbacks_datastorage(callback_list):

    #add callback updating data storage
    tables = []
    buttons = []
    textareas = []
    insertrows_buttons = []
    deleterows_button = []
    insertrows_table = []
    deleterows_dropdown = []
    for callback_id in callback_list:
        if callback_id.name == "table" and callback_id.kind in ("Waveform", "Attributes"):
            tables.append(callback_id)
        elif callback_id.kind == "sendConfigText":
            buttons.append(callback_id)
        elif callback_id.kind == "textArea":
            textareas.append(callback_id)
        elif callback_id.name == "insertRowButton" and callback_id.kind == "Waveform":
            insertrows_buttons.append(callback_id)
        elif callback_id.name == "deleteRowButton" and callback_id.kind == "Waveform":
            deleterows_button.append(callback_id)
        elif callback_id.name == "insertrowTable" and callback_id.kind == "Waveform":
            insertrows_table.append(callback_id)
        elif callback_id.name == "deleteRowDropdown" and callback_id.kind == "Waveform":
            deleterows_dropdown.append(callback_id)

    inputs = [Input(i.id, "data") for i in tables]
    outputs = [Output(i.id, "value") for i in textareas]
    if not create_callback_id(outputs) in app.callback_map:
        app.callback(outputs, inputs,)(data_update_textarea)

    #the first part of outputs and states containing tables has to be identical!
    #table outputs are identified through states
    outputs = [Output(i.id, "data") for i in tables]
    status = [State(i.id, "data") for i in tables]

    #add contents of textarea through state
    status += [State(i.id, "value") for i in textareas]

    inputs = [Input(i.id, "n_clicks") for i in buttons]
    inputs += [Input(i.id, "n_clicks") for i in insertrows_buttons]
    inputs += [Input(i.id, "n_clicks") for i in deleterows_button]
    status += [State(i.id, "data") for i in insertrows_table]
    status += [State(i.id, "value") for i in deleterows_dropdown]

    if not create_callback_id(outputs) in app.callback_map:
        app.callback(output=outputs, inputs=inputs, state=status)(data_update_tables)

def data_update_textarea(*args):

    triggers, inputs, states =get_idhandlers_context(dash.callback_context)

    cont = True
    level = triggers[0].idhandler
    while cont:
        if level.parent is not None:
            level = level.parent
        else:
            cont = False

    if level.kind == "ConfigFile":
        config = config_types[level.name]()

    for table in inputs:
        if table.idhandler.kind == "Attributes":
            config = set_channelattributes_from_attributestable(config, table)
        elif table.idhandler.kind == "Waveform" and table.idhandler.name == "table":
            config = set_channelwaveform_from_waveformtable(config, table)

    return [config.as_string()]

def data_update_tables(*args):

    triggers, inputs, states = get_idhandlers_context(dash.callback_context)

    outputs = []
    output_tables = []
    for state in states:
        if state.idhandler.name == "table" and state.idhandler.kind in ("Waveform", "Attributes"):
            output_tables.append(state)


    for trigger in triggers:
        #react to callback fired by sendConfigTextArea button press
        if trigger.idhandler.kind == "sendConfigText" and trigger.callback_property == "n_clicks":
            for state in states:
                if state.idhandler.kind == "textArea" and state.idhandler.name == trigger.idhandler.name:
                    outputs = fired_by_textarea_sendtext(state, output_tables, outputs)
        #react to callback fired by add row button in waveform or attributes
        elif (trigger.callback_property == "n_clicks" and trigger.idhandler.name == "insertRowButton" and
              trigger.idhandler.parent.kind in ("Waveform", "Attributes")):
            for output_table in output_tables:
                if trigger.idhandler.parent.id == output_table.idhandler.id:
                    for state in states:
                        if state.idhandler.parent.id == trigger.idhandler.id:
                            outputs.append(insert_row_table(output_table.callback_data, state.callback_data))
                            break
                else:
                    outputs.append(output_table.callback_data)

        elif (trigger.callback_property == "n_clicks" and trigger.idhandler.name == "deleteRowButton" and
              trigger.idhandler.parent.kind in ("Waveform", "Attributes")):
            for output_table in output_tables:
                if trigger.idhandler.parent.id == output_table.idhandler.id:
                    for state in states:
                        if state.idhandler.parent.id == trigger.idhandler.id:
                            outputs.append(delete_row_waveform(output_table.callback_data, state.callback_data))
                            break
                else:
                    outputs.append(output_table.callback_data)

    return outputs

def delete_row_waveform(table_data, rownumber):
    table_data.pop(rownumber)
    for index, row in enumerate(table_data):
        row["index"] = str(index)

    return table_data

def insert_row_table(table_data, row):
    index = int(row[0]["index"])
    if index < 0 or index > len(table_data):
        table_data += row
        table_data[-1]["index"] = str(len(table_data) - 1)
    else:
        table_data.insert(index, row[0])
        for i in range(index+1, len(table_data)):
            table_data[i]["index"] = str(int(table_data[i]["index"])+1)
    return table_data

def get_idhandlers_context(context):
    triggers =[]
    for trigger in context.triggered:
        triggers.append(CallbackHandler.from_callback_context(trigger["prop_id"], trigger["value"]))

    inputs = []
    for key, item in context.inputs.items():
        inputs.append(CallbackHandler.from_callback_context(key, item))

    states = []
    for key, item in context.states.items():
        states.append(CallbackHandler.from_callback_context(key, item))

    return triggers, inputs, states

def get_data_attributes(config, table):

    level = table.idhandler.parent
    cont = True
    table_member = {}

    while cont:
        if level.kind == "Channel":
            table_member["Channel"] = level.name
        elif level.kind == "ConfigFile":
            table_member["config"] = level.name

        if level.parent:
            level = level.parent
        else:
            cont = False

    table_data = getattr(config, table_member["Channel"]).attributes
    table = channelattributes2tabledata(table_data)

    return table

def get_data_waveform(config, table):

    level = table.idhandler
    cont = True
    table_member = {}
    while cont:
        if level.kind == "Waveform" and not level.name == "table":
            table_member["waveform"] = level.name
        elif level.kind == "Channel":
            table_member["channel"] = level.name
        elif level.kind == "ConfigFile":
            table_member["config"] = level.name

        if level.parent:
            level = level.parent
        else:
            cont = False

    if "channel" in table_member.keys():
        channel = getattr(config, table_member["channel"])

        if table_member["waveform"] == "Enabled":
            table_data = channel.Enabled
        else:
            table_data = channel.waveforms[table_member["waveform"]]

        table = waveformsetpoints2tabledata(table_data.return_SetPoints())
    else:
        table = waveformsetpoints2tabledata(config.waveform.return_SetPoints())

    return table

def set_channelattributes_from_attributestable(config, table):



    attributes = tabledata2channelattributes(table.callback_data)
    level = table.idhandler.parent
    cont = True
    table_member = {}

    while cont:
        if level.kind == "Channel":
            table_member["Channel"] = level.name
        elif level.kind == "ConfigFile":
            table_member["config"] = level.name

        if level.parent:
            level = level.parent
        else:
            cont = False

    channel = getattr(config, table_member["Channel"])
    setattr(channel, "attributes", attributes)
    return config

def set_channelwaveform_from_waveformtable(config, table):

    waveform = callback_table_as_waveform(table.callback_data)
    level = table.idhandler
    cont = True
    table_member = {}
    while cont:
        if level.kind == "Waveform" and not level.name == "table":
            table_member["waveform"] = level.name
        elif level.kind == "Channel":
            table_member["channel"] = level.name
        elif level.kind == "ConfigFile":
            table_member["config"] = level.name

        if level.parent:
            level = level.parent
        else:
            cont = False

    if "channel" in table_member.keys():
        channel = deepcopy(getattr(config, table_member["channel"]))

        if table_member["waveform"] == "Enabled":
            channel.Enabled = waveform
        else:
            channel.waveforms[table_member["waveform"]] = waveform
        setattr(config, table_member["channel"], channel)
    else:
        config.waveform = waveform

    return config

def fired_by_textarea_sendtext(state,output_tables, outputs):

    parser = MarteConfigParser()
    #try:
    parsed = parser.parse_config(state.callback_data)
    #except Exception:
    #    raise dash.exceptions.PreventUpdate()
    config = config_types[state.idhandler.name].from_parsed(parsed)

    for table in output_tables:
        if table.idhandler.kind == "Attributes":
            outputs.append(get_data_attributes(config, table))
        if table.idhandler.kind == "Waveform" and table.idhandler.name == "table":
            outputs.append(get_data_waveform(config, table))


    return outputs

