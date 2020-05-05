from statistics import mean
import operator, itertools
from operator import itemgetter

# set speaker data global
speaker_data = {
    "speaker_count_arg": {},
    "speaker_avg_arg": -1,
    "speaker_avg_supporting": -1,
    "speaker_avg_supported": -1,
    "speaker_avg_countering": -1,
    "speaker_avg_countered": -1,
    "speaker_supporting": {},
    "speaker_supported": {},
    "speaker_countering": {},
    "speaker_countered": {},
}


def test_get_all_speakerIDs(dataframes):
    # test function to get all speaker IDs to counter check
    locutions = dataframes["locutions"]
    speakerIDs = locutions["personID"].drop_duplicates()


def count_arg(dataframes, debate_data):
    # get relevant dataframes
    LNodes = dataframes["LNodes"]
    locutions = dataframes["locutions"]
    edges = dataframes["edges"]
    schemeNodes = dataframes["schemeNodes"]

    # set local var
    arg_count = {}
    supporting = {}
    supported = {}
    countering = {}
    countered = {}

    # get asserting YA nodes
    assertNodes = schemeNodes.query(
        'scheme=="Asserting" or scheme == "AssertiveQuestioning" or scheme == "PureQuestioning" or scheme == "RhetoricalQuestioning"')

    # get L-Nodes and check for the speakerID in locutions
    for ID in LNodes["nodeID"]:
        # get speaker ID for the LNode
        locution = locutions[locutions["nodeID"] == ID]
        speakerID = locution["personID"]

        if len(speakerID) >= 1:
            # get ID as string out of series
            speakerID = speakerID.max()

            # find edges coming from the LNode
            matching = edges[edges["fromID"] == ID]

            # for each outgoing edge, check if it goes to an asserting node
            for toID in matching["toID"]:
                matching_assert = assertNodes[assertNodes["nodeID"] == toID]["nodeID"].tolist()

                # count if matching found and add to counter
                if speakerID in arg_count:
                    arg_count[speakerID] += len(matching_assert)
                else:
                    arg_count[speakerID] = len(matching_assert)

                # get IDs for the INodes that the assertions etc. link to
                if len(matching_assert) == 1:
                    assertID = matching_assert[0]
                    edge_out = edges[edges["fromID"] == assertID]["toID"]
                    INodeID = edge_out.max()

                    # check if that INode is supporting & count
                    if INodeID in debate_data["supporting_list"]:
                        temp = debate_data["supporting_list"].count(INodeID)
                        if speakerID in supporting:
                            supporting[speakerID] += temp
                        else:
                            supporting[speakerID] = temp

                    # check if that INode is supported & count
                    if INodeID in debate_data["supported_list"]:
                        temp = debate_data["supported_list"].count(INodeID)
                        if speakerID in supported:
                            supported[speakerID] += temp
                        else:
                            supported[speakerID] = temp

                    # check if that INode is countering & count
                    if INodeID in debate_data["countering_list"]:
                        temp = debate_data["countering_list"].count(INodeID)
                        if speakerID in countering:
                            countering[speakerID] += temp
                        else:
                            countering[speakerID] = temp

                    # check if that INode is countered & count
                    if INodeID in debate_data["countered_list"]:
                        temp = debate_data["countered_list"].count(INodeID)
                        if speakerID in countered:
                            countered[speakerID] += temp
                        else:
                            countered[speakerID] = temp

    # set results in speaker_data
    speaker_data["speaker_count_arg"] = arg_count
    speaker_data["speaker_supporting"] = supporting
    speaker_data["speaker_supported"] = supported
    speaker_data["speaker_countering"] = countering
    speaker_data["speaker_countered"] = countered


