import json
import os
import processAnnotatedData


def getPathForDataset(name):
    file = open("list_of_datasets.json")
    dataSetList = file.read()
    dataSetList = json.loads(dataSetList)
    for debate in dataSetList:
        if debate["name"] == name:
            return debate["nameAtPath"]

def loadData(dataSetName):
    allNodeSets = []
    pathName = getPathForDataset(dataSetName)
    dataSetPath = "datasets/" + pathName
    # print(glob.glob("C:/Users/lilli/PycharmProjects/HonoursProject/datasets/MM2019Hypocrisy/*.json"))
    files = os.listdir(dataSetPath)

    #nodeset11410
    for filename in files:
        #change back to just .json
        if filename.endswith("nodeset11397.json"):
            f = open(dataSetPath+"/"+filename, "r")
            nodeSet = f.read()
            allNodeSets.append(nodeSet)
    return allNodeSets
