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
        color="navy",
        dark="True"
    )
    return navbar


def generateMainHeader(text, color):
    heading = html.H1(
        children=text,
        style={
            'textAlign': 'center',
            'color': color,
            'margin': 10
        },
    )
    return heading

def create_accordion_item(i, title, content):
    #create Card
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        title,
                        color="link",
                        id=f"group-{i+1}-toggle",
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(content),
                id=f"collapse-{i+1}",
            ),
        ]
    )

def create_accordion_items(noOfItems, titleList, contentList):
    accordionItems = []
    for i in range(0, noOfItems):
        accordionItems.append(create_accordion_item(i, titleList[i], contentList[i]))
    return accordionItems

