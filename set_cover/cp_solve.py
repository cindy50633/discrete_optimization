def is_valid_solution(solution, item_to_included_set_dict):
    """Check if the current solution satisfies all constraints."""
    for item, sets in item_to_included_set_dict.items():
        if not any(solution[set.index] for set in sets):
            return False
    return True


def calc_total_cost(candidate_set_dict, solution):
    total_cost = 0
    for index, selected in enumerate(solution):
        if selected:
            total_cost += candidate_set_dict[index].cost
    return total_cost


def dummy_cp_solve(
        candidate_set_dict, item_to_included_set_dict, solution=None, idx=0):
    if solution is None:
        solution = [0] * len(candidate_set_dict)

    # Base case: If all sets are considered
    if idx == len(candidate_set_dict):
        if is_valid_solution(solution, item_to_included_set_dict):
            print(calc_total_cost(candidate_set_dict, solution))
            print(solution)
            return solution
        return None

    # Try including the current set in the solution
    solution[idx] = 1
    dummy_cp_solve(
        candidate_set_dict,
        item_to_included_set_dict,
        solution.copy(),
        idx + 1)

    # Try excluding the current set from the solution and backtrack
    solution[idx] = 0
    dummy_cp_solve(
        candidate_set_dict,
        item_to_included_set_dict,
        solution.copy(),
        idx + 1)
