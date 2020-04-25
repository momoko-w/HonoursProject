from models import dataLoader
import os

dataSetPath = dataLoader.get_path_for_dataset("Green Belt - Moral Maze")
files = os.listdir(dataSetPath)

for filename in files:
    if filename.endswith("nodeset11399.json"):
        f = open(str(dataSetPath) + "/" + filename, "r")
        nodeSet = f.read()

