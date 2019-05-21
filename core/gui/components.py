import dash_core_components as dcc
import dash_html_components as html
from marconpa.core.gui.config.layout import (
    config_layout_channels,
    config_layout_waveform,
)
from marconpa.core.gui.utils import IdHandler

def generate_tab_channels(app, config_instance, key):

    textarea = generate_config_textarea(config_instance, key)
    config_id = IdHandler(name=key, component_type="ConfigFile")
    contents, callback_list= config_layout_channels(app, config_instance, config_id)
    tab = dcc.Tab(
        label=key,
        id=config_id.id,
        children=[
            contents,
            html.Details(
                [html.Summary("{0} Configuration File Text".format(key)), textarea]
            ),
        ],
    )

    return tab, callback_list


def generate_tab_waveform(app, config_instance, key):

    textarea = generate_config_textarea(config_instance, key)
    config_id = IdHandler(name=key, component_type="ConfigFile")
    contents, callbacks = config_layout_waveform(app, config_instance, config_id)
    tab = dcc.Tab(
        label=key,
        id=config_id.id,
        children=[
            contents,
            html.Details(
                [html.Summary("{0} Configuration File Text".format(key)), textarea]
            ),
        ],
    )
    return tab, callbacks


def generate_config_textarea(config_instance, key):
    textarea = html.Div(
        dcc.Textarea(
            placeholder="{0} configuration file".format(key),
            id="text_{0}".format(key),
            value=config_instance.as_string(),
            style={"width": "100%", "height": 600},
        )
    )

    return textarea

def generate_upload_layout():
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

