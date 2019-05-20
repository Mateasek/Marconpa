import dash_core_components as dcc
import dash_html_components as html
from marconpa.core.gui.config.layout import (
    config_layout_channels,
    config_layout_waveform,
)


def generate_tab_channels(app, config_instance, key):

    textarea = generate_config_textarea(config_instance, key)
    tab = dcc.Tab(
        label=key,
        id=key,
        children=[
            config_layout_channels(key, config_instance, app),
            html.Details(
                [html.Summary("{0} Configuration File Text".format(key)), textarea]
            ),
        ],
    )

    return tab


def generate_tab_waveform(app, config_instance, key):

    textarea = generate_config_textarea(config_instance, key)
    tab = dcc.Tab(
        label=key,
        id=key + ": config,",
        children=[
            config_layout_waveform("config-" + key, config_instance, app),
            html.Details(
                [html.Summary("{0} Configuration File Text".format(key)), textarea]
            ),
        ],
    )
    return tab


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
