"""Day 7 - Bridge Repair"""
import itertools
from rich.progress import track
import useful_functions

EXAMPLE_INPUT = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip()

# Custom type
OpCombo = list[list[tuple[str, int] | tuple[int, ...]]]

PUZZLE_INPUT: str = useful_functions.input_data_read("../text_inputs/day_7.txt")
_puzzle_data: list[str] = EXAMPLE_INPUT.splitlines()  # Example puzzle data
puzzle_data: list[str] = PUZZLE_INPUT.splitlines()


@useful_functions.report_results
def day_7(puzzle_input: list[str]) -> tuple[int, int]:
    """Day 7 - Bridge Repair Part 1 & 2"""

    # Helper functions.
    def parse_calibrations(puzzle: list[str]) -> list[dict]:
        """Parse input data to list of calibration value: operators maps"""
        calibrations: list[dict] = []
        for row in puzzle:
            value, operators = row.split(":")
            calibrations.append(
                {"value": int(value), "operations": list(map(int, operators.split()))}
            )
        return calibrations

    def operation_combinations(
        operators: list[int], symbols: tuple[str, ...] = ("+", "*", "||")
    ) -> OpCombo:
        """Generate all operator combinations paired with numbers"""
        op_combos = list(itertools.product(symbols, repeat=len(operators) - 1))
        return [
            [tuple([operators[0]])] + list(zip(operator, operators[1:]))
            for operator in op_combos
        ]

    def evaluate(operator_combo: list) -> int:
        """Evaluate operators and numbers"""
        result, the_rest = int(operator_combo[0][0]), operator_combo[1:]

        # Operator functions.
        operator_functions = {"+": int.__add__, "*": int.__mul__}

        for operator, number in the_rest:
            if operator == "||":
                result = int(f"{result}{number}")  # Concatenate two numbers
            else:
                result = operator_functions[operator](result, number)
        return result

    # Place to store results.
    part_1_values, part_2_values = [], []

    # Create value: operators map.
    calibration_map: list[dict] = parse_calibrations(puzzle_input)

    track_msg = "Repairing Bridges..."
    for value_operator in track(calibration_map, description=track_msg):
        # Store True/False depending on if evaluation matches expected value.
        temp_part_1_result = False
        temp_part_2_result = False

        all_symbol_combos: OpCombo = operation_combinations(
            value_operator["operations"]
        )

        for op_combo in all_symbol_combos:
            result = evaluate(op_combo)
            if result == value_operator["value"]:
                if "||" in "".join(map(str, op_combo)):
                    temp_part_2_result = True
                else:
                    temp_part_1_result = True
                break  # Stop checking once found 1 True.

        # If any True in temp results - aka; result == expected value
        # add to main list.
        if temp_part_1_result:
            part_1_values.append(value_operator["value"])
        elif temp_part_2_result:
            part_2_values.append(value_operator["value"])

    return sum(part_1_values), sum(part_2_values + part_1_values)


if __name__ == "__main__":
    print("*** DAY 7 - BRIDGE REPAIR ***")
    day_7(puzzle_data)
