import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import views.main_components as main_components
from views.app import app
import mainController
from controllers import dataController as dataCtrl

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

# nav bar for layout
navbar = main_components.generateNavBar()

# header for layout
header = html.Div(
    [
        # main heading
        main_components.generateMainHeader('Debate Visualiser', 'main-header'),
        dbc.Row(
            dbc.Col(
                html.Div(
                    children='Tool to visualise and score debates. Put description of project here',
                    style={
                        'textAlign': 'center',
                        'color': colors['text'],
                        "background-color": "white",
                        "padding": "5px"
                    },
                    id='debate-description-div',
                    className="mb-3"
                ),
                width="auto"
            ),
            justify="center",
            no_gutters=True
        ),
    ]
)

# body for layout
accordionItems = main_components.create_accordion_items(dataCtrl.get_no_of_debates(), dataCtrl.get_debate_names(),
                                                        dataCtrl.get_debate_descriptions())

body = html.Div(
    [
        html.Div(
            accordionItems, className="accordion"
        )
    ],
    style={
        "min-height": "100vh",
        "margin-bottom": "-60px",
    }
)

layout = html.Div(
    [
        # nav bar

        main_components.generateNavBar(),
        # header component
        header,
        # body component
        body,
        main_components.generate_footer()
    ],
    style={
        "background-image": "url(\"/assets/background.png\")",
        "background-repeat": "repeat",
        "background-position": "top",
        #"height": "100vh"
    }
)


# dynamic callback function for the accordion and collapsible items in it
@app.callback(
    # output will set the is_open property of the collapsible elements
    [Output(f"collapse-{i}", "is_open") for i in range(1, dataCtrl.get_no_of_debates() + 1)],
    # input is the click event, when an accordion item is clicked
    [Input(f"group-{i}-toggle", "n_clicks") for i in range(1, dataCtrl.get_no_of_debates() + 1)],
    # state is the states of the is_open property of all collapsible elements
    [State(f"collapse-{i}", "is_open") for i in range(1, dataCtrl.get_no_of_debates() + 1)],
)
# using argv here, since number of arguments for this function depends on number of debates stored
def toggle_accordion(*argv):
    # Parameters: for each debate element in the accordion there will be a click event
    # and the value for whether it is collapsed or open as input
    nclicks = []
    isOpen = []

    # separate the arguments in argv into click events and isOpen states
    for i in range(len(argv)):
        if i < int(len(argv) / 2):
            nclicks.append(argv[i])
        else:
            isOpen.append(argv[i])

    # get the id for the element clicked
    context = dash.callback_context
    if not context.triggered:
        return ""
    else:
        button_id = context.triggered[0]["prop_id"].split(".")[0]

    # since output needs to be list of states for is_open properties of all collapsible elements,
    # need output list the length of number of debates stored (which is the number of collapsible elements)
    outputlist = [False] * int(len(argv) / 2)

    for i in range(int(len(argv) / 2)):
        # find button that was clicked and change state of is_open for output
        if button_id == f"group-{i + 1}-toggle" and nclicks[i]:
            outputlist[i] = not isOpen[i]
            return outputlist
    # fail safe in case something went wrong: return list with all states as false
    return outputlist
