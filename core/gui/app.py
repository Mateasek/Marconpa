import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from marconpa.core.gui.callbacks import tab_structure_from_files


class Marta:
    CONFIG_NAMES = ["Density", "EFPS", "FABR", "FABV", "SFPS", "TFPS", "Density2"]

    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.app.config["suppress_callback_exceptions"] = True

        # generates clicking stuff to initiate file selection and upload
        upload_layout = self.generate_upload_layout()

        # compose general layout
        layout = html.Div(
            [
                upload_layout,
                html.Div(id="div_tabs"),
                html.Div(id="data_div", style={"display": "none"}),
            ]
        )

        # set app layout
        self.app.layout = dbc.Container([layout])

        # calback initializing tabs and their content after upload
        self.app.callback(
            [Output("div_tabs", "children"), Output("data_div", "children")],
            [Input("upload-data", "contents")],
            [State("upload-data", "filename")],
        )(self.tab_structure)

    def tab_structure(self, list_of_contents, list_of_names):
        return tab_structure_from_files(self, list_of_contents, list_of_names)

    def generate_upload_layout(self):
        """
        Returns html.Div containing dcc.Upload, which server for file selection and upload.
        :return: Div
        """
        layout = html.Div(
            [
                dcc.Upload(
                    id="upload-data",
                    children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
                    style={
                        "width": "100%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "margin": "10px",
                    },
                    # Allow multiple files to be uploaded
                    multiple=True,
                ),
                html.Div(id="output-data-upload"),
            ]
        )

        return layout


if __name__ == "__main__":
    marta = Marta()
    marta.app.run_server(debug=True)
