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

from collections import namedtuple

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


def solve_it(input_data):
    lines = input_data.split('\n')

    # item_count = int(lines[0].split()[0])
    candidate_set_dict = convert_to_candidate_set_dict(lines)

    solution = cost_first_second_length_greedy_solve(candidate_set_dict)
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
    #     print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/sc_6_1)')

    file_location = 'set_cover\\data\\sc_157_0'
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
    print(solve_it(input_data))
