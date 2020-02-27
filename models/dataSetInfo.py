import json


#function to return the basic information on all available data sets
def get_dataSet_list():
    file = open('../models/list_of_datasets.json', "r")
    dataSetList = file.read()
    return json.loads(dataSetList)

#get list of names of all debates available
def get_debate_names():
    dataSets = get_dataSet_list()
    return [ dataSet["name"] for dataSet in dataSets]

def get_debate_descriptions():
    dataSets = get_dataSet_list()
    return [dataSet["description"] for dataSet in dataSets]