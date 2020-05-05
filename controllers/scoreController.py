from statistics import mean

# calculate the percentage a value holds in a range from min to max
def get_percentage_in_range(value, min, max):
    if (max-min) == 0:
        return 100
    percentage = ((value-min)*100)/(max-min)
    return round(percentage, 2)


def get_strength_label(value, min, max, avg):
    # if a given value is lower than the average
    if value < avg:
        # get percentage in range between min & avg
        percentage = get_percentage_in_range(value, min, avg)
        if percentage < 50:
            return "low"
        else:
            return "low-medium"
    else:
        # else get percentage between avg & max
        percentage = get_percentage_in_range(value, avg, max)
        if percentage < 50:
            return "high-medium"
        else:
            return "high"

# discarded
def get_points_for_strength(strength, multiplier):
    if strength == "low":
        return 2.5*multiplier
    elif strength == "low-medium":
        return 5*multiplier
    elif strength == "medium-high":
        return 7.5*multiplier
    elif strength == "high":
        return 10*multiplier
    else:
        # something went wrong
        return 0


def get_adjusted_percentage(value, min, max, avg):
    # pretend that the avg value is the midpoint between min & max and adjust accordingly
    # if a given value is lower than the average
    if value < avg:
        # get percentage in range between min & avg
        percentage = get_percentage_in_range(value, min, avg)
        return round(percentage/2, 2)
    else:
        # else get percentage between avg & max
        percentage = get_percentage_in_range(value, avg, max)
        return round((percentage/2)+50, 2)


def get_points_for_percentage(percentage, multiplier):
    # divide percentage value by ten and apply the multiplier given
    return round((percentage/10)*multiplier, 2)


def calculate_speaker_scores(debate_data, standards, speakers_list, debateName):
    speaker_scores = {
        "speaker_avg_score": -1,
        # contains all scores with IDs
        "speaker_scores": []
    }
    debate_context = standards["debate_speaker_context"][debateName]
    for speaker in speakers_list:
        name = speaker["name"]
        score = 0
        # total arguments made - high
        temp = debate_context["total_arg"]
        percentage = get_adjusted_percentage(speaker["total_arg"], temp["min"], temp["max"], temp["avg"])
        score += get_points_for_percentage(percentage, 4)

        # supporting arguments made - high
        temp = debate_context["supporting"]
        if temp["max"] > 100:
            temp["max"] = 100
        supporting_perc = round(speaker["supporting"]/speaker["total_arg"]*100, 2)
        percentage = get_adjusted_percentage(supporting_perc, temp["min"], temp["max"], temp["avg"])
        score += get_points_for_percentage(percentage, 1.5)

        # supported arguments made - high
        temp = debate_context["supported"]
        if temp["max"] > 100:
            temp["max"] = 100
        supported_perc = round(speaker["supported"]/speaker["total_arg"]*100, 2)
        percentage = get_adjusted_percentage(supported_perc, temp["min"], temp["max"], temp["avg"])
        score += get_points_for_percentage(percentage, 1.5)

        # countering arguments made - high
        temp = debate_context["countering"]
        if temp["max"] > 100:
            temp["max"] = 100
        countering_perc = round(speaker["countering"]/speaker["total_arg"]*100, 2)
        percentage = get_adjusted_percentage(countering_perc, temp["min"], temp["max"], temp["avg"])
        score += get_points_for_percentage(percentage, 1.5)

        # countered arguments made - high NEGATIVE
        temp = debate_context["countered"]
        if temp["max"] > 100:
            temp["max"] = 100
        countered_perc = round(speaker["countered"]/speaker["total_arg"]*100, 2)
        percentage = get_adjusted_percentage(countered_perc, temp["min"], temp["max"], temp["avg"])
        score -= get_points_for_percentage(percentage, 1.5)

        if score < 0:
            score = 0
        speaker_scores["speaker_scores"].append({ "name" : name, "score": round(score, 2) })

    # calculate avg score
    speaker_scores["speaker_avg_score"] = round(
        mean([speaker['score'] for speaker in speaker_scores["speaker_scores"]]), 2)

    return speaker_scores


