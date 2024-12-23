"""Day 6 - GG, only Part 1"""
import os
import time
import itertools
import useful_functions

# custom types
PuzzleRows = list[str]

# example Input
EXAMPLE: str = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".strip()

# read puzzle input from text
PUZZLE_INPUT: str = useful_functions.input_data_read("../text_inputs/day_6.txt")

# split input into rows
puzzle_data: PuzzleRows = EXAMPLE.splitlines()
# puzzle_data: PuzzleRows = PUZZLE_INPUT.splitlines()

# cycle iterator for progressing through direction
direction_order = itertools.cycle(["up", "right", "down", "left"])


def get_start_index(puzzle: PuzzleRows):
    """
    Get sprite start index.
    For puzzle purposes - have assumed will always be facing up.
    """
    for i, row in enumerate(puzzle):
        if "^" in row:
            return row.index("^"), i


def get_blockers(i: int, puzzle_input_row: str):
    """
    Get locations of all blockers.
    """
    # for one row
    obstacles = [
        (index, i) for index, step in enumerate(puzzle_input_row) if step == "#"
    ]
    return tuple(itertools.chain(*obstacles)) if obstacles else None


def move_guard_one_step(
    grid: PuzzleRows, guard_position: tuple[int, int], direction: str
):
    """
    Move the guard one step in the current direction.
    If blocked, turn 90° clockwise - aka cycle next direction.
    """
    x, y = guard_position

    # movement map
    move_map = {
        "up": (0, -1),
        "right": (1, 0),
        "down": (0, 1),
        "left": (-1, 0),
    }

    # get movement change
    dx, dy = move_map[direction]
    # add it to your current x,y position
    new_x, new_y = x + dx, y + dy

    # check for blocker
    if grid[new_y][new_x] == "#":
        # turn 90 clockwise if blocked - new direction
        new_direction = next(direction_order)
        return (x, y), new_direction

    # move forward one step, keep direction
    return (new_x, new_y), direction


def display_grid(
    grid: PuzzleRows,
    guard_pos: tuple[int, int],
    visited: set[tuple[int, int]],
    revisited: set[tuple[int, int]],
    distinct_counter: int,
    step_counter: int,
    direction: str,
    escaped=False,
):
    """
    Display the grid with the guard's position/blockers.
    Also visited/revisited markers.
    """
    os.system("cls" if os.name == "nt" else "clear")  # clear screen

    # sprites for direction and escape!
    marker_map = {"up": "^", "down": "v", "left": "<", "right": ">", "escaped": "⭐"}

    if escaped is True:
        direction = "escaped"

    # current 'quirk' - will consider each direction change a new
    # set of coords in such a way that the end of one movement,
    # and the start of the next considers it 'revisited'

    for y, row in enumerate(grid):
        line = ""
        for x, char in enumerate(row):
            if (x, y) == guard_pos:
                line += marker_map[direction]  # "^"  # Guard's position
            elif (x, y) in revisited:
                line += "+"  # Revisited
            elif (x, y) in visited:
                line += "X"  # First time visited
            else:
                line += char
        print(line)

    # print counters, current pos and distinct visits
    print(
        f"\nSteps: {step_counter} | Current X,Y {guard_pos} ",
        f"| Distinct Places Visited: {distinct_counter+1}",
    )


def get_edges(grid: PuzzleRows) -> list[tuple[int, int]]:
    """Get all the coordinates at the grid's edges."""
    height = len(grid)
    width = len(grid[0])

    top_row = [(i, 0) for i in range(width)]
    bottom_row = [(i, height - 1) for i in range(width)]
    left_col = [(0, i) for i in range(height)]
    right_col = [(width - 1, i) for i in range(height)]

    return top_row + bottom_row + left_col + right_col


def escape(grid: PuzzleRows):
    """Main game loop to move the guard step by step."""
    # Find the starting position of the guard
    guard_pos = get_start_index(grid)

    # starting direction - should be up!
    # although is it worth adding check?
    direction = "up"

    # keep track of visited positions
    visited: set[tuple[int, int]] = set()
    revisited: set[tuple[int, int]] = set()

    # counters
    distinct_counter = 0
    step_counter = 0

    # stay in while loop until escape
    while True:
        # check the current position for visited before
        if guard_pos in visited:
            revisited.add(guard_pos)
        else:
            visited.add(guard_pos)
            distinct_counter += 1

        # display grid
        display_grid(
            grid,
            guard_pos,
            visited,
            revisited,
            distinct_counter,
            step_counter,
            direction,
        )

        # move one step
        guard_pos, direction = move_guard_one_step(grid, guard_pos, direction)
        step_counter += 1

        # if reach edge - you've escaped!
        if guard_pos in get_edges(grid):
            display_grid(
                grid,
                guard_pos,
                visited,
                revisited,
                distinct_counter,
                step_counter,
                direction,
                escaped=True,
            )
            print("\nThe guard has escaped!")
            break


if __name__ == "__main__":
    start_time = time.time()
    escape(puzzle_data)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Time Taken: {total_time:.2f} secs")
