from models import dataSetInfo


def get_dataset_list():
    return dataSetInfo.get_dataSet_list()

def get_debate_names():
    return dataSetInfo.get_debate_names()

def get_no_of_debates():
    return len(get_dataset_list())

def get_debate_descriptions():
    return dataSetInfo.get_debate_descriptions()