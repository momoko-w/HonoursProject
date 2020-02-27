import json
import os

from models import dataSetInfo

def get_path_for_dataset(name):
    dataSetList = dataSetInfo.get_dataSet_list()
    for debate in dataSetList:
        if debate["name"] == name:
            return debate["nameAtPath"]

def loadData(dataSetName):
    allNodeSets = []
    pathName = get_path_for_dataset(dataSetName)
    dataSetPath = "../datasets/" + pathName
    # print(glob.glob("C:/Users/lilli/PycharmProjects/HonoursProject/datasets/MM2019Hypocrisy/*.json"))
    files = os.listdir(dataSetPath)

    #nodeset11410
    for filename in files:
        #change back to just .json later
        if filename.endswith("nodeset11397.json"):
            f = open(dataSetPath + "/" + filename, "r")
            nodeSet = f.read()
            allNodeSets.append(nodeSet)
    return allNodeSets
