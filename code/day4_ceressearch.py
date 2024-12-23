"""Day 4 - Ceres Search"""
import re
import useful_functions

# set some types
ListListStr = list[list[str]]
Blah = dict[int, list[tuple[int, int]]]

EXAMPLE: str = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

PUZZLE_INPUT = useful_functions.input_data_read("../text_inputs/day_4.txt")


@useful_functions.report_results
def day4(puzzle_input: str) -> tuple[int, int]:
    """Day 4 'solution'"""
    # split puzzle input into horizontal and vertical lines
    horizontal_lines: ListListStr = [list(x) for x in puzzle_input.splitlines()]
    vertical_lines: ListListStr = [list(x) for x in zip(*horizontal_lines)]

    # get half of the diagonal coordinates from 0,0
    def get_diagonal_coordinates(
        input_lines: ListListStr,
    ) -> dict[int, list[tuple[int, int]]]:
        coordinates: dict[int, list[tuple[int, int]]] = {}
        for index in range(len(input_lines)):
            coordinates[index] = []
            x: int = index
            for i in range(index + 1):
                coordinates[index].append((x, i))
                x -= 1
        return coordinates

    # get diagonal cordinates required - will reuse
    diagonal_coords: dict[int, list[tuple[int, int]]] = get_diagonal_coordinates(
        horizontal_lines
    )

    # use diagonal coordinates to get corresponding values
    def get_diagonals(
        coords: dict[int, list[tuple[int, int]]], input_lines: ListListStr
    ) -> ListListStr:
        diagonals: ListListStr = []
        for coord_level in coords.values():
            xy_list: list[str] = []
            for coord in coord_level:
                xy_list.append(input_lines[coord[0]][coord[1]])
            diagonals.append(xy_list)
        return diagonals

    # get half of the diagonals from 0,0
    diagonals_top_left: ListListStr = get_diagonals(diagonal_coords, horizontal_lines)

    # get half diagonals from max(x), max(y)
    # need to flip/reverse horizontal lines to
    # ensure the bottom right is now top left
    horizontal_lines_flip_reverse: ListListStr = [
        list(x)[::-1] for x in puzzle_input.splitlines()[::-1]
    ]

    diagonals_bottom_right: ListListStr = get_diagonals(
        diagonal_coords, horizontal_lines_flip_reverse
    )

    # reverse order of horizontal lines to get
    # diagonals from max(y), 0 as 0,0
    diagonals_bottom_left: ListListStr = get_diagonals(
        diagonal_coords, horizontal_lines[::-1]
    )

    # get other half of those above
    diagonals_top_right: ListListStr = get_diagonals(
        diagonal_coords, horizontal_lines_flip_reverse[::-1]
    )

    # join those together in a reasonable fashion
    lines: list[ListListStr] = [
        horizontal_lines,
        vertical_lines,
        diagonals_top_left
        + [x[::-1] for x in diagonals_bottom_right[:-1]][::-1],  # tl to br
        diagonals_top_right
        + [x[::-1] for x in diagonals_bottom_left[:-1]][::-1],  # bl to tr
    ]

    # check for XMAS
    def has_xmas(lines: ListListStr):
        """Check if XMAS in input for forward and reverse lines"""
        # rejoin strings and reverse for both direction check
        joined_strings: list[str] = ["".join(x) for x in lines]
        reversed_joined_strings: list[str] = ["".join(x[::-1]) for x in lines]

        forward_total: int = sum(len(re.findall("XMAS", x)) for x in joined_strings)
        backwards_total: int = sum(
            len(re.findall("XMAS", x)) for x in reversed_joined_strings
        )

        return forward_total + backwards_total

    # search for xmas
    part_1_total: int = sum(map(has_xmas, lines))

    # ---- PART 2 ----
    part_2_total: int = 0
    for row_index, row in enumerate(horizontal_lines):
        for col_index, col in enumerate(row[1:-1]):
            if col == "A":
                if row_index in (0, len(horizontal_lines) - 1):
                    pass
                else:
                    box_diag_1: tuple[str, str, str] = (
                        horizontal_lines[row_index + 1][col_index],
                        horizontal_lines[row_index][col_index + 1],
                        horizontal_lines[row_index - 1][col_index + 2],
                    )
                    box_diag_2: tuple[str, str, str] = (
                        horizontal_lines[row_index - 1][col_index],
                        horizontal_lines[row_index][col_index + 1],
                        horizontal_lines[row_index + 1][col_index + 2],
                    )
                    if ("".join(box_diag_1) in {"MAS", "SAM"}) and (
                        "".join(box_diag_2) in {"SAM", "MAS"}
                    ):
                        part_2_total += 1

    return part_1_total, part_2_total


# test on example input
# day4(EXAMPLE)

# go time!
day4(PUZZLE_INPUT)
