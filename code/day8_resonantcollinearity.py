"""Day 8 - Resonant Collinearity"""

import itertools
from rich.progress import track

import useful_functions

EXAMPLE_INPUT = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............""".strip()

# custom types
Coordinate = tuple[int, int]
FrequencyMap = dict[str, list[Coordinate]]

PUZZLE_INPUT: str = useful_functions.input_data_read("../text_inputs/day_8.txt")

# split into lines
example_data: list[str] = EXAMPLE_INPUT.splitlines()
puzzle_data: list[str] = PUZZLE_INPUT.splitlines()


class LinearEquation:
    """Class for linear equation calculations.
    Used in Part 1.
    """

    # realised did not need to do it this way, but kept in for prosperity!
    @staticmethod
    def find_gradient(point1: Coordinate, point2: Coordinate) -> float | int:
        """Calculate slope (m) of line between two points"""
        # m = (y2-y1)/(x2-x1)
        x1, y1 = point1
        x2, y2 = point2
        m = (y2 - y1) / (x2 - x1)
        return m

    @staticmethod
    def find_next_prev_x(x1: int, x2: int) -> Coordinate:
        """Find next and previous x-coords"""
        next_x: int = x2 + (x2 - x1)
        prev_x: int = x1 - (x2 - x1)
        return next_x, prev_x

    @staticmethod
    def y_intercept(x1: int, y1: int, m: float | int) -> float | int:
        """Find y-intercept (c) of line"""
        c: float | int = y1 - (m * x1)
        return c

    @staticmethod
    def find_next_y(m: float | int, x: int, c: float | int) -> float | int:
        """Find y-coordinate for a given x, slope (m), y-intercept (c)"""
        y: float | int = (m * x) + c
        return y


@useful_functions.report_results
def day8(puzzle_input):
    """Day 8 - Resonant Collinearity Working Solution"""

    # find all the instances of tokens, and log coordinates.
    def find_frequencies(grid: list[str]) -> FrequencyMap:
        """Find coordinates of all frequencies"""
        frequencies: FrequencyMap = {}
        for row_index, row in enumerate(grid):
            for col_index, char in enumerate(row):
                if char.isalnum():
                    frequencies.setdefault(char, []).append((col_index, row_index))
        return frequencies

    # get all combos of two
    def get_pair_combos(
        coordinates: list[Coordinate],
    ) -> list[tuple[Coordinate, Coordinate]]:
        """Get all combos of pairs from list of frequency coords"""
        return list(itertools.combinations(coordinates, 2))

    def part_1_solve(
        point1: Coordinate, point2: Coordinate
    ) -> tuple[Coordinate, Coordinate]:
        x1, y1 = point1
        x2, _ = point2  # _ = y2, isn't used in anything.
        equation = LinearEquation()

        m: float | None
        m = equation.find_gradient(point1, point2)
        next_x, prev_x = equation.find_next_prev_x(x1, x2)
        c: float | int = equation.y_intercept(x1, y1, m)

        next_y: int = int(equation.find_next_y(m, next_x, c))
        prev_y: int = int(equation.find_next_y(m, prev_x, c))

        return (next_x, next_y), (prev_x, prev_y)

    def is_in_grid(point: Coordinate, height: int, width: int):
        """Check if a point is within the grid boundaries"""
        return 0 <= point[0] < width and 0 <= point[1] < height

    # a different, simpler method for part 2
    def find_differences(point1: Coordinate, point2: Coordinate):
        antinodes_part2: set[Coordinate] = set()

        x1, y1 = point1
        x2, y2 = point2
        dx, dy = x2 - x1, y2 - y1

        next_x, next_y = x1, y1
        prev_x, prev_y = x1, y1

        # go up from x1
        while is_in_grid((next_x, next_y), grid_height, grid_width):
            antinodes_part2.add((next_x, next_y))
            next_x, next_y = dx + next_x, dy + next_y
        # now go down from x1
        while is_in_grid((prev_x, prev_y), grid_height, grid_width):
            antinodes_part2.add((prev_x, prev_y))
            prev_x, prev_y = prev_x - dx, prev_y - dy
        return antinodes_part2

    # get the grid dimensions
    grid_height, grid_width = len(puzzle_input), len(puzzle_input[0])

    # find frequencies of antennas
    frequencies = find_frequencies(puzzle_input)

    # generate pairs of antennas on same frequencies
    frequency_pair_combos = {k: get_pair_combos(v) for k, v in frequencies.items()}

    # place to store the antinode locations
    first_antinode_locations: set[Coordinate] = set()
    all_antinodes: set[Coordinate] = set()

    for list_of_pairs in track(
        frequency_pair_combos.values(), description="Collinearising..."
    ):
        for pair in list_of_pairs:
            p1, p2 = pair
            next_antinode, prev_antinode = part_1_solve(p1, p2)
            all_antinodes.update(find_differences(p1, p2))
            if is_in_grid(next_antinode, grid_height, grid_width):
                first_antinode_locations.add(next_antinode)
            if is_in_grid(prev_antinode, grid_height, grid_width):
                first_antinode_locations.add(prev_antinode)

    part1 = len(first_antinode_locations)
    part2 = len(all_antinodes)

    return part1, part2


if __name__ == "__main__":
    day8(puzzle_data)

# TODO: would be fun to try and visualise this
# TODO: clean it up and make it easier to follow
# TODO: better & consistent typing
# TODO: better/earlier use of sets instead of lists.
