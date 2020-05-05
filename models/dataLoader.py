import os
import pathlib

from models import dataSetInfo


def get_path_for_dataset(name):
    dataSetList = dataSetInfo.get_dataSets_list()
    for debate in dataSetList:
        if debate["name"] == name:
            # get relative data directory
            dir = pathlib.Path(__file__).parent.parent
            path = dir.joinpath("datasets\\"+debate["nameAtPath"]).resolve()
            return path


def loadData(dataSetName):
    allNodeSets = []
    dataSetPath = get_path_for_dataset(dataSetName)
    # all files in directory
    files = os.listdir(dataSetPath)

    # check fi files are nodeset files
    for filename in files:
        if filename.endswith("json"):
            f = open(str(dataSetPath) + "/" + filename, "r")
            nodeSet = f.read()
            allNodeSets.append(nodeSet)
    return allNodeSets
