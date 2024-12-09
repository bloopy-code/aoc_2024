"""day 1"""
from collections import Counter
from useful_functions import input_data_read, report_results

EXAMPLE = """
3   4
4   3
2   5
1   3
3   9
3   3
"""


@report_results
def day1(puzzle_input: str):
    """Day 1 AOC Solution"""
    # split
    puzzleinput: list[str] = puzzle_input.split()

    # sort into two groups & sort
    l1: list[int] = list(map(int, puzzleinput[::2]))
    l2: list[int] = list(map(int, puzzleinput[1::2]))

    l1_sorted = sorted(l1)
    l2_sorted = sorted(l2)

    # differences
    diffs = sum(abs(x - y) for x, y in zip(l1_sorted, l2_sorted))

    # one liner for day 1 :)
    _day1_s1_oneliner = sum(  # noqa: F841
        abs(x - y)
        for x, y in zip(
            sorted(list(map(int, puzzle_input.split()[::2]))),
            sorted(list(map(int, puzzle_input.split()[1::2]))),
        )
    )

    # PART 2
    # counter of list 2
    l2_count = Counter(l2)

    sim_scores = sum(x * l2_count[x] for x in l1)

    # one liner for day 2 - verified - works! :)
    _day1_s2_oneliner = sum(  # noqa: F841
        x * Counter(list(map(int, puzzle_input.split()[1::2])))[x]
        for x in list(map(int, puzzle_input.split()[::2]))
    )

    return diffs, sim_scores


day1(input_data_read("../text_inputs/day_1.txt"))

# day1(EXAMPLE) # example input here
