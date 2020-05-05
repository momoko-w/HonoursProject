import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
from dash.dependencies import Input, Output

import mainController as mainCtrl
from controllers import speakersController as speakersCtrl
from views import graph_elements, main_components
from views.pages import informationToolTip as infoTips
from views.app import app


def get_debate_tab(debateName, data):
    # pie graph for sentences/sentences w. argument units
    labels = ["Sentences without arg. units", "Senteces w. arg. units"]
    values = [data["count_sentences"] - data["count_sents_with_arg"], data["count_sents_with_arg"]]
    sent_pie_graph = graph_elements.get_pie_chart(labels, values)

    # row containing overview information + total scores
    overview = dbc.Row(
        [
            # overall average score
            dbc.Col(
                dbc.Card([
                    dbc.Modal(
                        id="modal",
                    ),
                    dbc.CardHeader(
                        [
                            "Overall Debate Score: " + str(data["score"]),
                            html.Br(),
                            main_components.generate_modal_button("btn_debate_score"),
                            dbc.Tooltip(
                                infoTips.get_tooltip("score"),
                                target="btn_debate_score",
                            ),
                        ],
                    ),
                    dbc.CardBody([
                        daq.Thermometer(
                            min=0,
                            max=100,
                            value=data["score"],
                            scale={
                                'start': 0, 'interval': 10,
                                'labelInterval': 1,
                                'custom': {'44.27': 'Average Score', }
                            },
                            # color={"gradient": True, "ranges": {"green": [0, 60], "yellow": [60, 80], "red": [80, 100]}},
                        ),
                    ])
                ]),
                width=2
            ),
            # number of argument units in debate
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        "No. of Argument Units",
                        html.Br(),
                        main_components.generate_modal_button("btn_arg_unit"),
                        dbc.Tooltip(
                            infoTips.get_tooltip("arg_units"),
                            target="btn_arg_unit",
                        ),
                    ]),
                    dbc.CardBody([
                        html.H4(data["count_arg_units"], id="count_inodes"),
                    ])
                ]),
                width="auto"
            ),
            # number of dialogue turns in the debate
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("No. of Dialogue Turns"),
                    dbc.CardBody([
                        html.H4(data["count_turns"], id="count_turns"),
                    ])
                ]),
                width="auto"
            ),
            # avg number of arg units per dialogue turn
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Arg. Units per turn"),
                    dbc.CardBody([
                        html.H4(str(data["avg_arg_turn"]) + " (Avg.)" ),
                    ])
                ]),
                width="auto"
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("No. of Sentences: " + str(data["count_sentences"])),
                    dbc.CardBody([
                        dcc.Graph(figure=sent_pie_graph, config={'displayModeBar': False})
                    ])
                ]),
                width=3
            ),
            # avg number of arg units per sentence
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Arg. Units per sentence"),
                    dbc.CardBody([
                        html.H4(str(data["avg_arg_sent"])  + " (Avg.)"),
                    ])
                ]),
                width="auto"
            ),
        ],
        style={"padding": "1%"},
    )

    # bar graph for supporting/supported arguments
    x_values = ["Arguments: Total", "Supporting Arguments", "Supported Arguments"]
    y_values = [data["count_arg_units"], data["count_supporting"], data["count_supported"]]
    text = [
        "",
        str(data["perc_supporting"]) + "% of all arguments support other arguments",
        str(data["perc_supported"]) + "% of all arguments are supported by other arguments"
    ]
    colors = ["#636EFA", "rgb(27, 158, 119)", "rgb(102, 194, 165)"]
    support_bar_graph = graph_elements.get_bar_graph_basic(x_values, y_values, text, colors)

    # bar graph for countering/countered arguments
    x_values = ["Arguments: Total", "Attacking Arguments", "Attacked Arguments"]
    y_values = [data["count_arg_units"], data["count_countering"], data["count_countered"]]
    text = [
        "",
        str(data["perc_countering"]) + "% of all arguments attack other arguments",
        str(data["perc_countered"]) + "% of all arguments are attacked by other arguments"
    ]
    colors = ["#636EFA", "#EF553B", "rgb(252, 141, 98)"]
    conflict_bar_graph = graph_elements.get_bar_graph_basic(x_values, y_values, text, colors)

    # bar graph for nodes that neither support nor counter
    x_values = ["Arguments: Total", "Standalone Arguments"]
    y_values = [data["count_arg_units"], data["count_single"]]
    text = [
        "",
        str(data["perc_single"]) + "% of all arguments neither attack nor support other arguments"
    ]
    colors = ["#636EFA", "rgb(55, 126, 184)"]
    single_bar_graph = graph_elements.get_bar_graph_basic(x_values, y_values, text, colors)

    # section for data on supporting & conflicting arguments
    support_counter = dbc.Row(
        [
            # bar graph for supporting and supported arguments
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Supporting & Supported Arguments"),
                    dbc.CardBody([
                        dcc.Graph(figure=support_bar_graph, config={'displayModeBar': False})
                    ])
                ]),
                width=4
            ),
            # bar graph for supporting and supported arguments
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Countering & Countered Arguments"),
                    dbc.CardBody([
                        dcc.Graph(figure=conflict_bar_graph, config={'displayModeBar': False})
                    ])
                ]),
                width=4
            ),
            # bar graph for argument nodes with no connection to other nodes
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Arguments with no support/conflict relation to others"),
                    dbc.CardBody([
                        dcc.Graph(figure=single_bar_graph, config={'displayModeBar': False})
                    ])
                ]),
                width=4
            ),
        ],
        style={"padding": "1%"},
    )

    # pie graph for arguments/arguments in linked structures
    labels = ["Arguments not in Linked structures", "Arguments in Linked Structures"]
    values = [data["count_arg_units"] - data["count_linked_arg"], data["count_linked_arg"]]
    linked_pie_graph = graph_elements.get_pie_chart(labels, values)

    linked_arg_structure = dbc.Row(
        [
            # number of linked structures found
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        "No. of Linked Structures",
                        html.Br(),
                        main_components.generate_modal_button("btn_linked"),
                        dbc.Tooltip(
                            infoTips.get_tooltip("linked_arg"),
                            target="btn_linked",
                        ),
                    ]),
                    dbc.CardBody([
                        html.H4(data["count_linked"]),
                        html.H6("1 linked structure every " + str(data["linked_ratio"]) + " arguments.")
                    ])
                ]),
                width=2
            ),
            # number of linked arguments in said structures compared to total
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("No. of Arg. in Linked Structures"),
                    dbc.CardBody([
                        dcc.Graph(figure=linked_pie_graph, config={'displayModeBar': False})
                    ])
                ]),
                width=3
            ),
            # avg number of arguments in linked structures
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Arguments per Linked Structure"),
                    dbc.CardBody([
                        html.H4(str(data["avg_linked_arg"]) + " (Avg.)"),
                    ])
                ]),
                width=2
            ),
        ],
        style={"padding": "1%"},
    )

    # pie graph for arguments/arguments in convergent structures
    labels = ["Arguments not in Convergent Structures", "Arguments in Convergent Structures"]
    values = [data["count_arg_units"] - data["count_convergent_arg"], data["count_convergent_arg"]]
    linked_pie_graph = graph_elements.get_pie_chart(labels, values)

    convergent_arg_structure = dbc.Row(
        [
            # number of linked structures found
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        "No. of Convergent Structures",
                        html.Br(),
                        main_components.generate_modal_button("btn_linked"),
                        dbc.Tooltip(
                            infoTips.get_tooltip("convergent_arg"),
                            target="btn_linked",
                        ),
                    ]),
                    dbc.CardBody([
                        html.H4(data["count_convergent"]),
                        html.H6("1 convergent structure every " + str(data["convergent_ratio"]) + " arguments.")
                    ])
                ]),
                width=2
            ),
            # number of linked arguments in said structures compared to total
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("No. of Arg. in Convergent Structures"),
                    dbc.CardBody([
                        dcc.Graph(figure=linked_pie_graph, config={'displayModeBar': False})
                    ])
                ]),
                width=3
            ),
            # avg number of arguments in linked structures
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Arguments per Convergent Structure"),
                    dbc.CardBody([
                        html.H4(str(data["avg_convergent_arg"]) + " (Avg.)"),
                    ])
                ]),
                width=2
            ),
        ],
        style={"padding": "1%"},
    )

    # full tab with headings and sections
    tab = [
        dbc.Row(
            dbc.Col(
                html.H1("Debate Overview"),

            ),
            className="mt-4"
        ),
        overview,
        dbc.Row(
            dbc.Col([
                html.H1("Support & Conflict"),
                main_components.generate_modal_button("btn_support"),
                dbc.Tooltip(
                    infoTips.get_tooltip("support_attack"),
                    target="btn_support",
                ),
            ]),
            className="mt-4"
        ),
        support_counter,
        dbc.Row(
            dbc.Col(
                html.H1("Argument Structures")
            ),
            className="mt-4"
        ),
        dbc.Row(
            dbc.Col(
                html.H3("Linked Arguments")
            ),
            className="mt-4"
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.H6("Example: "),
                    html.Img(src=app.get_asset_url('Linked_Arg.png'), width="auto", height="auto")
                ]
            ),
            className = "mt-4"
        ),
        linked_arg_structure,
        dbc.Row(
            dbc.Col(
                html.H3("Convergent Arguments")
            ),
            className="mt-4"
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.H6("Example: "),
                    html.Img(src=app.get_asset_url('Convergent_arg.png'), width="auto", height="auto")
                ]
            ),
            className="mt-4"
        ),
        convergent_arg_structure,
        dbc.Row(
            dbc.Col(
                html.H1("Word Cloud: Top 100 Key Words")
            ),
            className="mt-4 mb-3"
        ),
        dbc.Row(
            dbc.Col(
                html.Img(src=app.get_asset_url(debateName + '_wordcloud.jpg'), width="80%", height="auto"),
            ),
            style={
                'textAlign': 'center',
                'margin': 10
            },
        ),
    ]
    return tab


