"""Day 5 - Print Queue"""
import itertools
import useful_functions

EXAMPLE: str = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

# read puzzle input
PUZZLE_INPUT: str = useful_functions.input_data_read("../text_inputs/day_5.txt")


@useful_functions.report_results
def day5(puzzle_input: str):
    """Day 5 Solution"""
    # split into rules and rows to check
    rule_input, row_input = puzzle_input.split("\n\n")
    rules_str: list[str] = rule_input.splitlines()
    rows_str: list[str] = row_input.splitlines()

    # parse rules into list
    rules: list[list[int]] = [list(map(int, x.split("|"))) for x in rules_str]

    # parse rows into list of ints
    rows: list[list[int]] = [list(map(int, x.split(","))) for x in rows_str]

    # create a rulebook of sorts with rule pairs
    all_numbers: set[int] = set(itertools.chain(*rows))

    # map rules to individual numbers. number: rules
    rulebook: dict = {}
    for number in all_numbers:
        rulebook[number] = [x for x in rules if x[0] == number]

    # initiate lists for passing in passed and failed rows
    pass_rows: list = []
    fail_rows: list = []

    def is_valid_row(row: list[int], return_error: bool = False) -> int | bool:
        """Check if an input row is valid, aka: obeys all rules"""
        valid: bool = True

        for value in row:
            for rule in rulebook[value]:
                # check the rule pair is in the row
                if set(rule).issubset(set(row)):
                    if row.index(value) > row.index(rule[1]):
                        valid = False
                        # for part 2 - return index of where rules fail
                        if return_error:
                            return row.index(value)
                        break
            if not valid:
                break

        return valid

    # check rows are valid (pass) or not (fail)
    for row in rows:
        if is_valid_row(row):
            # if row obeys all its rules
            pass_rows.append(row)
        else:
            # if row fails rules
            fail_rows.append(row)

    # this could be improved. come back to this part.
    def get_middle_value(row: list[int]):
        """Get middle value for each row"""
        result: int = 0
        if len(row) % 2 != 0:
            result += row[len(row) // 2]
        else:
            result += row[(len(row) // 2) - 1]
        return result

    # get middle value sum for part 1, all passed rows.
    part_1_result: int = sum(get_middle_value(x) for x in pass_rows)

    # --- PART 2 ---

    # initiate empty list to store reordered, obedient rows
    reordered_rows = []

    # check through failed rows and get back index
    # swap failed index with one before it, add row back to list to check
    # eventually it will be compliant and exit the loop
    # --- this part is a little slow... ---
    for row in fail_rows:
        if isinstance(is_valid_row(row, return_error=True), bool) is False:
            error_index: int = is_valid_row(row, return_error=True)
            row[error_index - 1], row[error_index] = (
                row[error_index],
                row[error_index - 1],
            )
            fail_rows.append(row)  # a bit fudgey but it gets the job done
        else:
            reordered_rows.append(row)

    # part 2 middle value
    part_2_result: int = sum(get_middle_value(x) for x in reordered_rows)

    return part_1_result, part_2_result


# example input
day5(EXAMPLE)

# actual input
day5(PUZZLE_INPUT)
