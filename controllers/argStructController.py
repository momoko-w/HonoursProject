# script to find argument structures

struct_data = {
    "count_supporting": -1,
    "count_supported": -1,
    "count_conflicting": -1,
    "count_conflicted": -1,
    "count_linked": -1,
    "count_linked_arg": -1,
}


# count number of supporting nodes & linked argument constructs
def find_linked(dataframes):
    schemeNodes = dataframes["schemeNodes"]
    edges = dataframes["edges"]
    iNodes = dataframes["INodes"]

    support_counter = 0
    conflict_counter = 0
    linked_count = 0
    linked_arg_count = 0

    # get all scheme nodes that support
    supportSchemeNodeIDs = schemeNodes.query('type=="RA"')["nodeID"]

    for index, ID in supportSchemeNodeIDs.items():
        node_count = 0
        # find edges that are going to the scheme node
        matching = edges[edges["toID"] == ID]

        # make sure support is coming from an I-Node not a transition or locution
        for fromID in matching["fromID"]:
            # see if ID from which the support comes can be found in Inodes
            node_count += len(iNodes[iNodes["nodeID"] == fromID])

        # add up supporting nodes
        support_counter += node_count

        # if there's more than one INode found for one scheme node there is a linked structure
        if node_count > 1:
            linked_count += 1
            linked_arg_count += node_count

    # set number of supporting nodes found
    struct_data["count_support"] = support_counter

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
            node_count += len(iNodes[iNodes["nodeID"] == fromID])

        # add up countering nodes
        conflict_counter += node_count

        # if there's more than one INode found for one scheme node there is a linked structure
        if node_count > 1:
            linked_count += 1
            linked_arg_count += node_count

    # set number of countering nodes found
    struct_data["count_conflict"] = conflict_counter

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

    # get all scheme nodes that support
    supportSchemeNodeIDs = schemeNodes.query('type=="RA"')["nodeID"]
    # get all scheme nodes that attack
    conflictSchemeNodeIDs = schemeNodes.query('type=="CA"')["nodeID"]

    # for each Inode check incoming edges
    for ID in iNodes["nodeID"]:
        arg_count = 0
        # find edges that go to an Inode (incoming
        matching = edges[edges["toID"] == ID]
        # check whether incoming edges come from support/conflict scheme nodes
        for fromID in matching["fromID"]:
            # count nodes found
            support_match = supportSchemeNodeIDs.value_counts()
            if fromID in support_match:
                arg_count += support_match[fromID]

            conflict_match = conflictSchemeNodeIDs.value_counts()
            if fromID in conflict_match:
                arg_count += conflict_match[fromID]

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


def find_arg_struct(dataframes):
    find_linked(dataframes)
    find_convergent(dataframes)
    return struct_data






