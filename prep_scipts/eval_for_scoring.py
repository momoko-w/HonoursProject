import timeit
import json
import pathlib
from statistics import mean
import copy


import mainController
from controllers import dataController, speakersController as speakersCtrl


def get_score_stdn():
    # get debate scores
    scores = []
    for data in tab_data:
        scores.append(data["score"])

    # set values
    standards["score"]["max"] = max(scores)
    standards["score"]["min"] = min(scores)
    standards["score"]["avg"] = round(mean(scores), 2)


def get_debate_stdn():
    turns = []
    sent_w_arg = [] # percentage
    avg_arg_in_sent = []
    supporting = []
    supported = []
    countering = []
    countered = []
    single = []
    linked_ratio = []
    convergent_ratio = []
    perc_linked_arg = []
    perc_convergent_arg = []
    avg_linked_arg = []
    avg_convergent_arg = []

    # for each debate extract values for specific property and save into separate lists
    for data in tab_data:
        turns.append(data["avg_arg_turn"])
        avg_arg_in_sent.append((data["avg_arg_sent"]))
        sent_w_arg.append(round(data["count_sents_with_arg"]/data["count_sentences"]*100, 2))
        # support/conflict
        supporting.append(data["perc_supporting"])
        supported.append(data["perc_supported"])
        countering.append(data["perc_countering"])
        countered.append(data["perc_countered"])
        single.append(data["perc_single"])
        # arg struct
        linked_ratio.append(data["linked_ratio"])
        convergent_ratio.append(data["convergent_ratio"])
        perc_linked_arg.append(data["perc_linked_arg"])
        perc_convergent_arg.append(data["perc_convergent_arg"])
        avg_linked_arg.append(data["avg_linked_arg"])
        avg_convergent_arg.append(data["avg_convergent_arg"])

    # from data compiled from all debates get min, max & avg value

    # general data
    standards["avg_arg_turn"]["min"] = min(turns)
    standards["avg_arg_turn"]["max"] = max(turns)
    standards["avg_arg_turn"]["avg"] = round(mean(turns), 2)

    standards["count_sents_with_arg"]["min"] = min(sent_w_arg)
    standards["count_sents_with_arg"]["max"] = max(sent_w_arg)
    standards["count_sents_with_arg"]["avg"] = round(mean(sent_w_arg), 2)

    standards["avg_arg_sent"]["min"] = min(avg_arg_in_sent)
    standards["avg_arg_sent"]["max"] = max(avg_arg_in_sent)
    standards["avg_arg_sent"]["avg"] = round(mean(avg_arg_in_sent), 2)

    # arg struct data
    standards["supporting_arg"]["min"] = min(supporting)
    standards["supporting_arg"]["max"] = max(supporting)
    standards["supporting_arg"]["avg"] = round(mean(supporting), 2)

    standards["supported_arg"]["min"] = min(supported)
    standards["supported_arg"]["max"] = max(supported)
    standards["supported_arg"]["avg"] = round(mean(supported), 2)

    standards["countering_arg"]["min"] = min(countering)
    standards["countering_arg"]["max"] = max(countering)
    standards["countering_arg"]["avg"] = round(mean(countering), 2)

    standards["countered_arg"]["min"] = min(countered)
    standards["countered_arg"]["max"] = max(countered)
    standards["countered_arg"]["avg"] = round(mean(countered), 2)

    standards["single_arg"]["min"] = min(single)
    standards["single_arg"]["max"] = max(single)
    standards["single_arg"]["avg"] = round(mean(single), 2)

    # arg struct
    standards["linked_ratio"]["min"] = min(linked_ratio)
    standards["linked_ratio"]["max"] = max(linked_ratio)
    standards["linked_ratio"]["avg"] = round(mean(linked_ratio), 2)

    standards["convergent_ratio"]["min"] = min(convergent_ratio)
    standards["convergent_ratio"]["max"] = max(convergent_ratio)
    standards["convergent_ratio"]["avg"] = round(mean(convergent_ratio), 2)

    standards["avg_linked_arg"]["min"] = min(avg_linked_arg)
    standards["avg_linked_arg"]["max"] = max(avg_linked_arg)
    standards["avg_linked_arg"]["avg"] = round(mean(avg_linked_arg), 2)

    standards["avg_convergent_arg"]["min"] = min(avg_convergent_arg)
    standards["avg_convergent_arg"]["max"] = max(avg_convergent_arg)
    standards["avg_convergent_arg"]["avg"] = round(mean(avg_convergent_arg), 2)

    standards["perc_linked_arg"]["min"] = min(perc_linked_arg)
    standards["perc_linked_arg"]["max"] = max(perc_linked_arg)
    standards["perc_linked_arg"]["avg"] = round(mean(perc_linked_arg), 2)

    standards["perc_convergent_arg"]["min"] = min(perc_convergent_arg)
    standards["perc_convergent_arg"]["max"] = max(perc_convergent_arg)
    standards["perc_convergent_arg"]["avg"] = round(mean(perc_convergent_arg), 2)


