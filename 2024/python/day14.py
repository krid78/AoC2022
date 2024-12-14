"""Solve Advent of Code 2024, day 14

https://adventofcode.com/2024/day/14
"""

import time


def get_data(filename: str) -> list[dict[str, tuple[int, int]]]:
    """
    Return file contents as a structured list of dictionaries.

    Args:
        filename (str): Path to the input file.

    Returns:
        list[dict[str, tuple[int, int]]]: A list of dictionaries, where each dictionary
        contains the position 'p' and velocity 'v' as tuples.
    """
    data = []
    with open(filename, "r") as in_file:
        for line in in_file:
            line = line.strip()
            if line:
                # Parse position (p) and velocity (v)
                p_part, v_part = line.split(" ")
                px, py = map(int, p_part[2:].split(","))
                vx, vy = map(int, v_part[2:].split(","))
                data.append({"p": (px, py), "v": (vx, vy)})
    return data


def draw_bot_map(bot_pos, max_row, max_col):
    """
    Draw the bot positions on the grid.

    Args:
        bot_pos (list[tuple[int, int]]): List of bot positions.
        max_row (int): Number of rows in the grid.
        max_col (int): Number of columns in the grid.
    """
    grid = [[" " for _ in range(max_col)] for _ in range(max_row)]

    for r, c in bot_pos:
        grid[r][c] = "#"

    for row in grid:
        print("".join(row))


# Speichern der Positionen in einer Datei
def save_bot_map(bot_pos, max_row, max_col, steps):
    """
    Save the bot positions to a text file.

    Args:
        bot_pos (list[tuple[int, int]]): List of bot positions.
        max_row (int): Maximum rows in the grid.
        max_col (int): Maximum columns in the grid.
        steps (int): Current number of steps, used in the filename.
    """
    filename = f"bot_map_{steps:05d}.txt"
    with open(filename, "w") as f:
        for r in range(max_row):
            for c in range(max_col):
                if (r, c) in bot_pos:
                    f.write("#")
                else:
                    f.write(".")
            f.write("\n")  # Newline after each row
    print(f"Map saved to {filename}")


def calculate_position(bot, steps, max_row, max_col):
    """
    Calculate the position of a bot after a given number of steps.

    Args:
        bot (dict): A dictionary containing 'p' (position) and 'v' (velocity).
        steps (int): Number of steps to simulate.
        max_row (int): Maximum row index for the grid.
        max_col (int): Maximum column index for the grid.

    Returns:
        tuple[int, int]: The new position (row, col).
    """
    r = (bot["p"][1] + bot["v"][1] * steps) % max_row
    c = (bot["p"][0] + bot["v"][0] * steps) % max_col
    return r, c


def update_quadrants(row, col, max_row, max_col, quadrants):
    """
    Update the quadrants count based on the given position, skipping the middle row/col.

    Args:
        row (int): Row index.
        col (int): Column index.
        max_row (int): Maximum row index.
        max_col (int): Maximum column index.
        quadrants (list[int]): List of four quadrant counts.
    """
    half_row = max_row // 2
    half_col = max_col // 2

    # Top-left quadrant
    if 0 <= row < half_row and 0 <= col < half_col:
        quadrants[0] += 1
    # Top-right quadrant
    elif 0 <= row < half_row and half_col < col < max_col:
        quadrants[1] += 1
    # Bottom-right quadrant
    elif half_row < row < max_row and half_col < col < max_col:
        quadrants[2] += 1
    # Bottom-left quadrant
    elif half_row < row < max_row and 0 <= col < half_col:
        quadrants[3] += 1
    # Debugging for unexpected positions
    else:
        print(f"Position ({row}, {col}) does not fit into any quadrant.")


def solve_part1(the_data, steps, max_row, max_col):
    quadrants = [0, 0, 0, 0]
    bot_final_pos = []

    for bot in the_data:
        # Berechnung der Endposition nach `steps`
        r, c = calculate_position(bot, steps, max_row, max_col)
        bot_final_pos.append((r, c))
        # Aktualisiere Quadranten
        update_quadrants(r, c, max_row, max_col, quadrants)

    # draw_bot_map(bot_final_pos, max_row, max_col)
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def is_christmas_tree(bot_pos, max_row, max_col):
    """
    Check if the bot positions form a Christmas tree pattern.

    Args:
        bot_pos (set[tuple[int, int]]): Set of bot positions (row, col).
        max_row (int): Maximum rows in the grid.
        max_col (int): Maximum columns in the grid.

    Returns:
        bool: True if the bots form a Christmas tree, False otherwise.
    """
    rows = {}
    for r, c in bot_pos:
        if r not in rows:
            rows[r] = []
        rows[r].append(c)

    sorted_rows = sorted(rows.items())  # Sort by row index
    prev_width = 0

    for i, (row, cols) in enumerate(sorted_rows):
        cols.sort()
        width = len(cols)
        center = sum(cols) / width  # Calculate center of current row

        # Check symmetry
        if not all(
            cols[j] + cols[-(j + 1)] == 2 * center for j in range(len(cols) // 2)
        ):
            return False

        # Check increasing width for tree shape
        if width <= prev_width and i > 0:
            return False
        prev_width = width

    return True


def solve_part2(the_data, steps, max_row, max_col):
    """
    Find when all bots return to their starting positions.

    Args:
        the_data (list[dict]): List of bots with positions and velocities.
        steps (int): Maximum number of steps to simulate.
        max_row (int): Maximum row index for the grid.
        max_col (int): Maximum column index for the grid.

    Returns:
        int: The number of steps required for all bots to return to their starting positions.
    """
    bot_start_pos = {calculate_position(bot, 0, max_row, max_col) for bot in the_data}

    for step in range(1, steps + 1):
        bot_pos = {calculate_position(bot, step, max_row, max_col) for bot in the_data}

        # Check for Christmas tree pattern
        if is_christmas_tree(bot_pos, max_row, max_col):
            print(f"Christmas tree pattern found at step {step}.")
            save_bot_map(bot_pos, max_row, max_col, step)  # Optional: Save the pattern
            return step
        elif bot_pos == bot_start_pos:
            print(f"All bots are back in their start position at step {step}.")
            break

        print("=" * 25 + f" Bots at step {step} " + "=" * 25)
        draw_bot_map(bot_pos, max_row, max_col)
        time.sleep(.20)
        # save_bot_map(bot_pos, max_row, max_col, step)

    return -1  # Return -1 if no solution found within the given steps


def solve():
    """Solve the puzzle."""
    solution1 = 0
    solution2 = 0

    the_data = get_data("2024/data/day14.data")
    solution1 = solve_part1(the_data, 100, 103, 101)
    # solution2 = solve_part2(the_data, 75, 103, 101)
    solution2 = solve_part2(the_data, 10500, 103, 101)

    # the_data = get_data("2024/data/day14.test")
    # solution1 = solve_part1(the_data, 100, 7, 11)
    # solution2 = solve_part2(the_data, 100, 7, 11)

    return solution1, solution2


if __name__ == "__main__":
    time_start = time.perf_counter()
    solution1, solution2 = solve()
    print(f"Solved in {time.perf_counter()-time_start:.5f} Sec.")
    print(f"{solution1=} | {solution2=}")