def calculate_avgs(participants):
    # for each debate get data on speakers that has merged speakers with multiple IDs
    speaker_names = get_speaker_names(speaker_data, participants)
    speakers_list = get_speaker_data_wo_dupl(speaker_names, speaker_data, participants)


    # get average number of arguments made by speakers
    speaker_data["speaker_avg_arg"] = round(
        mean([speaker['total_arg'] for speaker in speakers_list]), 2)
    # speaker_data["speaker_count_arg"][key] for key in speaker_data["speaker_count_arg"]

    # get average number of supporting arguments made by speakers
    speaker_data["speaker_avg_supporting"] = round(
        mean([speaker['supporting'] for speaker in speakers_list]), 2)
    # speaker_data["speaker_supporting"][key] for key in speaker_data["speaker_supporting"]

    # get average number of supported arguments made by speakers
    speaker_data["speaker_avg_supported"] = round(
        mean([speaker['supported'] for speaker in speakers_list]), 2)
    # speaker_data["speaker_supported"][key] for key in speaker_data["speaker_supported"]

    # get average number of countering arguments made by speakers
    speaker_data["speaker_avg_countering"] = round(
        mean([speaker['countering'] for speaker in speakers_list]), 2)
    # speaker_data["speaker_countering"][key] for key in speaker_data["speaker_countering"]

    # get average number of countered arguments made by speakers
    speaker_data["speaker_avg_countered"] = round(
        mean([speaker['countered'] for speaker in speakers_list]))
    # speaker_data["speaker_countered"][key] for key in speaker_data["speaker_countered"]


def get_speakers_data(dataframes, debate_data, participants):
    # count number of arguments each speaker has made
    # check for each if they counter/countered/support/supported
    count_arg(dataframes, debate_data)

    # calculate averages for each counter
    calculate_avgs(participants)
    return speaker_data


def get_arg_table_graph_data(data, participants):
    output = {
        # set table list & column names
        "table_data": [["Name", "# of Arguments Made"]],
        # for graph data
        "x_values": [],
        "y_values": []
    }

    # list of speaker names and values: need to sum duplicate speakers' values
    to_sort = []

    for (speakerID, arg_count) in data["speaker_count_arg"].items():
        # per value get the speaker dict matching the speakerID
        speaker = [speaker for speaker in participants if speaker["id"] == speakerID]
        if len(speaker) > 0:
            to_sort.append({
                "arg_count": arg_count,
                "first_name": speaker[0]["first_name"],
                "last_name": speaker[0]["last_name"]
            })

    key = operator.itemgetter('first_name', 'last_name')
    final = [{'arg_count': sum(x['arg_count'] for x in g), 'first_name': k[0], 'last_name': k[1]} for k, g in
             itertools.groupby(sorted(to_sort, key=key), key=key)]

    # order data by highest # of arg made
    sorted_values = sorted(final, key=itemgetter('arg_count'), reverse=True)

    for item in sorted_values:
        full_name = item["first_name"] + " " + item["last_name"]
        # set table row for the speaker
        output["table_data"].append([full_name, item["arg_count"]])

        # set graph data for speaker
        output["x_values"].append(full_name)
        output["y_values"].append(item["arg_count"])

    return output


