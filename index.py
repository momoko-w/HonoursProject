import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from views.app import app
from views.pages import home_page, debate_analysis_page


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home_page.layout
    if pathname == '/home':
        return home_page.layout
    elif pathname == '/debate':
         return debate_analysis_page.layout
    else:
        return '404 - Page not found.'

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False)