import dash
import dash_bootstrap_components as dbc

CONFIG_NAMES = ["Density", "EFPS", "FABR", "FABV", "SFPS", "TFPS", "Density2"]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