def get_pro_con_graph_data(data, participants, arg_type):
    output = {
        # set table list & column names
        "speaker_names": [],
        # for graph data
        "x_values": [],
        "y_values": []
    }

    # temp to remove duplicates in data
    to_sort = []

    # remove duplicates to get list of names and # of total arguments
    for (speakerID, arg_count) in data["speaker_count_arg"].items():
        # per value get the speaker dict matching the speakerID
        speaker = [speaker for speaker in participants if speaker["id"] == speakerID]
        if len(speaker) > 0:
            to_sort.append({
                "total_arg_count": arg_count,
                "first_name": speaker[0]["first_name"],
                "last_name": speaker[0]["last_name"]
            })

    key = operator.itemgetter('first_name', 'last_name')
    # sum up arg_count values where the name is the same
    no_dupl_total_arg = [{'total_arg_count': sum(x['total_arg_count'] for x in g),
                          'first_name': k[0], 'last_name': k[1]} for k, g
                         in itertools.groupby(sorted(to_sort, key=key), key=key)]

    # reset: temp to remove duplicates in data
    to_sort = []

    for (speakerID, arg_count) in data[arg_type].items():
        # per value get the speaker dict matching the speakerID
        speaker = [speaker for speaker in participants if speaker["id"] == speakerID]
        if len(speaker) > 0:
            to_sort.append({
                "arg_count": arg_count,
                "first_name": speaker[0]["first_name"],
                "last_name": speaker[0]["last_name"]
            })

    # sum together data for duplicate speakers
    key = operator.itemgetter('first_name', 'last_name')
    # sum up arg_count values where the name is the same
    no_dupl_arg = [{'arg_count': sum(x['arg_count'] for x in g), 'first_name': k[0], 'last_name': k[1]} for k, g in
                   itertools.groupby(sorted(to_sort, key=key), key=key)]

    # get total arguments per speaker for each saying the specific arg type (e.g. supporting)
    for speaker in no_dupl_arg:
        total_arg_match = [item["total_arg_count"] for item in no_dupl_total_arg
                           if item["first_name"] == speaker["first_name"]
                           and item["last_name"] == speaker["last_name"]]
        # add speaker name, total_arg and arg counts to final output lists
        if len(total_arg_match) > 0:
            output["speaker_names"].append(speaker["first_name"] + " " + speaker["last_name"])
            output["x_values"].append(speaker["arg_count"])
            output["y_values"].append(total_arg_match[0])

    return output


def get_speaker_names(data, participants):
    speakers = get_arg_table_graph_data(data, participants)
    names = speakers["x_values"]
    return names


# get ids for a speaker by name
def get_speaker_ids(name, participants):
    ids = []

    first_name = name.split(" ")[0]
    last_name = name.split(" ")[1]

    # get all ids where the name matches
    for speaker_dict in participants:
        if speaker_dict["first_name"] == first_name and speaker_dict["last_name"] == last_name:
            ids.append(speaker_dict["id"])

    return ids


def get_speaker_data_wo_dupl(speaker_names, data, participant_dicts):
    full_speaker_list = []

    # get data with duplicates removed
    speakers_arg_data = get_arg_table_graph_data(data, participant_dicts)
    speakers_supporting_data = get_pro_con_graph_data(data, participant_dicts, "speaker_supporting")
    speakers_supported_data = get_pro_con_graph_data(data, participant_dicts, "speaker_supported")
    speakers_countering_data = get_pro_con_graph_data(data, participant_dicts, "speaker_countering")
    speakers_countered_data = get_pro_con_graph_data(data, participant_dicts, "speaker_countered")

    # for each speaker, generate the contents
    for i in range(len(speaker_names)):
        # get name & number of total arguments made
        name = speakers_arg_data["x_values"][i]
        total_arg = speakers_arg_data["y_values"][i]

        # get score from data
        if "speaker_scores" in data:
            score = [speaker['score'] for speaker in data["speaker_scores"] if speaker["name"] == name][0]
        else:
            score = -1

        # check for name if supporting, ... arguments have been made and get number
        if name in speakers_supporting_data["speaker_names"]:
            index = speakers_supporting_data["speaker_names"].index(name)
            supporting = speakers_supporting_data["x_values"][index]
        else:
            supporting = 0

        if name in speakers_supported_data["speaker_names"]:
            index = speakers_supported_data["speaker_names"].index(name)
            supported = speakers_supported_data["x_values"][index]
        else:
            supported = 0

        if name in speakers_countering_data["speaker_names"]:
            index = speakers_countering_data["speaker_names"].index(name)
            countering = speakers_countering_data["x_values"][index]
        else:
            countering = 0

        if name in speakers_countered_data["speaker_names"]:
            index = speakers_countered_data["speaker_names"].index(name)
            countered = speakers_countered_data["x_values"][index]
        else:
            countered = 0

        speaker = {
            "name": name,
            "total_arg": total_arg,
            "score": score,
            "supporting": supporting,
            "supported": supported,
            "countering": countering,
            "countered": countered
        }
        full_speaker_list.append(speaker)

    return full_speaker_list