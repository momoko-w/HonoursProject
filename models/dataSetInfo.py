import json
import pathlib

# function to return the basic information on all available data sets
def get_dataSets_list():
    # get relative data directory
    PATH = pathlib.Path(__file__).parent.parent
    DATA_PATH = PATH.joinpath("models/list_of_datasets.json").resolve()
    file = open(DATA_PATH.resolve(), "r")
    # file = open('../models/list_of_datasets.json', "r")
    dataSetList = file.read()
    return json.loads(dataSetList)


# get list of names of all debates available
def get_debate_names():
    dataSets = get_dataSets_list()
    return [dataSet["name"] for dataSet in dataSets]


# get list of names of all debates available
def get_number_speakers():
    dataSets = get_dataSets_list()
    return [dataSet["noOfSpeakers"] for dataSet in dataSets]


def get_debate_descriptions():
    dataSets = get_dataSets_list()
    return [dataSet["description"] for dataSet in dataSets]


# find debate info by debate name
def get_debate_info(debateName):
    dataSets = get_dataSets_list()
    for dataSet in dataSets:
        if dataSet["name"] == debateName:
            return dataSet
    # if not found return empty
    return {}

# get the main text file for a specific debate
def get_textfile_name(debateName):
    dataSets = get_dataSets_list()
    for dataSet in dataSets:
        if dataSet["name"] == debateName:
            return dataSet["textfile"]
    return ""