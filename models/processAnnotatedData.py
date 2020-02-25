import json
from typing import List, Any
import loadAnnotatedData

def processJSON(jSONObject):
    fullNodeSet = json.loads(jSONObject)
    dataNodes = fullNodeSet["nodes"]
    edges = fullNodeSet["edges"]
    locutions = fullNodeSet["locutions"]

    schemeNodes: List[Any] =[]
    nonSchemeNodes: List[Any] = []
    for dataNode in dataNodes:
        if "scheme" in dataNode:
            schemeNodes.append(dataNode)
        else:
            nonSchemeNodes.append(dataNode)
        print(dataNode)
    #print(nonSchemeNodes)
