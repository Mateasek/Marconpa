import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from marconpa.gui.utils import IdHandler
from marconpa.utils.conversions import list2string
from marconpa.gui.channel.callbacks import callback_update_drwopdown_deleterows
from dash._utils import create_callback_id
from marconpa.gui.app import app

def attributes_table(attributes, parent_id):
    """
    Constructs table for waveform display
    :param id: Table ID
    :param setpoints: Setpoints from waveform to fill the table
    :return:
    """
    data = []
    table_id = IdHandler(name="table", kind="Attributes", parent=parent_id)
    insert_button, insert_button_id = insert_row_button(table_id)
    insert_table, insert_table_id = insert_row_table(insert_button_id)

    delete_button, delete_button_id = deleterow_button(table_id)
    dropdown, dropdown_id = dropdown_delete_row(delete_button_id)

    table_changes = dbc.Row([dbc.Col(insert_table), dbc.Col(insert_button),
                             dbc.Col(dropdown), dbc.Col(delete_button)])


    index = 0
    for key, item in attributes.items():
        if isinstance(item, list):
           item = list2string(item)
        data.append({"index": index, "attribute name": key, "value": str(item)})
        index += 1

    table = dash_table.DataTable(
        id=table_id.id,
        columns=[{"name": i, "id": i} for i in ["index", "attribute name", "value"]],
        data=data,
        editable=True,
    )


    #add calback to update dropdown menu for row deletion
    output = Output(dropdown_id.id, "options")
    if not create_callback_id(output) in app.callback_map:
        app.callback(output, [Input(table_id.id, "data")])(callback_update_drwopdown_deleterows)

    return_div = html.Div([table_changes, html.Div(table)])

    return return_div,  [table_id, insert_button_id, insert_table_id, delete_button_id, dropdown_id]

def insert_row_table(parent_id):

    row_table_id = IdHandler(name="insertrowTable", kind="Waveform", parent=parent_id)

    columns = [{"name": i, "id": i} for i in ["index", "attribute name", "value"]]
    data = [{"index": 0, "attribute name": "", "value": ""}]

    table =html.Div(dash_table.DataTable(
        id=row_table_id.id,
        columns= columns,
        data=data,
        editable=True,
    ))
    return table, row_table_id

def insert_row_button(parent_id):

    button_id = IdHandler(name="insertRowButton", kind="Waveform", parent=parent_id)

    button = html.Div(
        html.Button("Insert Row", accessKey="z", title="ctrl+z", id=button_id.id)
    )
    return button, button_id


def dropdown_delete_row(parent_id):
    dropdown_id = IdHandler(name="deleteRowDropdown", kind="Waveform", parent=parent_id)

    dropdown = html.Div([dcc.Dropdown(id=dropdown_id.id, options=[{"label": 0, "value": 0}], value=0)],
                        )

    return dropdown, dropdown_id

def deleterow_button(parent_id):

    button_id = IdHandler(name="deleteRowButton", kind="Waveform", parent=parent_id)

    button = html.Div(
        html.Button("Delete Row", accessKey="z", title="ctrl+z", id=button_id.id)
    )

    return button, button_id