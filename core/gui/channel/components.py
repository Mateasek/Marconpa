import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import base64


def attributes_table(id, attributes):
    """
    Constructs table for waveform display
    :param id: Table ID
    :param setpoints: Setpoints from waveform to fill the table
    :return:
    """
    data = [{"attribute name": key, "value": str(item)} for key, item in attributes.items()]

    return dash_table.DataTable(
        id=id,
        columns=[
            {"name": i, "id": i} for i in ["attribute name", "value"]
        ],
        data= data,
        editable=True,
    )
