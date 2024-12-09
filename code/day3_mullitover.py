"""day 3 aoc - mull it over"""
import re
from useful_functions import report_results, input_data_read

EXAMPLE = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
EXAMPLE2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


@report_results
def day3(puzzle_input: str):
    """Day 3 AoC Solution - Mull It Over"""
    # regex to extract correct mul values

    def regex_find_and_sum(instructions):
        """Find relevant instructions and multiply/sum"""
        # ol' regex
        match_regex = r"mul\((\d{1,3}),(\d{1,3})\)"

        # apply regex over input
        matches = re.findall(match_regex, instructions)

        # map str results to int then multiply, then sum all
        results = sum(x[0] * x[1] for x in [list(map(int, match)) for match in matches])

        return results

    # PART 1
    part1 = regex_find_and_sum(puzzle_input)

    # PART 2
    # split & rejoin on 'do', remove any sections starting with n't (don't)
    new_instructions = "".join(
        [puzzle for puzzle in puzzle_input.split("do") if not puzzle.startswith("n't")]
    )

    part2 = regex_find_and_sum(new_instructions)

    return part1, part2


# run on example input
day3(EXAMPLE2)

# run on actual input
day3(input_data_read("../text_inputs/day_3.txt"))
