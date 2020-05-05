from nltk.tokenize import sent_tokenize
from statistics import mean
import pathlib
import json

from controllers import dataController as dataCtrl, argStructController as argStructCtrl, speakersController as \
    speakersCtrl, scoreController as scoreCtrl

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
    # data on structures from other script
    # data on speakers comes from another script
    # score data
    "speaker_avg_score": -1,
    # contains all scores with IDs
    "speaker_scores": [],
    "score": -1,
}


def get_participants_list(debateName):
    # get file with participant names
    parent_dir = pathlib.Path(__file__).parent
    path = parent_dir.joinpath("models/participants.json").resolve()
    file = open(path.resolve(), "r")

    participants = json.loads(file.read())
    return participants[debateName]


def get_full_transcript(debateName):
    # load in main text file with full transcript and calculate values
    path = dataCtrl.get_debate_textfile_path(debateName)
    f = open(path, "r", encoding="utf8")
    debate_text = f.read()
    return debate_text


# load in main text file with full transcript and calculate values
def calculate_values_from_text(debateName):
    global debate_data

    debate_text = get_full_transcript(debateName)

    # get list of dialogue turns
    turns = debate_text.split("<br>")
    # calculate number of dialogue turns
    debate_data["count_turns"] = len(turns) - 1  # debate_text.count("<br>")

    # calculate average number of argument units per turn
    # have to get this rougher version of avg, since not all arg units are annotated with span tags
    avg = debate_data["count_arg_units"] / debate_data["count_turns"]
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
    debate_data["avg_arg_sent"] = round(debate_data["count_arg_units"] / debate_data["count_sentences"], 2)

    # arg_in_sent = []
    # for sentence in sents:
    #     arg_counter = 0
    #     if "<span" in sentence:
    #         arg_counter += sentence.count("<span")
    #     if arg_counter > 0:
    #         arg_in_sent.append(arg_counter)
    # debate_data["avg_arg_sent"] = round(mean(arg_in_sent), 2)


def calculate_frames_data(dataframes):
    iNodes = dataframes["INodes"]

    # count number of arg units in debate
    debate_data["count_arg_units"] = len(iNodes.index)


def get_result_standards():
    # read in context data file containing info on all existing debates
    parent_dir = pathlib.Path(__file__).parent
    path = parent_dir.joinpath("models/result_standards.json").resolve()
    file = open(path.resolve(), "r")
    standards = json.loads(file.read())
    return standards


# function to get all data needed for the tab elements
def calculate_tab_data(debateName):
    global debate_data

    # get full dataframes
    dataframes = dataCtrl.fetchOrganisedData(debateName)

    # calculate from dataframes
    calculate_frames_data(dataframes)

    # find argument structures
    struct_data = argStructCtrl.find_arg_struct(dataframes, debate_data)
    debate_data.update(struct_data)

    # calculate values from unannotated debate transcript text
    calculate_values_from_text(debateName)

    participants_dicts = get_participants_list(debateName)

    # calculate data on speakers
    speaker_data = speakersCtrl.get_speakers_data(dataframes, debate_data, participants_dicts)
    debate_data.update(speaker_data)

    standards = get_result_standards()
    speaker_debate_context = []

    # for each debate get data on speakers that has merged speakers with multiple IDs
    speaker_names = speakersCtrl.get_speaker_names(speaker_data, participants_dicts)
    speakers_list = speakersCtrl.get_speaker_data_wo_dupl(speaker_names, speaker_data, participants_dicts)

    # calculate speaker scores
    speaker_scores = scoreCtrl.calculate_speaker_scores(debate_data, standards, speakers_list, debateName)
    debate_data.update(speaker_scores)

    # calculate full score for debate
    debate_data["score"] = scoreCtrl.calculate_debate_score(debate_data, standards)

    return debate_data
