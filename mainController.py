import nltk
from nltk.tokenize import sent_tokenize
from statistics import mean

from controllers import dataController as dataCtrl, argStructController as argStructCtrl



# global var containing all values needed to populate the tab elements in the UI
debate_data = {
    # overview data
    "count_arg_units": -1,
    # data on NL text from full transcript
    "count_turns": -1,
    "avg_arg_turn": 0.0,
    "count_sentences": -1,
    "count_sents_with_arg": -1,
    "avg_arg_sent": 0.0,
    # supporting nodes
    "count_support": -1,
    # attacking nodes
    "count_conflict": -1,
    # linked argument structure + no. of arg in them
    "count_linked": -1,
    "count_linked_arg": -1,
    # convergent structure + no. of arg. in them
    "count_convergent": -1,
    "count_convergent_arg": -1,
    # single standalone arguments (not connected)
    "count_single": -1,
    # score data
    "score": -1,
}


def calculate_values_from_text(debateName):
    global debate_data
    # load in main text file with full transcript and calculate values
    path = dataCtrl.get_debate_textfile_path(debateName)
    f = open(path, "r", encoding="utf8")
    debate_text = f.read()

    # get list of dialogue turns
    turns = debate_text.split("<br>")
    # calculate number of dialogue turns
    debate_data["count_turns"] = len(turns)-1 # debate_text.count("<br>")

    # calculate average number of argument units per turn
    # have to get this rougher version of avg, since not all arg units are annotated with span tags
    avg = debate_data["count_arg_units"]/debate_data["count_turns"]
    debate_data["avg_arg_turn"] = round(avg, 2)

    # arg_in_turn = []
    # for turn in turns:
    #     arg_turn_counter = 0
    #     if "<span" in turn:
    #         arg_turn_counter += turn.count("<span")
    #     if arg_turn_counter > 0:
    #         arg_in_turn.append(arg_turn_counter)
    # debate_data["avg_arg_turn"] = round(mean(arg_in_turn), 2)


    # split text into transcript into sentences
    sents = sent_tokenize(debate_text)
    # calculate number of sentences
    debate_data["count_sentences"] = len(sents)

    # count number of sentences with argument units in them
    arg_sent_counter = 0
    for sentence in sents:
        if "<span" in sentence:
            arg_sent_counter += 1
    debate_data["count_sents_with_arg"] = arg_sent_counter

    # calculate average number of argument units per sentence
    # have to get this rougher version of avg, since not all arg units are annotated with span tags
    debate_data["avg_arg_sent"] = round(debate_data["count_arg_units"]/debate_data["count_sentences"], 2)

    # arg_in_sent = []
    # for sentence in sents:
    #     arg_counter = 0
    #     if "<span" in sentence:
    #         arg_counter += sentence.count("<span")
    #     if arg_counter > 0:
    #         arg_in_sent.append(arg_counter)
    # debate_data["avg_arg_sent"] = round(mean(arg_in_sent), 2)


def calculate_debate_data(dataframes):
    iNodes = dataframes["INodes"]

    # count number of arg units in debate
    debate_data["count_arg_units"] = len(iNodes.index)


def calculate_debate_score():
    debate_data["score"] = 90


# function to get all data needed for the tab elements
def calculate_tab_data(debateName, dataframes):
    global debate_data
    # calculate from dataframes
    calculate_debate_data(dataframes)
    # find argument structures
    struct_data = argStructCtrl.find_arg_struct(dataframes)
    debate_data.update(struct_data)
    # calculate values from unannotated debate transcript text
    calculate_values_from_text(debateName)

    calculate_debate_score()
    return debate_data
