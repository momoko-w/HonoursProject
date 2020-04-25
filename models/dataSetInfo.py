import json


# function to return the basic information on all available data sets
def get_dataSets_list():
    file = open('../models/list_of_datasets.json', "r")
    dataSetList = file.read()
    return json.loads(dataSetList)


# get list of names of all debates available
def get_debate_names():
    dataSets = get_dataSets_list()
    return [dataSet["name"] for dataSet in dataSets]


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