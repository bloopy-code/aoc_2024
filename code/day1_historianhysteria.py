"""day 1"""
from collections import Counter
from useful_functions import input_data_read, rp

EXAMPLE = """
3   4
4   3
2   5
1   3
3   9
3   3
"""


@rp
def day1(puzzle_input: str):
    """Day 1 AOC Solution
    """
    # split
    puzzle_input = puzzle_input.split()

    # sort into two groups & sort
    l1 = list(map(int, puzzle_input[::2]))
    l2 = list(map(int, puzzle_input[1::2]))

    l1_sorted = sorted(l1)
    l2_sorted = sorted(l2)

    # differences
    diffs = sum(abs(x-y) for x, y in zip(l1_sorted, l2_sorted))

    # PART 2
    # counter of list 2
    l2_count = Counter(l2)

    sim_scores = sum(x*l2_count[x] for x in l1)

    return diffs, sim_scores


day1(input_data_read("../text_inputs/day_1.txt"))

# day1(EXAMPLE) # example input