def get_speakers_tab(debateName, data, participants):
    # get specific calculated and formatted data necessary for tab
    overview = dbc.Row(
        [
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        "Avg. Speaker Score",
                        html.Br(),
                        main_components.generate_modal_button("btn_speaker_score"),
                        dbc.Tooltip(
                            infoTips.get_tooltip("speaker_score"),
                            target="btn_speaker_score",
                        ),
                    ]),
                    dbc.CardBody([
                        html.H4(data["speaker_avg_score"]),
                    ])
                ]),
                width="auto"
            )
        ],
        style={"padding": "1%"},
    )

    # get graph data and graph+table for number of arguments made per speaker
    graph_data = speakersCtrl.get_arg_table_graph_data(data, participants)
    speakers_arg_graph = graph_elements.get_speaker_arg_graph(graph_data["table_data"], graph_data["x_values"],
                                                              graph_data["y_values"])

    table_graph_arg = dbc.Row(
        [
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        "# of Arguments Made Per Speaker",
                        html.Br(),
                        main_components.generate_modal_button("btn_arg"),
                        dbc.Tooltip(
                            infoTips.get_tooltip("arg_units"),
                            target="btn_arg",
                        ),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(figure=speakers_arg_graph, config={'displayModeBar': False})
                    ])
                ]),
                width=12
            )
        ],
        style={"padding": "1%"},
    )

    # get data & graph for supporting per speaker
    supported_data = speakersCtrl.get_pro_con_graph_data(data, participants, "speaker_supported")
    speakers_supported_graph = graph_elements.get_speaker_table_dot_graph(supported_data["speaker_names"],
                                                                          supported_data["x_values"],
                                                                          supported_data["y_values"], "Supported")

    supported_graph = dbc.Row(
        [
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("No. of Supported Arguments Per Speaker"),
                    dbc.CardBody([
                        dcc.Graph(figure=speakers_supported_graph, config={'displayModeBar': False})
                    ])
                ]),
                width=12
            )
        ],
        style={"padding": "1%"},
    )

    # get data & graph for supporting per speaker
    supporting_data = speakersCtrl.get_pro_con_graph_data(data, participants, "speaker_supporting")
    speakers_supporting_graph = graph_elements.get_speaker_table_dot_graph(supporting_data["speaker_names"],
                                                                           supporting_data["x_values"],
                                                                           supporting_data["y_values"], "Supporting")

    supporting_graph = dbc.Row(
        [
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("No. of Arguments Per Speaker Supporting Other Arguments"),
                    dbc.CardBody([
                        dcc.Graph(figure=speakers_supporting_graph, config={'displayModeBar': False})
                    ])
                ]),
                width=12
            )
        ],
        style={"padding": "1%"},
    )

    # get data & graph for countered per speaker
    countered_data = speakersCtrl.get_pro_con_graph_data(data, participants, "speaker_countered")
    speakers_countered_graph = graph_elements.get_speaker_table_dot_graph(countered_data["speaker_names"],
                                                                          countered_data["x_values"],
                                                                          countered_data["y_values"], "Attacked")

    countered_graph = dbc.Row(
        [
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("No. of Arguments Attacked by Others"),
                    dbc.CardBody([
                        dcc.Graph(figure=speakers_countered_graph, config={'displayModeBar': False})
                    ])
                ]),
                width=12
            )
        ],
        style={"padding": "1%"},
    )

    # get data & graph for countering per speaker
    countering_data = speakersCtrl.get_pro_con_graph_data(data, participants, "speaker_countering")
    speakers_countering_graph = graph_elements.get_speaker_table_dot_graph(countering_data["speaker_names"],
                                                                           countering_data["x_values"],
                                                                           countering_data["y_values"], "Attacked")

    countering_graph = dbc.Row(
        [
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("No. of Arguments Attacked by Others"),
                    dbc.CardBody([
                        dcc.Graph(figure=speakers_countering_graph, config={'displayModeBar': False})
                    ])
                ]),
                width=12
            )
        ],
        style={"padding": "1%"},
    )

    tab = [
        dbc.Row(
            dbc.Col(
                html.H1("Speakers Overview")
            ),
            className="mt-4"
        ),
        overview,
        table_graph_arg,
        dbc.Row(
            dbc.Col(
                html.H1("Speakers' Supported Arguments")
            ),
            className="mt-4"
        ),
        supported_graph,
        dbc.Row(
            dbc.Col(
                html.H1("Supporting Arguments Made by Speakers")
            ),
            className="mt-4"
        ),
        supporting_graph,
        dbc.Row(
            dbc.Col(
                html.H1("Speakers' Attacked Arguments")
            ),
            className="mt-4"
        ),
        countered_graph,
        dbc.Row(
            dbc.Col(
                html.H1("Attacking Arguments Made by Speakers")
            ),
            className="mt-4"
        ),
        countering_graph,
    ]

    return tab


