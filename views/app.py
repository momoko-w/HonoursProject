import dash
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])
app.title = "Debate Wiz"
server = app.server
app.config.suppress_callback_exceptions = True