def calculate_debate_score(debate_data, standards):
    # calculate score
    score = 0
    # ARG. dENSITY
    # avg arg/turn
    temp = standards["avg_arg_turn"]
    percentage = get_adjusted_percentage(debate_data["avg_arg_turn"], temp["min"], temp["max"], temp["avg"])
    score += get_points_for_percentage(percentage, 1)

    # perc sent with arg
    temp = standards["count_sents_with_arg"]
    percentage = get_adjusted_percentage(debate_data["count_sents_with_arg"]/debate_data["count_sentences"]*100, temp["min"], temp["max"], temp["avg"])
    score += get_points_for_percentage(percentage, 0.5)

    # avg arg/SENT
    temp = standards["avg_arg_sent"]
    percentage = get_adjusted_percentage(debate_data["avg_arg_sent"], temp["min"], temp["max"], temp["avg"])
    score += get_points_for_percentage(percentage, 0.5)

    # SUPPORT & CONFLICT
    # % supporting
    temp = standards["supporting_arg"]
    percentage = get_adjusted_percentage(debate_data["perc_supporting"], temp["min"], temp["max"], temp["avg"])
    score += get_points_for_percentage(percentage, 0.5)

    # % supported
    temp = standards["supported_arg"]
    percentage = get_adjusted_percentage(debate_data["perc_supported"], temp["min"], temp["max"], temp["avg"])
    score += get_points_for_percentage(percentage, 0.5)

    # % countering
    temp = standards["countering_arg"]
    percentage = get_adjusted_percentage(debate_data["perc_countering"], temp["min"], temp["max"], temp["avg"])
    score += get_points_for_percentage(percentage, 0.5)

    # % countered
    temp = standards["countered_arg"]
    percentage = get_adjusted_percentage(debate_data["perc_countered"], temp["min"], temp["max"], temp["avg"])
    score += get_points_for_percentage(percentage, 0.5)

    # ARG STRUCT
    # Ratio Linked
    temp = standards["linked_ratio"]
    percentage = get_adjusted_percentage(debate_data["linked_ratio"], temp["min"], temp["max"], temp["avg"])
    score += get_points_for_percentage(percentage, 0.25)

    # Ratio Linked
    temp = standards["convergent_ratio"]
    percentage = get_adjusted_percentage(debate_data["convergent_ratio"], temp["min"], temp["max"], temp["avg"])
    score += get_points_for_percentage(percentage, 0.25)

    # % arg in linked
    temp = standards["perc_linked_arg"]
    percentage = get_adjusted_percentage(debate_data["perc_linked_arg"], temp["min"], temp["max"], temp["avg"])
    score += get_points_for_percentage(percentage, 0.75)

    # % arg in convergent
    temp = standards["perc_convergent_arg"]
    percentage = get_adjusted_percentage(debate_data["perc_convergent_arg"], temp["min"], temp["max"], temp["avg"])
    score += get_points_for_percentage(percentage, 1)

    # avg arg in linked
    temp = standards["avg_linked_arg"]
    percentage = get_adjusted_percentage(debate_data["avg_linked_arg"], temp["min"], temp["max"], temp["avg"])
    score += get_points_for_percentage(percentage, 0.75)

    # avg arg in convergent
    temp = standards["avg_convergent_arg"]
    percentage = get_adjusted_percentage(debate_data["avg_convergent_arg"], temp["min"], temp["max"], temp["avg"])
    score += get_points_for_percentage(percentage, 1)

    # AVG SPEAKER SCORE
    temp = standards["speaker_avg_score"]
    percentage = get_adjusted_percentage(debate_data["speaker_avg_score"], temp["min"], temp["max"], temp["avg"])
    score += get_points_for_percentage(percentage, 1)

    # return final score
    return round(score, 2)
