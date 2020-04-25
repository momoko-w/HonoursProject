import timeit
import json
import pathlib

import mainController
from controllers import dataController

# run calculations for 5 debates to get averages to compare against
debate_names = ["Green Belt - Moral Maze"]
    #, "Hypocrisy - Moral Maze", "Syria - Moral Maze",
                #"Problem Families - Moral Maze", "Welfare - Moral Maze"]

dataframes = []
for debate in debate_names:
    dataframes.append(dataController.fetchOrganisedData(debate))

# calculate tab data for each debate
tab_data = []
for i in range(len(debate_names)):
    tab_data.append(mainController.calculate_tab_data(debate_names[i], dataframes[i]))

debate_data = {
    # overview data
    "count_arg_units": "Error",
    # data on NL text from full transcript
    "count_turns": "Error",
    "avg_arg_turn": "Error",
    "count_sentences": "Error",
    "count_sents_with_arg": "Error",
    "avg_arg_sent": "Error",
    # support
    "count_support": "Error",
    # conflict
    "count_conflict": "Error",
    # score data
    "score": "Error",
}

standards = {
    "score": {
        "avg": 0,
        "min": 0,
        "max": 100
    },
    "avg_arg_turn": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "count_sents_with_arg": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "avg_arg_sent": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
}

# get relative data directory
parent_dir = pathlib.Path(__file__).parent.parent
path = parent_dir.joinpath("views\\result_standards.json").resolve()
with open(path, 'w') as file:
    json.dump(standards, file)
