import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from views.app import app
from dash.dependencies import Input, Output, State
import dash


def generateNavBar():
    navbar = dbc.Navbar(
        children=[
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=app.get_asset_url('LOGO.png'), height="30px")),
                        dbc.Col(
                            dbc.NavbarBrand("Debate Visualiser", className="ml-2")
                        ),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/home",
            )
        ],
        sticky="top",
        color="primary",
        dark="True"
    )
    return navbar


def generateMainHeader(text, id):
    heading = dbc.Row(
        dbc.Col(
            html.H1(
                id=id,
                children=text,
                style={
                    'textAlign': 'center',
                    'margin': 10
                },
            ),
            width="auto"
        ),
        justify="center",
        # set margin-bottom
        className="mb-4",
        # remove automatic spacing between columns
        no_gutters=True
    )

    return heading


def create_accordion_item(i, title, content):
    # create Card
    card = dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        title,
                        color="info",
                        id=f"group-{i + 1}-toggle",
                        block=True,
                        size="lg",
                        style={"padding": "10px"}
                    )
                ),
                style={"padding": "0px"}
            ),
            dbc.Collapse(
                dbc.CardBody(
                    [
                        html.P(
                            content,
                            className="card-text text-dark",
                        ),
                        dcc.Link(
                            dbc.Button(
                                "View Analysis",
                                color="primary",
                                id=f"analysis-button-{i + 1}",
                            ),
                            href="/debate?" + title
                        ),

                    ]
                ),
                id=f"collapse-{i + 1}",
            ),
        ],
        color="info",
        outline=True
    )
    return dbc.Row(
        dbc.Col(
            card,
            width="8"
        ),
        justify="center",
        # remove automatic spacing between columns
        no_gutters=True
    )


def create_accordion_items(noOfItems, titleList, contentList):
    accordionItems = []
    for i in range(0, noOfItems):
        accordionItems.append(create_accordion_item(i, titleList[i], contentList[i]))
    return accordionItems


def generate_footer():
    footer = dbc.Row(
        dbc.Col(
            html.Footer(
                html.Div(
                    [
                        "Icons made by ",
                        html.A("Freepik", href="https://www.flaticon.com/authors/freepik", title="Freepik"),
                        " from ",
                        html.A("www.flaticon.com", href="https://www.flaticon.com/", title="Flaticon"),
                    ],
                    className="bg-light ml-3",
                    id="footer-content"
                ),
                id="footer"
            ),
            # style={
            #     "position": "absolute",
            #     "bottom": "0",
            #     "width": "100%",
            #     "height": "60px",
            #     "lineHeight": "60px"
            # }
            style={"height": "60px", "lineHeight": "60px"}
        ),
        no_gutters=True
    )
    return footer


def generate_debate_info_table():
    table = dbc.Row(
        dbc.Col(
            dbc.Table(id="debate-info-table"),
            width="auto",
            className="mt-3"
        ),
        justify="center",
        no_gutters=True
    )
    return table
