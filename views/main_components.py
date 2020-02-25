import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


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
    )
    return navbar


def generateMainHeader(text, color):
    heading = html.H1(
        children=text,
        style={
            'textAlign': 'center',
            'color': color
        }
    )
    return heading