def get_speakers_stdn():
    avg_score = []
    avg_speaker_arg = []
    avg_speaker_supporting = []
    avg_speaker_supported = []
    avg_speaker_countering = []
    avg_speaker_countered = []
    speaker_debate_contexts = {}

    for i in range(len(tab_data)):
        data = tab_data[i]

        # set values & get vaues for speakers overview
        avg_score.append(data["speaker_avg_score"])
        avg_speaker_arg.append(data["speaker_avg_arg"])
        avg_speaker_supporting.append(data["speaker_avg_supporting"])
        avg_speaker_supported.append(data["speaker_avg_supported"])
        avg_speaker_countering.append(data["speaker_avg_countering"])
        avg_speaker_countered.append(data["speaker_avg_countered"])

        # for each debate get data on speakers that has merged speakers with multiple IDs
        participants = mainController.get_participants_list(debate_names[i])
        speaker_names = speakersCtrl.get_speaker_names(data, participants)
        speakers_list = speakersCtrl.get_speaker_data_wo_dupl(speaker_names, data, participants)

        scores = [speaker['score'] for speaker in speakers_list]
        total_args = [speaker['total_arg'] for speaker in speakers_list]
        supporting = [
            round(
                speaker['supporting'] / speaker['total_arg'] * 100, 2)
            for speaker in speakers_list
        ]

        supported = [
            round(
                speaker['supported'] / speaker['total_arg'] * 100, 2)
            for speaker in speakers_list
        ]

        countering = [
            round(
                speaker['countering'] / speaker['total_arg'] * 100, 2)
            for speaker in speakers_list
        ]

        countered = [
            round(
                speaker['countered'] / speaker['total_arg'] * 100, 2)
            for speaker in speakers_list
        ]

        # put together values in dict
        debate_context = {
            debate_names[i]: {
                "scores": {
                    "min": min(scores),
                    "max": max(scores),
                    "avg": round(mean(scores), 2)
                },
                "total_arg": {
                    "min": min(total_args),
                    "max": max(total_args),
                    "avg": round(mean(total_args), 2)
                },
                "supporting": {
                    "min": min(supporting),
                    "max": max(supporting),
                    "avg": round(mean(supporting), 2)
                },
                "supported": {
                    "min": min(supported),
                    "max": max(supported),
                    "avg": round(mean(supported), 2)
                },
                "countering": {
                    "min": min(countering),
                    "max": max(countering),
                    "avg": round(mean(countering), 2)
                },
                "countered": {
                    "min": min(countered),
                    "max": max(countered),
                    "avg": round(mean(countered), 2)
                }
            }
        }
        speaker_debate_contexts.update(debate_context)

    # from compiled data get values for standards
    standards["speaker_avg_score"]["min"] = min(avg_score)
    standards["speaker_avg_score"]["max"] = max(avg_score)
    standards["speaker_avg_score"]["avg"] = round(mean(avg_score), 2)

    standards["speaker_avg_arg"]["min"] = min(avg_speaker_arg)
    standards["speaker_avg_arg"]["max"] = max(avg_speaker_arg)
    standards["speaker_avg_arg"]["avg"] = round(mean(avg_speaker_arg), 2)

    standards["speaker_avg_supporting"]["min"] = min(avg_speaker_supporting)
    standards["speaker_avg_supporting"]["max"] = max(avg_speaker_supporting)
    standards["speaker_avg_supporting"]["avg"] = round(mean(avg_speaker_supporting), 2)

    standards["speaker_avg_supported"]["min"] = min(avg_speaker_supported)
    standards["speaker_avg_supported"]["max"] = max(avg_speaker_supported)
    standards["speaker_avg_supported"]["avg"] = round(mean(avg_speaker_supported), 2)

    standards["speaker_avg_countering"]["min"] = min(avg_speaker_countering)
    standards["speaker_avg_countering"]["max"] = max(avg_speaker_countering)
    standards["speaker_avg_countering"]["avg"] = round(mean(avg_speaker_countering), 2)

    standards["speaker_avg_countered"]["min"] = min(avg_speaker_countered)
    standards["speaker_avg_countered"]["max"] = max(avg_speaker_countered)
    standards["speaker_avg_countered"]["avg"] = round(mean(avg_speaker_countered), 2)

    standards["debate_speaker_context"] = speaker_debate_contexts


##################### MAIN ########################################################################

# run calculations for 5 debates to get averages, highest and lowest values to compare against
debate_names = ["Green Belt - Moral Maze", "Hypocrisy - Moral Maze", "Syria - Moral Maze",
                "Problem Families - Moral Maze", "Welfare State - Moral Maze"]

dataframes = []
for debate in debate_names:
    print("Getting data for " + debate)
    dataframes.append(dataController.fetchOrganisedData(debate))


# calculate tab data for each debate
tab_data = []
for i in range(len(debate_names)):
    print("Calculating data for " + debate_names[i])
    # deep copy needed because otherwise issues with how Python appends objects arises (always calls from same memory address
    debatedata = copy.deepcopy(mainController.calculate_tab_data(debate_names[i]))
    tab_data.append(debatedata)


standards = {
    "score": {
        "avg": 0,
        "min": 0,
        "max": 100
    },
    "avg_arg_turn": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "count_sents_with_arg": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "avg_arg_sent": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "supporting_arg": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "supported_arg": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "countered_arg": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "countering_arg": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "single_arg": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "linked_ratio": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "convergent_ratio": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "perc_linked_arg": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "perc_convergent_arg": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "avg_linked_arg": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "avg_convergent_arg": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "speaker_avg_score": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "speaker_avg_arg": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "speaker_avg_supporting": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "speaker_avg_supported": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "speaker_avg_countering": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "speaker_avg_countered": {
        "avg": 0,
        "min": 0,
        "max": 0
    },
    "debate_speaker_context": {}
}

# set standard values for debate
get_debate_stdn()
# set standard values for speakers dqtq
get_speakers_stdn()
get_score_stdn()

# get relative data directory
parent_dir = pathlib.Path(__file__).parent.parent
path = parent_dir.joinpath("models\\result_standards.json").resolve()
with open(path, 'w') as file:
    json.dump(standards, file)

