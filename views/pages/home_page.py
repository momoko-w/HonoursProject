import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import main_components
from app import app

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

navbar = main_components.generateNavBar()

header = html.Div([
    # main heading
    main_components.generateMainHeader('Debate Visualiser', colors['text']),
    html.Div(children='Tool to visualise and score debates. Put desciption of project here', style={
        'textAlign': 'center',
        'color': colors['text']
    }, ),
    html.Div(
        id="tabs",
        className="row tabs",
        children=[
            dcc.Link("Debate Statistics", href="/"),
            dcc.Link("Compare Speakers", href="/"),
            dcc.Link("Individual Speakers", href="/"),
        ],
    ),
    html.Div(
        id="mobile_tabs",
        className="row tabs",
        style={"display": "none"},
        children=[
            dcc.Link("Opportunities", href="/"),
            dcc.Link("Leads", href="/"),
            dcc.Link("Cases", href="/"),
        ],
    )
])

layout = html.Div([
    # nav bar
    main_components.generateNavBar(),
    # main heading
    main_components.generateMainHeader('Debate Visualiser', colors['text']),
    html.Div(
        id="tabs",
        className="row tabs",
        children=[
            dcc.Link("Debate Statistics", href="/"),
            dcc.Link("Compare Speakers", href="/"),
            dcc.Link("Individual Speakers", href="/"),
        ],
    ),
    html.Div(
        id="mobile_tabs",
        className="row tabs",
        style={"display": "none"},
        children=[
            dcc.Link("Opportunities", href="/"),
            dcc.Link("Leads", href="/"),
            dcc.Link("Cases", href="/"),
        ],
    ),
    html.Div(children='Tool to visualise and score debates. Put desciption of project here', style={
        'textAlign': 'center',
        'color': colors['text']
    }, ),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'A', 'B', 'C'
            ]
        ]
    ),
    html.Div(id='app-1-display-value'),
    dcc.Link('Go to App 2', href='/home')
])


@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
