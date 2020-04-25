import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

import mainController as mainCtrl
from views import graph_elements


def get_debate_tab(debateName, data):
    # get all graph elements
    # stacked graph bar for sentences/sentences w. argument units
    labels = ["Sentences without arg. units", "Senteces w. arg. units"]
    values = [data["count_sentences"] - data["count_sents_with_arg"], data["count_sents_with_arg"]]
    sent_pie_graph = graph_elements.get_pie_chart(labels, values)

    # row containing overview information + total scores
    overview = dbc.Row([
        # overall average score
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Overall Debate Score"),
                dbc.CardBody([
                    html.H4(data["score"], className="card-title", id="debate-score"),
                ])
            ]),
            width="auto"
        ),
        # number of argument units in debate
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("No. of Argument Units"),
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
                    html.H4("∅ " + str(data["avg_arg_turn"])),
                ])
            ]),
            width="auto"
        ),
    ],
        style={"padding": "1%"},
    )

    sentences = dbc.Row(
        [
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
                        html.H4("∅ " + str(data["avg_arg_sent"])),
                    ])
                ]),
                width="auto"
            ),
        ],
        style={"padding": "1%"},
    )

    # section for data on supporting arguments
    support = dbc.Row(
        [
            # number of supporting arguments
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("No. of Supporting Nodes"),
                    dbc.CardBody([
                        html.H4(data["count_support"]),
                    ])
                ]),
                width="auto"
            )
        ],
        style={"padding": "1%"},
    )

    # section for data on conflicting arguments
    conflict = dbc.Row(
        [
            # number of conflicting arguments
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("No. of Conflicting Nodes"),
                    dbc.CardBody([
                        html.H4(data["count_conflict"]),
                    ])
                ]),
                width="auto"
            )
        ],
        style={"padding": "1%"},
    )

    tab = [
        dbc.Row(
            dbc.Col(
                html.H1("Debate Overview")
            ),
            className="mt-4"
        ),
        overview,
        sentences,
        dbc.Row(
            dbc.Col(
                html.H1("Support & Conflict")
            ),
            className="mt-4"
        ),
        support,
        conflict
    ]
    return tab


def get_speakers_tab(debateName, dataframes):
    # get specific calculated and formatted data necessary for tab
    overview = dbc.Row(

    )

    tab = [
        dbc.Row(
            dbc.Col(
                html.H1("Speakers Overview")
            ),
            className="mt-4"
        ),
        overview
    ]
    return tab


def get_speaker_tab(debateName, dataframes):
    # get specific calculated and formatted data necessary for tab

    return []
