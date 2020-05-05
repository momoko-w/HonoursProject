import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from urllib.parse import unquote
import dash_bootstrap_components as dbc
import pandas as pd

import views.main_components as main_components
from views.app import app
import mainController as mainCtrl
from controllers import dataController as dataCtrl, speakersController as speakersCtrl
import views.pages.debateTabs as debateTabs
from models import dataSetInfo
from views.pages import informationToolTip as infoModals

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

# page header for layout
header = html.Div(
    [
        # main heading
        dcc.Loading(
            main_components.generateMainHeader('Debate', 'debate-header'),
        ),

        # description of debate
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    html.Div(
                        children='Debate Topic',
                        style={
                            'textAlign': 'center',
                            'color': colors['text']
                        },
                        id='debate-description-div'
                    ),
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
body = html.Div(
    [
        # hidden div that helps with calling callbacks at page init
        html.Div(
            id='hidden-div'
        ),
        html.Div(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            # main tabs to select 3 data categories
                            dbc.Tabs(
                                [
                                    dbc.Tab(label="Debate Stats", tab_id="tab-debate"),
                                    dbc.Tab(label="Speakers Compared", tab_id="tab-speakers"),
                                    dbc.Tab(label="Speaker Stats", tab_id="tab-speaker")
                                ],
                                id="tabs",
                                active_tab="tab-debate",
                            ),
                            # divs that will contain the tab contents (set through init callback on page load
                            dcc.Loading(
                                html.Div(
                                    [
                                        html.H3("Loading...", id="first-load"),
                                        html.Div(
                                            id="debate_tab",
                                            hidden=True
                                        ),
                                        html.Div(
                                            id="speakers_tab",
                                            hidden=True
                                        ),
                                        html.Div(
                                            id="speaker_tab",
                                            hidden=True
                                        )
                                    ],
                                    id="tab-content",
                                    style={"padding": "10px"}
                                ),
                            )

                        ],
                        width=10,
                        align="center", style={"background-color": "#F9F9F9"}
                    ),
                    justify="center",
                    no_gutters=True
                )
            ]
        )
    ],
    style={
        "min-height": "100vh",
        "margin-bottom": "60px",
    }
)

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


## callback functions ##

@app.callback(
    [
        # Output("tab-content", "children"),
        Output("debate_tab", "hidden"),
        Output("speakers_tab", "hidden"),
        Output("speaker_tab", "hidden")
    ],
    [
        Input("tabs", "active_tab"),
        Input('url', 'search')
    ])
def switch_tab(activeTab, debateName):
    # old
    # # get full dataframes
    # dataframes = dataCtrl.fetchOrganisedData(debateName)
    # # get specific calculated and formatted data necessary for tab
    # data = mainCtrl.calculate_tab_data(debateName, dataframes)

    # trigger visibility of tab content depending on what the active tab is
    if activeTab == "tab-debate":
        return False, True, True
        # debateTabs.get_debate_tab(debateName, data),
    elif activeTab == "tab-speakers":
        return True, False, True
        # debateTabs.get_speakers_tab(debateName, data)
    elif activeTab == "tab-speaker":
        return True, True, False
        # debateTabs.get_speaker_tab(debateName, data), []
    return html.P("Error: This shouldn't be displayed."), []


@app.callback(
    [
        Output('debate-header', 'children'),
        Output('debate-description-div', 'children'),
        Output('debate-info-table', 'children'),
        Output("debate_tab", "children"),
        Output("speakers_tab", "children"),
        Output("speaker_tab", "children"),
        Output("first-load", "hidden")
    ],
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
        # set as empty, for when callback is called on home page
        tableData = pd.DataFrame({})
        table = dbc.Table.from_dataframe(tableData)
        debate_tab = []
        speakers_tab = []
        speaker_tab = []
    else:
        # set data for debate information table as pandas data frame
        tableData = pd.DataFrame(
            {
                "Debate Name": [debateName],
                "Number of Speakers": [dataSetInfo["noOfSpeakers"]],
                "Length": [str(dataSetInfo["length"]) + " min"],
                "Date Aired": dataSetInfo["date"]
            }
        )
        table = dbc.Table.from_dataframe(tableData, striped=True, bordered=True,
                                         hover=True)
        description = dataSetInfo["description"]

        # get specific calculated and formatted data necessary for tab
        data = mainCtrl.calculate_tab_data(debateName)
        participants = mainCtrl.get_participants_list(debateName)

        debate_tab = debateTabs.get_debate_tab(debateName, data)
        speakers_tab = debateTabs.get_speakers_tab(debateName, data, participants)
        speaker_tab = debateTabs.get_speaker_tab(debateName, data, participants)

    # return the debate name for the header, description and data for the info table
    return debateName, description, table, debate_tab, speakers_tab, speaker_tab, True


@app.callback(
    [
        # hardcoded in atm, would need to store data in between callbacks somehow
        # would need to increase this number if there was a debate with more than 25 speakers (max atm is 19)
        # probably unlikely though
        Output(f"speaker-content-{i}", "hidden") for i in range(0, 25)
    ],
    [
        Input("drop-speakers", "value")
        # Input("drop_speakers", "options")
    ]
)
def switch_speaker_dropdown(name_index):
    # set all speaker data as hidden, except for the value selected in the dropdown
    outputlist = [True] * 25
    outputlist[name_index] = False
    return outputlist
