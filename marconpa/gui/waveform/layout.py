import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from dash._utils import create_callback_id
import dash

from marconpa.gui.waveform.components import waveform_table, waveform_plot, insert_row_button, insert_row_table, deleterow_button, dropdown_delete_row
from marconpa.gui.waveform.callback import callback_tablechanged, callback_update_drwopdown_deleterows
from marconpa.gui.utils import IdHandler
from marconpa.gui.app import app
def waveform_layout(waveform, waveform_name, parent_id):
    """
    Constructs content for the waveform part
    :param waveform_id:
    :param waveform_name:
    :param waveform:
    :param app:
    :return:
    """
    waveform_id = IdHandler(name=waveform_name, kind="Waveform", parent=parent_id)

    table, table_id =  waveform_table(parent_id=waveform_id, setpoints=waveform.return_SetPoints())

    graph, graph_id = waveform_plot(parent_id=waveform_id, setpoints=waveform.return_SetPoints())

    insert_button, insert_button_id = insert_row_button(table_id)
    insert_table, insert_table_id = insert_row_table(insert_button_id)

    delete_button, delete_button_id = deleterow_button(table_id)
    dropdown, dropdown_id = dropdown_delete_row(delete_button_id)

    table_changes = dbc.Row([dbc.Col(insert_table), dbc.Col(insert_button),
                             dbc.Col(dropdown), dbc.Col(delete_button)])

    waveform_row = dbc.Row([dbc.Col(table), dbc.Col(graph)])

    return_div = html.Details(
        [html.Summary(waveform_name), html.Div([table_changes, waveform_row])], id=waveform_id.id
    )
    # add callback for change in table
    output = Output(graph_id.id, "figure")
    if not create_callback_id(output) in app.callback_map:
        app.callback(output, [Input(table_id.id, "data")])(callback_tablechanged)

    #add calback to update dropdown menu for row deletion
    output = Output(dropdown_id.id, "options")
    if not create_callback_id(output) in app.callback_map:
        app.callback(output, [Input(table_id.id, "data")])(callback_update_drwopdown_deleterows)

    return return_div, [table_id, graph_id, insert_table_id, insert_table_id, insert_button_id, delete_button_id, dropdown_id]


