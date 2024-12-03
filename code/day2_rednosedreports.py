"""day 2 aoc"""
from itertools import combinations
from functools import reduce
from useful_functions import rp, input_data_read

EXAMPLE = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


@rp
def day2(puzzle_input: str):
    """AoC Day 2 - Red Nosed Reports"""
    # turn input into lists of ints
    reports = [
        list(map(int, x.split())) for x in puzzle_input
    ]  # add .splitlines() for example input

    def check_ascending_descending(report: list[int]):
        """check a report is entirely ascending or
        descending.

        Args:
            report (list[int]): line from puzzle input
        """
        return (
            report
            if report == sorted(report) or report == sorted(report, reverse=True)
            else None
        )

    def get_differences(report: list[int]):
        """get differences between each item in report

        Args:
            report (list[int]): line from puzzle input
        """
        return [abs(report[i] - report[i + 1]) for i in range(len(report) - 1)]

    def safe_reports(report: list[int]):
        """figure out if 0 or num above 3 is in report
        if so, return None.

        Args:
            report (list[int]): line from puzzle input
        """
        return report if not any(i == 0 or i > 3 for i in report) else None

    # create a pipeline function
    def safe_report_pipeline(report: list[int]):
        """Pipeline a few other functions together.

        Args:
            report (list[int]): line from puzzle input
        """
        return reduce(
            lambda r, f: f(r) if r is not None else None,
            [check_ascending_descending, get_differences, safe_reports],
            report,
        )

    # PART 1
    part_1 = sum(1 for report in reports if safe_report_pipeline(report) is not None)

    # PART 2
    # create combos with one item removed
    def create_combos(report: list[int]):
        """get all the combos of removing 1 item from report"""
        return [list(combo) for combo in combinations(report, len(report) - 1)]

    # create combos - then go through each combo pipeline
    part_2 = 0
    for report in reports:
        combo_reports = create_combos(report)
        part_2 += (
            1 if any(safe_report_pipeline(r) is not None for r in combo_reports) else 0
        )

    return part_1, part_2


# day2(EXAMPLE)  # test input
day2(input_data_read("../text_inputs/day_2.txt"))
