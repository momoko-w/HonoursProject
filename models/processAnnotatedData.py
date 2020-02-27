import json
from typing import List, Any
from models import loadAnnotatedData

def processJSON(jSONObject, completeNodeSet):
    #convert JSON nodeset into dictionary
    nodeSet = json.loads(jSONObject)

    #append data from nodeset to collective set
    completeNodeSet["dataNodes"].append(nodeSet["nodes"])
    completeNodeSet["edges"].append(nodeSet["edges"])
    completeNodeSet["locutions"].append(nodeSet["locutions"])

    # schemeNodes: List[Any] =[]
    # nonSchemeNodes: List[Any] = []
    # for dataNode in dataNodes:
    #     if "scheme" in dataNode:
    #         schemeNodes.append(dataNode)
    #     else:
    #         nonSchemeNodes.append(dataNode)

    return completeNodeSet

def fetchOrganisedData(dataSetName):
    completeNodeSet = {
        "dataNodes" : [],
        "edges" : [],
        "locutions" : []
    }

    nodeSets = loadAnnotatedData.loadData(dataSetName)
    for nodeSet in nodeSets:
        completeNodeSet = processJSON(nodeSet, completeNodeSet)

    return completeNodeSet