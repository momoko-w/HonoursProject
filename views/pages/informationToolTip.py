import dash_bootstrap_components as dbc
import pathlib
import json

def load_tip_file():
    # get file with participant names
    parent_dir = pathlib.Path(__file__).parent.parent
    path = parent_dir.joinpath("assets/tooltip_info.json").resolve()
    file = open(path.resolve(), "r")

    tooltips = json.loads(file.read())
    return tooltips


def get_tooltip(tip_name):
    tooltips = load_tip_file()
    text = tooltips[tip_name]
    return text


