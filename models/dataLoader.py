import json
import os
import pathlib

from models import dataSetInfo



def get_path_for_dataset(name):
    dataSetList = dataSetInfo.get_dataSets_list()
    for debate in dataSetList:
        if debate["name"] == name:
            # get relative data directory
            PATH = pathlib.Path(__file__).parent.parent
            DATA_PATH = PATH.joinpath("datasets\\"+debate["nameAtPath"]).resolve()
            return DATA_PATH


def loadData(dataSetName):
    allNodeSets = []
    dataSetPath = get_path_for_dataset(dataSetName)

    files = os.listdir(dataSetPath)

    for filename in files:
        if filename.endswith("nodeset11399.json"):
            f = open(str(dataSetPath) + "/" + filename, "r")
            nodeSet = f.read()
            allNodeSets.append(nodeSet)
    return allNodeSets
