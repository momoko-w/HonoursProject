import json
import os
import processAnnotatedData

def loadData():
    dataSetName = "MoralMazeGreenBelt"
    dataSetPath = "datasets/" + dataSetName
    # print(glob.glob("C:/Users/lilli/PycharmProjects/HonoursProject/datasets/MM2019Hypocrisy/*.json"))
    files = os.listdir(dataSetPath)

    #nodeset11410
    for filename in files:
        if filename.endswith("nodeset11397.json"):
            f = open(dataSetPath+"/"+filename, "r")
            nodeSet = f.read()
            processAnnotatedData.processJSON(nodeSet)
            print("")

loadData()