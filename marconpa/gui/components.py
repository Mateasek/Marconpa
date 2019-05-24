import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from marconpa.core.gui.config.layout import (
    config_layout_channels,
    config_layout_waveform,
)
from marconpa.core.gui.utils import IdHandler

def generate_tab_channels(config_instance, key):

    config_id = IdHandler(name=key, kind="ConfigFile")
    contents, callback_list= config_layout_channels(config_instance, config_id)
    textarea, textarea_id = generate_config_textarea(config_instance, config_id)
    button, button_id = generate_textarea_sendbutton(config_id)
    callback_list += [textarea_id, button_id]

    tab = dcc.Tab(
        label=key,
        id=config_id.id,
        children=[
            contents,
            html.Details(
                [html.Summary("{0} Configuration File Text".format(key)), html.Div([button, textarea])]
            ),
        ],
    )

    return tab, callback_list


def generate_tab_waveform(config_instance, key):

    config_id = IdHandler(name=key, kind="ConfigFile")
    contents, callback_list = config_layout_waveform(config_instance, config_id)

    textarea, textarea_id = generate_config_textarea(config_instance, config_id)
    button, button_id = generate_textarea_sendbutton(config_id)
    callback_list += [textarea_id, button_id]

    tab = dcc.Tab(
        label=key,
        id=config_id.id,
        children=[
            contents,
            html.Details(
                [html.Summary("{0} Configuration File Text".format(key)), html.Div([button, textarea])]
            ),
        ],
    )
    return tab, callback_list


def generate_config_textarea(config_instance, parent_id):
    textarea_id = IdHandler(name=parent_id.name, kind="textArea", parent=parent_id)
    textarea = html.Div(
        dbc.Textarea(
            placeholder="{0} configuration file".format(textarea_id.name),
            id=textarea_id.id,
            value=config_instance.as_string(),
            style={"width": "100%", "height": 600},
        )
    )

    return textarea, textarea_id

def generate_textarea_sendbutton(parent_id):

    button_id = IdHandler(name=parent_id.name, kind="sendConfigText", parent=parent_id)
    button = html.Div(
        html.Button("Apply Config Text", accessKey="z", title="ctrl+z", id=button_id.id)
    )
    return button, button_id

def generate_upload_layout():
    """
    Returns html.Div containing dcc.Upload, which server for file selection and upload.
    :return: Div
    """
    upload_id = IdHandler(name="fileUpload", kind="fileUpload")
    upload_output_id = IdHandler(name="Output", kind="fileUploadOutput", parent=upload_id)
    layout = html.Div(
        [
            dcc.Upload(
                id=upload_id.id,
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
            html.Div(id=upload_output_id.id),
        ]
    )



    return layout, upload_id, upload_output_id

