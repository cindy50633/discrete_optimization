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
