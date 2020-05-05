# script to find argument structures

struct_data = {
    # counters & lists of I-Nodes for support/conflict
    "count_supporting": -1,
    "supporting_list": [],
    "count_supported": -1,
    "supported_list": [],
    "count_countering": -1,
    "countering_list": [],
    "count_countered": -1,
    "countered_list": [],

    # data on structures
    "count_linked": -1,
    "count_linked_arg": -1,
    "count_convergent": -1,
    "count_convergent_arg": -1,
    "count_single": -1,
}


# count number of supporting nodes & linked argument constructs
def find_linked(dataframes):
    schemeNodes = dataframes["schemeNodes"]
    edges = dataframes["edges"]
    iNodes = dataframes["INodes"]

    support_counter = 0
    supporting_list = []
    conflict_counter = 0
    countering_list = []
    linked_count = 0
    linked_arg_count = 0

    # get all scheme nodes that support
    supportSchemeNodeIDs = schemeNodes.query('type == "RA"')["nodeID"]

    for index, ID in supportSchemeNodeIDs.items():
        node_count = 0
        # find edges that are going to the scheme node
        matching = edges[edges["toID"] == ID]

        # make sure support is coming from an I-Node not a transition or locution
        for fromID in matching["fromID"]:
            # see if ID from which the support comes can be found in Inodes
            matched_Inodes = iNodes[iNodes["nodeID"] == fromID]
            node_count += len(matched_Inodes)
            supporting_list.extend(matched_Inodes["nodeID"].tolist())

        # add up supporting nodes
        support_counter += node_count

        # if there's more than one INode found for one scheme node there is a linked structure
        if node_count > 1:
            linked_count += 1
            linked_arg_count += node_count

    # set number of supporting nodes found
    struct_data["count_supporting"] = support_counter
    struct_data["supporting_list"] = supporting_list

    # count number of conflicting nodes & linked argument structures

    # get all scheme nodes that attack
    conflictSchemeNodeIDs = schemeNodes.query('type=="CA"')["nodeID"]

    for index, ID in conflictSchemeNodeIDs.items():
        node_count = 0
        # find edges coming into the scheme node
        matching = edges[edges["toID"] == ID]

        # make sure support is coming from an I-Node, not a transition or locution
        for fromID in matching["fromID"]:
            # see if ID from which the attack comes can be found in Inodes
            matched_Inodes = iNodes[iNodes["nodeID"] == fromID]
            node_count += len(matched_Inodes)
            countering_list.extend(matched_Inodes["nodeID"].tolist())

        # add up countering nodes
        conflict_counter += node_count

        # if there's more than one INode found for one scheme node there is a linked structure
        if node_count > 1:
            linked_count += 1
            linked_arg_count += node_count

    # set number of countering nodes found
    struct_data["count_countering"] = conflict_counter
    struct_data["countering_list"] = countering_list

    # set how many linked arg. structures found and how many arguments in those
    struct_data["count_linked"] = linked_count
    struct_data["count_linked_arg"] = linked_arg_count


# count convergent argument structures & single standalone arg.
def find_convergent(dataframes):
    # get dataframes needed
    schemeNodes = dataframes["schemeNodes"]
    edges = dataframes["edges"]
    iNodes = dataframes["INodes"]

    convergent_count = 0
    convergent_arg_count = 0
    single_count = 0
    supported = 0
    supported_list = []
    countered = 0
    countered_list = []

    # get all scheme nodes that support
    supportSchemeNodeIDs = schemeNodes.query('type=="RA"')["nodeID"]
    # get all scheme nodes that attack
    conflictSchemeNodeIDs = schemeNodes.query('type=="CA"')["nodeID"]

    # for each Inode check incoming edges
    for ID in iNodes["nodeID"]:
        arg_count = 0

        matching = edges[edges["toID"] == ID]
        # check whether incoming edges come from support/conflict scheme nodes
        for fromID in matching["fromID"]:
            # count nodes found
            support_match = supportSchemeNodeIDs.value_counts()
            if fromID in support_match:
                arg_count += support_match[fromID]
                supported += support_match[fromID]
                supported_list.append(ID)

            conflict_match = conflictSchemeNodeIDs.value_counts()
            if fromID in conflict_match:
                arg_count += conflict_match[fromID]
                countered += conflict_match[fromID]
                countered_list.append(ID)

        # if none found: check if single argument
        if arg_count == 0:
            outgoing = edges[edges["fromID"] == ID]
            if len(outgoing.index) == 0:
                single_count += 1

        # if more than one found: convergent argument structure
        if arg_count > 1:
            convergent_count += 1
            convergent_arg_count += arg_count

    struct_data["count_single"] = single_count
    struct_data["count_convergent"] = convergent_count
    struct_data["count_convergent_arg"] = convergent_arg_count

    struct_data["count_supported"] = supported
    struct_data["count_countered"] = countered
    struct_data["supported_list"] = supported_list
    struct_data["countered_list"] = countered_list


def calculate_avgs(debate_data):
    # percentages comparing to number of total argument units found
    struct_data["perc_supporting"] = round(
        struct_data["count_supporting"] / debate_data["count_arg_units"] * 100, 2)

    struct_data["perc_supported"] = round(
        struct_data["count_supported"] / debate_data["count_arg_units"] * 100, 2)

    struct_data["perc_countering"] = round(
        struct_data["count_countering"] / debate_data["count_arg_units"] * 100, 2)

    struct_data["perc_countered"] = round(
        struct_data["count_countered"] / debate_data["count_arg_units"] * 100, 2)

    struct_data["perc_single"] = round(
        struct_data["count_single"] / debate_data["count_arg_units"] * 100, 2)

    # arg structs avgs
    if struct_data["count_linked"] > 0:
        struct_data["avg_linked_arg"] = round(struct_data["count_linked_arg"] / struct_data["count_linked"], 2)
    else:
        struct_data["avg_linked_arg"] = 0

    if struct_data["count_convergent"] > 0:
        struct_data["avg_convergent_arg"] = round(
            struct_data["count_convergent_arg"] / struct_data["count_convergent"], 2)
    else:
        struct_data["avg_convergent_arg"] = 0

    # arg structs percentages
    struct_data["perc_linked_arg"] = round(
        struct_data["count_linked_arg"] / debate_data["count_arg_units"] * 100, 2)

    struct_data["perc_convergent_arg"] = round(
        struct_data["count_convergent_arg"] / debate_data["count_arg_units"] * 100, 2)

    # arg struct ratios
    struct_data["linked_ratio"] = round(debate_data["count_arg_units"] / struct_data["count_linked"], 2)
    struct_data["convergent_ratio"] = round(debate_data["count_arg_units"] / struct_data["count_convergent"], 2)


def find_arg_struct(dataframes, debate_data):
    # get linked structures and supporting/countering arguments
    find_linked(dataframes)
    # get convergent structures and supported/countered arguments
    find_convergent(dataframes)
    # get averages & percenatges
    calculate_avgs(debate_data)
    return struct_data