def generate_speaker_tab_content(speaker_names, data, participant_dicts):
    # get data with duplicates removed
    speakers_arg_data = speakersCtrl.get_arg_table_graph_data(data, participant_dicts)
    speakers_supporting_data = speakersCtrl.get_pro_con_graph_data(data, participant_dicts, "speaker_supporting")
    speakers_supported_data = speakersCtrl.get_pro_con_graph_data(data, participant_dicts, "speaker_supported")
    speakers_countering_data = speakersCtrl.get_pro_con_graph_data(data, participant_dicts, "speaker_countering")
    speakers_countered_data = speakersCtrl.get_pro_con_graph_data(data, participant_dicts, "speaker_countered")

    generated_contents = []

    # for each speaker, generate the contents
    for i in range(len(speaker_names)):
        # get name & number of total arguments made
        name = speakers_arg_data["x_values"][i]
        total_arg = speakers_arg_data["y_values"][i]

        # get score from data
        score = [speaker['score'] for speaker in data["speaker_scores"] if speaker["name"] == name][0]  # data[""]

        # check for name if supporting, ... arguments have been made and get number
        if name in speakers_supporting_data["speaker_names"]:
            index = speakers_supporting_data["speaker_names"].index(name)
            supporting = speakers_supporting_data["x_values"][index]
        else:
            supporting = 0

        if name in speakers_supported_data["speaker_names"]:
            index = speakers_supported_data["speaker_names"].index(name)
            supported = speakers_supported_data["x_values"][index]
        else:
            supported = 0

        if name in speakers_countering_data["speaker_names"]:
            index = speakers_countering_data["speaker_names"].index(name)
            countering = speakers_countering_data["x_values"][index]
        else:
            countering = 0

        if name in speakers_countered_data["speaker_names"]:
            index = speakers_countered_data["speaker_names"].index(name)
            countered = speakers_countered_data["x_values"][index]
        else:
            countered = 0

        # based on support/conflict data generate bar graphs
        # bar graph for supporting/supported arguments
        x_values = ["Arguments: Total", "Supporting Arguments", "Supported Arguments"]
        y_values = [total_arg, supporting, supported]
        text = [
            "",
            str(round(supporting / total_arg * 100, 2)) + "% of all arguments support other arguments",
            str(round(supported / total_arg * 100, 2)) + "% of all arguments are supported by other arguments"
        ]
        colors = ["#636EFA", "rgb(27, 158, 119)", "rgb(102, 194, 165)"]
        support_bar_graph = graph_elements.get_bar_graph_basic(x_values, y_values, text, colors)

        # bar graph for countering/countered arguments
        x_values = ["Arguments: Total", "Attacking Arguments", "Attacked Arguments"]
        y_values = [total_arg, countering, countered]
        text = [
            "",
            str(round(countering / total_arg * 100, 2)) + "% of all arguments attack other arguments",
            str(round(countered / total_arg * 100, 2)) + "% of all arguments are attacked by other arguments"
        ]
        colors = ["#636EFA", "#EF553B", "rgb(252, 141, 98)"]
        conflict_bar_graph = graph_elements.get_bar_graph_basic(x_values, y_values, text, colors)

        # generate tab content
        tab_content = html.Div(
            [
                # score & total
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader([
                                    "Speaker Score",
                                    html.Br(),
                                    main_components.generate_modal_button("btn_speaker_score"),
                                    dbc.Tooltip(
                                        infoTips.get_tooltip("speaker_score"),
                                        target="btn_speaker_score",
                                    ),
                                ]),
                                dbc.CardBody([
                                    html.H4(score),
                                    daq.Thermometer(
                                        min=0,
                                        max=100,
                                        value=score,
                                        scale={
                                            'start': 0, 'interval': 20,
                                            'labelInterval': 1,
                                            'custom': {data["speaker_avg_score"]: 'Average Score', }
                                        },
                                        # color={"gradient": True, "ranges": {"green": [0, 60], "yellow": [60, 80], "red": [80, 100]}},
                                    ),
                                ])
                            ]),
                            width=3
                        ),
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader([
                                    "Total Arguments Made",
                                    html.Br(),
                                    main_components.generate_modal_button("btn_arg"),
                                    dbc.Tooltip(
                                        infoTips.get_tooltip("arg_units"),
                                        target="btn_arg",
                                    ),
                                ]),
                                dbc.CardBody([
                                    html.H4(total_arg),
                                ])
                            ]),
                            width="auto"
                        ),
                    ],
                    style={"padding": "1%"},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader("Supporting & Supported Arguments"),
                                dbc.CardBody([
                                    dcc.Graph(figure=support_bar_graph, config={'displayModeBar': False})
                                ])
                            ]),
                            width=4
                        ),
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader("Attacking & Attack Arguments"),
                                dbc.CardBody([
                                    dcc.Graph(figure=conflict_bar_graph, config={'displayModeBar': False})
                                ])
                            ]),
                            width=4
                        ),
                    ],
                    style={"padding": "1%"},
                ),
            ],
            id="speaker-content-" + str(i),
            hidden=True
        )
        generated_contents.append(tab_content)

    return generated_contents


def get_speaker_tab(debateName, data, participants):
    # get data with duplicates removed
    names = speakersCtrl.get_speaker_names(data, participants)

    # drop down to select a speaker from
    name_options = names
    drop_down = dbc.Row(
        [
            dbc.Col(
                [
                    html.H4("Select a Speaker: "),
                    dcc.Dropdown(
                        id="drop-speakers",
                        options=[{'label': name, 'value': name_options.index(name)} for name in name_options],
                        value=0,
                        clearable=False,
                        style={"marginBottom": 50, "font-size": 12}
                    ),
                ],
                width="auto"
            )
        ],
        style={"padding": "1%"},
    )

    speaker_tab_contents = generate_speaker_tab_content(names, data, participants)

    # all sections put together with headings
    speaker_tab = [
                      dbc.Row(
                          dbc.Col(
                              html.H1("Speaker Overview")
                          ),
                          className="mt-4"
                      ),
                      drop_down,
                      # hidden div that helps with calling callbacks at page init
                      html.Div(
                          id='hidden-div2'
                      ),
                  ] + speaker_tab_contents

    return speaker_tab

# app.callback(Output(f"speaker_content_{i}", "hidden") for i in range(0, 14)), [Input("drop_speakers", "value")])(
#         test)
