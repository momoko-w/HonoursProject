import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from app import app
from dash.dependencies import Input, Output, State
import dash


def generateNavBar():
    navbar = dbc.Navbar(
        children=[
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="assets/LOGO.jpg", height="30px")),
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
    heading = html.H1(
        id=id,
        children=text,
        style={
            'textAlign': 'center',
            'margin': 10
        },
    )
    return heading


def create_accordion_item(i, title, content):
    # create Card
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        title,
                        color="info",
                        id=f"group-{i + 1}-toggle"
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(
                    [
                        html.P(
                            content,
                            className="card-text",
                        ),
                        dcc.Link(
                            dbc.Button(
                                "View Analysis",
                                color="primary",
                                id=f"analysis-button-{i + 1}",
                            ),
                            href="/debate?"+title
                        ),

                    ]
                ),
                id=f"collapse-{i + 1}",
            ),
        ],
        color="info"
    )


def create_accordion_items(noOfItems, titleList, contentList):
    accordionItems = []
    for i in range(0, noOfItems):
        accordionItems.append(create_accordion_item(i, titleList[i], contentList[i]))
    return accordionItems
