import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from marconpa.gui.callbacks import tab_structure_from_files
from marconpa.gui.components import generate_upload_layout
from marconpa.gui.app import app
from marconpa.gui.utils import IdHandler

# generates clicking stuff to initiate file selection and upload
upload_layout, upload_id, upload_output_id = generate_upload_layout()

tabs_id = IdHandler(name="configFiles", kind="tabs")
datastorage_id = IdHandler(name="configs", kind="datastorage")
# compose general layout
layout = html.Div(
    [
        upload_layout,
        html.Div(id=tabs_id.id),
        html.Div(id=datastorage_id.id, style={"display": "none"}),
    ]
)


app.callback(
    [Output(tabs_id.id, "children"), Output(datastorage_id.id, "children")],
    [Input(upload_id.id, "contents")],
    [State(upload_id.id, "filename")])(tab_structure_from_files)

# set app layout
app.layout = dbc.Container([layout])


if __name__ == "__main__":

    app.run_server(debug=True)

