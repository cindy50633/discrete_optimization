from my_type import MySet


def cost_coverage_ratio_greedy_solve(candidate_set_dict, item_count):
    """
    Solve greedy by using the ratio cost/len_of_cover_region.
    """
    solution = [0] * len(candidate_set_dict)
    covered = set()

    cost_region_ratio_dict = {}
    for s in candidate_set_dict.values():
        cost_region_ratio_dict[s.index] = s.cost / len(s.items)

    asc_cost_region_ratio_dict = \
        dict(sorted(cost_region_ratio_dict.items(),
                    key=lambda item: item[1], reverse=False))
    for index, _ in asc_cost_region_ratio_dict.items():
        solution[index] = 1
        curr_set = candidate_set_dict[index]
        covered = covered.union(curr_set.items)
        if len(covered) >= item_count:
            break
    return solution


def cost_first_second_length_greedy_solve(candidate_set_dict):
    solution = [0] * len(candidate_set_dict)
    covered = set()

    cost_to_set_dict = {}
    for _, my_set in candidate_set_dict.items():
        if my_set.cost in cost_to_set_dict:
            cost_to_set_dict[my_set.cost].append(my_set)
        else:
            cost_to_set_dict[my_set.cost] = [my_set]
    asc_cost_to_set_info_dict = dict(
        sorted(cost_to_set_dict.items(), key=lambda item: item[0]))

    # sort value of asc_cost_to_set_info_dict by items length
    for _, my_set_list in asc_cost_to_set_info_dict.items():
        my_set_list.sort(key=lambda my_set: -len(my_set.items))

    # print(asc_cost_to_set_info_dict)

    for _, my_set_list in asc_cost_to_set_info_dict.items():
        for my_set in my_set_list:
            for item in my_set.items:
                if item not in covered:
                    solution[my_set.index] = 1
                    covered = covered.union(my_set.items)
    return solution


def make_item_to_included_set_dict(
        item_count, candidate_set_dict: dict[int, MySet]):
    item_to_included_set_dict = {}
    # initialize dict with key as item_index in asc order
    for item_index in range(item_count):
        item_to_included_set_dict[item_index] = []

    for curr_set in candidate_set_dict.values():
        for item_index in curr_set.items:
            item_to_included_set_dict[item_index].append(curr_set)
    return item_to_included_set_dict


def included_set_cost_first_solve(
        item_count, candidate_set_dict: dict[int, MySet]):
    item_to_included_set_dict = \
        make_item_to_included_set_dict(item_count, candidate_set_dict)
    solution = [0] * len(candidate_set_dict)
    item_selected_list = [0] * item_count

    for i in range(item_count):
        if item_selected_list[i] == 1:
            continue
        candidate_sets = item_to_included_set_dict[i]
        selected_set = sorted(
            candidate_sets,
            key=lambda set: (set.cost, -len(set.items)))[0]
        solution[selected_set.index] = 1
        for item in selected_set.items:
            item_selected_list[item] = 1
    return solution
