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
    data = []
    for key, item in attributes.items():
        data.append({"attribute name": key, "value": str(item)})
        if isinstance(item, list):
            data[-1]["value"] = data[-1]["value"].replace("[", "{")
            data[-1]["value"] = data[-1]["value"].replace("]", "}")

    return dash_table.DataTable(
        id=id,
        columns=[{"name": i, "id": i} for i in ["attribute name", "value"]],
        data=data,
        editable=True,
    )
