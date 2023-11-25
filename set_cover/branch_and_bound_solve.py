def is_valid_solution(solution, item_to_sets):
    """Check if the current solution satisfies all constraints."""
    for item, sets in item_to_sets.items():
        if not any(solution[set.index] for set in sets):
            return False
    return True


def calc_total_cost(candidate_set_dict, solution):
    total_cost = 0
    for index, selected in enumerate(solution):
        if selected:
            total_cost += candidate_set_dict[index].cost
    return total_cost


def cost_bound_solve(
        candidate_set_dict, item_to_sets,
        best_solution=None,
        solution=None, idx=0):

    if best_solution is None:
        best_solution = [1] * len(candidate_set_dict)
    if solution is None:
        solution = [0] * len(candidate_set_dict)

    my_cost = calc_total_cost(candidate_set_dict, solution)
    best_cost = calc_total_cost(candidate_set_dict, best_solution)

    if my_cost > best_cost:
        return

    # Base case: If all sets are considered
    if idx == len(candidate_set_dict):
        if is_valid_solution(solution, item_to_sets):
            my_cost = calc_total_cost(candidate_set_dict, solution)
            best_cost = calc_total_cost(candidate_set_dict, best_solution)
            # in-place change used to make object value change across functions
            best_solution[:] = \
                solution[:] if my_cost < best_cost else best_solution[:]
            return
        return

    # Try including the current set in the solution
    solution[idx] = 1
    cost_bound_solve(
        candidate_set_dict,
        item_to_sets,
        best_solution,
        solution.copy(),
        idx + 1
        )

    # Try excluding the current set from the solution and backtrack
    solution[idx] = 0
    cost_bound_solve(
        candidate_set_dict,
        item_to_sets,
        best_solution,
        solution.copy(),
        idx + 1)

    return best_solution


def item_bound_solve(
        candidate_set_dict,
        item_to_sets,
        best_solution=None,
        solution=None, item_idx=0, selected_items=None):
    if selected_items is None:
        selected_items = [0] * len(item_to_sets)
    if best_solution is None:
        best_solution = [1] * len(candidate_set_dict)
    if solution is None:
        solution = [0] * len(candidate_set_dict)

    # print(f'{item_idx}: {selected_items}')

    my_cost = calc_total_cost(candidate_set_dict, solution)
    best_cost = calc_total_cost(candidate_set_dict, best_solution)

    if my_cost >= best_cost:
        return

    if item_idx == len(item_to_sets):
        if my_cost < best_cost:
            best_solution[:] = solution[:]
        return

    if selected_items[item_idx] >= 1:
        return item_bound_solve(
            candidate_set_dict,
            item_to_sets,
            best_solution,
            solution,
            item_idx+1,
            selected_items.copy())
    for curr_set in item_to_sets[item_idx]:
        curr_solution = solution[:]
        curr_solution[curr_set.index] = 1
        curr_selected_items = selected_items[:]
        for curr_item in curr_set.items:
            curr_selected_items[curr_item] += 1
        item_bound_solve(
            candidate_set_dict,
            item_to_sets,
            best_solution,
            curr_solution,
            item_idx+1,
            curr_selected_items)

    return best_solution