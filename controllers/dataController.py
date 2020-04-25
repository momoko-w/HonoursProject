import json
import pandas as pd

from models import dataSetInfo
from models import dataLoader


# methods for getting meta data on data sets
def get_dataset_list():
    return dataSetInfo.get_dataSets_list()


def get_debate_names():
    return dataSetInfo.get_debate_names()


def get_no_of_debates():
    return len(get_dataset_list())


def get_debate_descriptions():
    return dataSetInfo.get_debate_descriptions()


def get_debate_by_name(debateName):
    return dataSetInfo.get_debate_info(debateName)

def get_debate_textfile_path(debateName):
    filename = dataSetInfo.get_textfile_name(debateName)
    datasetpath = dataLoader.get_path_for_dataset(debateName)
    path = str(datasetpath) + "/" + filename
    return path


#####################################################

# process data once loaded in
def processJSON(jSONObject, completeNodeSet):
    # convert JSON nodeset into dictionary
    nodeSet = json.loads(jSONObject)

    # append data from nodeset to collective set
    for node in nodeSet["nodes"]:
        completeNodeSet["dataNodes"].append(node)
    for edge in nodeSet["edges"]:
        completeNodeSet["edges"].append(edge)
    for locution in nodeSet["locutions"]:
        completeNodeSet["locutions"].append(locution)
    return completeNodeSet


def fetchOrganisedData(dataSetName):
    completeNodeSet = {
        "dataNodes": [],
        "edges": [],
        "locutions": [],
        "schemeNodes": [],
        "INodes": [],
        "LNodes": [],
        "other": []
    }

    nodeSets = dataLoader.loadData(dataSetName)
    for nodeSet in nodeSets:
        completeNodeSet = processJSON(nodeSet, completeNodeSet)

    # take all data nodes and split up further based on type of node
    for dataNode in completeNodeSet["dataNodes"]:
        # print(dataNode)
        if "scheme" in dataNode:
            completeNodeSet["schemeNodes"].append(dataNode)
        # inconsistencies in some of the datasets mean some of the nodes aren't annotated fully
        elif (dataNode["type"] == "RA") | (dataNode["type"] == "CA") | (dataNode["type"] == "TA") | (dataNode["type"] == "MA"):
            completeNodeSet["schemeNodes"].append(dataNode)
        elif dataNode["type"] == "I":
            completeNodeSet["INodes"].append(dataNode)
        elif dataNode["type"] == "L":
            completeNodeSet["LNodes"].append(dataNode)
        else:
            # this should be empty, if not there are inconsistencies in the dataset
            completeNodeSet["other"].append(dataNode)

    if len(completeNodeSet["other"]) > 0:
        print("Unidentified data nodes found.")

    # save as pandas dataframes
    # dataFrame = pd.DataFrame.from_dict(completeNodeSet)
    dataFrames = {
       "schemeNodes": pd.DataFrame(completeNodeSet["schemeNodes"]),
        "INodes": pd.DataFrame(completeNodeSet["INodes"]),
        "LNodes": pd.DataFrame(completeNodeSet["LNodes"]),
        "edges": pd.DataFrame(completeNodeSet["edges"]),
        "locutions": pd.DataFrame(completeNodeSet["locutions"])
    }
    return dataFrames
