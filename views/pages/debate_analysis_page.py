import dash_html_components as html
import dash
from dash.dependencies import Input, Output
from urllib.parse import unquote
import dash_bootstrap_components as dbc
import pandas as pd

import views.main_components as main_components
from views.app import app
import mainController as mainCtrl
from controllers import dataController as dataCtrl
import views.pages.debateTabs as debateTabs

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

# page header for layout
header = html.Div(
    [
        # main heading
        main_components.generateMainHeader('Debate', 'debate-header'),
        # description of debate
        dbc.Row(
            dbc.Col(
                html.Div(
                    children='Debate Topic',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    },
                    id='debate-description-div'
                ),
                width="auto"
            ),
            justify="center",
            no_gutters=True
        ),
        # table holding key metadata on debate
        main_components.generate_debate_info_table()
    ],
    style={"alignItems": "center"}
)

# body for layout
body = html.Div([
    # hidden div that helps with calling callbacks at page init
    html.Div(
        id='hidden-div'
    ),
    html.Div(
        [
            dbc.Row(
                dbc.Col(
                    children=[
                        dbc.Tabs(
                            [
                                dbc.Tab(label="Debate Stats", tab_id="tab-debate"),
                                dbc.Tab(label="Speakers Compared", tab_id="tab-speakers"),
                                dbc.Tab(label="Speaker Stats", tab_id="tab-speaker")
                            ],
                            id="tabs",
                            active_tab="tab-debate",
                        ),
                        html.Div(id="tab-content", style={"padding": "10px"}),
                    ],
                    width=10,
                    align="center", style={"background-color": "#F9F9F9"}
                ),
                justify="center",
                no_gutters=True
            )
        ]
    )
])

# set layout for entire page
layout = html.Div([
    # nav bar
    main_components.generateNavBar(),
    # header component
    header,
    # body component
    body,
    # footer for layout
    main_components.generate_footer()
])





@app.callback(
    Output("tab-content", "children"),
    [
        Input("tabs", "active_tab"),
        Input('url', 'search')
    ])
def switch_tab(activeTab, debateName):
    # remove special character URL encoding and cut off question mark at beginning
    debateName = unquote(debateName)[1:]

    # get full dataframes
    dataframes = dataCtrl.fetchOrganisedData(debateName)
    # get specific calculated and formatted data necessary for tab
    data = mainCtrl.calculate_tab_data(debateName, dataframes)

    if activeTab == "tab-debate":
        return debateTabs.get_debate_tab(debateName, data)
    elif activeTab == "tab-speakers":
        return debateTabs.get_speakers_tab(debateName, data)
    elif activeTab == "tab-speaker":
        return debateTabs.get_speaker_tab(debateName, data)
    return html.P("Error: This shouldn't be displayed.")


@app.callback(
    [Output('debate-header', 'children'),
     Output('debate-description-div', 'children'),
     Output('debate-info-table', 'children')],
    [  # the hidden div allows for the callback to be called
        Input('hidden-div', 'children'),
        Input('url', 'search')])
def on_init_set_page(aux, debateName):
    # remove special character URL encoding and cut off question mark at beginning
    debateName = unquote(debateName)[1:]
    description = ""
    # get data set information to display
    dataSetInfo = dataCtrl.get_debate_by_name(debateName)
    if "noOfSpeakers" not in dataSetInfo:
        # do nothing
        tableData = pd.DataFrame({})
    else:
        # set data for debate information table as pandas data frame
        tableData = pd.DataFrame(
            {
                "Debate Name": [debateName],
                "Number of Speakers": [dataSetInfo["noOfSpeakers"]],
                "Length": [str(dataSetInfo["length"]) + " min"]
            }
        )
        description = dataSetInfo["description"]

    # return the debate name for the header, description and data for the info table
    return debateName, description, dbc.Table.from_dataframe(tableData, striped=True, bordered=True,
                                                             hover=True)