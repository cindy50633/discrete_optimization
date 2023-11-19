#!/usr/bin/python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Carleton Coffrin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# import sys
# from greedy_solve import cost_first_second_length_greedy_solve
from collections import namedtuple, defaultdict

MySet = namedtuple("MySet", ['index', 'cost', 'items'])


def convert_to_candidate_set_dict(lines):
    # first line structure:
    # number_of_item number_of_set
    set_count = int(lines[0].split()[1])

    set_dict: dict[int, MySet] = {}
    for i in range(1, set_count+1):
        parts = lines[i].split()
        curr_index = i - 1
        set_dict[curr_index] = \
            MySet(
                curr_index,
                float(parts[0]),
                sorted([int(i) for i in parts[1:]])
            )
    return set_dict


def remove_duplicate_solution(solution, candidate_set_dict):
    item_occurance_count_dict = defaultdict(int)
    for i, selected in enumerate(solution):
        if selected:
            my_set = candidate_set_dict[i]
            for item in my_set.items:
                item_occurance_count_dict[item] += 1

    removable_index_candidates = []
    for i, selected in enumerate(solution):
        if selected:
            my_set = candidate_set_dict[i]
            has_one = False
            for item in my_set.items:
                if item_occurance_count_dict[item] == 1:
                    has_one = True
                    break
            if not has_one:
                removable_index_candidates.append((i))

    removable_index_candidates.sort(
        key=lambda i: (
            candidate_set_dict[i].cost, -len(candidate_set_dict[i].items)))

    while len(removable_index_candidates):
        target_index = removable_index_candidates.pop()
        target_set = candidate_set_dict[target_index]

        is_removable = True
        for item in target_set.items:
            if item_occurance_count_dict[item] == 1:
                is_removable = False
                break
        if is_removable:
            solution[target_index] = 0
            for item in target_set.items:
                item_occurance_count_dict[item] -= 1


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


def dummy_cp_solve(item_to_included_set_dict, candidate_set_dict):
    item_count = len(item_to_included_set_dict)
    solution = [0] * len(candidate_set_dict)
    item_selected_list = [0] * item_count

    for i in range(item_count):
        if item_selected_list[i] == 1:
            continue
        candidate_sets: list[MySet] = item_to_included_set_dict[i]
        selected_set = sorted(
            candidate_sets,
            key=lambda set: (set.cost, -len(set.items)))[0]
        solution[selected_set.index] = 1
        for item in selected_set.items:
            item_selected_list[item] = 1
    return solution


def solve_it(input_data):
    lines = input_data.split('\n')

    item_count = int(lines[0].split()[0])
    candidate_set_dict = convert_to_candidate_set_dict(lines)

    # solution = cost_first_second_length_greedy_solve(candidate_set_dict)
    # remove_duplicate_solution(solution, candidate_set_dict)

    item_to_included_set_dict = make_item_to_included_set_dict(
        item_count, candidate_set_dict)
    solution = dummy_cp_solve(item_to_included_set_dict, candidate_set_dict)
    remove_duplicate_solution(solution, candidate_set_dict)

    # solution = cost_coverage_ratio_greedy_solve(
    #     candidate_set_dict, item_count)

    # calculate the cost of the solution
    obj = sum([s.cost*solution[s.index] for s in candidate_set_dict.values()])

    # prepare the solution in the specified output format
    output_data = str(obj) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     file_location = sys.argv[1].strip()
    #     with open(file_location, 'r') as input_data_file:
    #         input_data = input_data_file.read()
    #     print(solve_it(input_data))
    # else:
    #     print('This test requires an input file.')

    file_location = 'set_cover\\data\\sc_4000_8'
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
    print(solve_it(input_data))
