import dash_html_components as html
import dash
from dash.dependencies import Input, Output
from urllib.parse import unquote

import views.main_components as main_components
from views.app import app
import mainController
from controllers import dataController as dataCtrl

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

# navigation bar for layout
navbar = main_components.generateNavBar()

# page header for layout
header = html.Div(
    [
        # main heading
        main_components.generateMainHeader('Debate', 'debate-header'),
        html.Div(
            children='Put description of debate here',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        )
    ]
)

# body for layout
body = html.Div([
    html.Div(
        id='hidden-div'
    )
])

layout = html.Div([
    # nav bar
    main_components.generateNavBar(),
    # header component
    header,
    # body component
    body
])


@app.callback(Output('debate-header', 'children'),
              [ # the hidden div allows for the callback to be called
                Input('hidden-div', 'children'),
                Input('url', 'search')])
def on_data_set_header(aux, debateName):
    # remove special character URL encoding and cut off ? at beginning
    debateName = unquote(debateName)[1:]
    return debateName
