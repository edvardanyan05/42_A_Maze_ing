#!/usr/bin/env python3

import sys
import random
from typing import Any

from my_exceptions import ConfigError
from parse_validate import read_maze_file, parse_to_dict
from mazegen import MazeGenerator, shortest_path, path_to_directions
from maze_display import (
    WALL_COLORS,
    clear_terminal,
    display_maze,
)
"""  """

def generate_maze(
    config_dict: dict[str, Any],
) -> tuple[list[list[int]], list[tuple[int, int]]]:
    """
    Generate a maze and calculate its shortest path.

    This keeps the original project logic:
        MazeGenerator -> generate()
        shortest_path() -> solve maze
    """

    maze_generator = MazeGenerator(config_dict)
    maze = maze_generator.generate()

    path = shortest_path(
        maze,
        config_dict["WIDTH"],
        config_dict["HEIGHT"],
        config_dict["ENTRY"],
        config_dict["EXIT"],
    )

    return maze, path


def write_output_file(
    maze: list[list[int]],
    path: list[tuple[int, int]],
    config_dict: dict[str, Any],
) -> None:
    """Write the complete maze grid, entry, exit, and direction path to the output file."""
    output_file = config_dict["OUTPUT_FILE"]
    width = config_dict["WIDTH"]
    height = config_dict["HEIGHT"]
    entry = config_dict["ENTRY"]
    exit_ = config_dict["EXIT"]

    lines = []
    
    # 1. Convert each cell's bitmask to a single hex character row by row
    for r in range(height):
        row_str = ""
        for c in range(width):
            # Format the integer wall value as a lowercase hex digit (0-f)
            row_str += format(maze[r][c], "x")
        lines.append(row_str)

    # 2. Add an empty line separator
    lines.append("")

    # 3. Add entry and exit coordinates
    lines.append(f"{entry[0]},{entry[1]}")
    lines.append(f"{exit_[0]},{exit_[1]}")

    # 4. Add the direction path string (N, E, S, W)
    lines.append(path_to_directions(path))

    # Write everything with a trailing newline for each line
    with open(output_file, "w") as f:
        f.write("\n".join(lines) + "\n")


def interactive_mode(config_dict: dict[str, Any]) -> None:
    """Run the interactive maze display using numerical choices."""

    maze, path = generate_maze(config_dict)
    write_output_file(maze, path, config_dict)

    show_path = True
    wall_color_index = 0
    wall_color = WALL_COLORS[wall_color_index]

    while True:
        display_maze(
            maze,
            path,
            config_dict,
            show_path,
            wall_color,
        )

        try:
            command = input("\nChoice? (1-4): ").strip()

        except (KeyboardInterrupt, EOFError):
            print()
            break

        # 1: Re-generate a new maze
        if command == "1":
            new_config = config_dict.copy()
            new_config["SEED"] = random.SystemRandom().randint(
                0,
                2**32 - 1,
            )
            maze, path = generate_maze(new_config)
            write_output_file(maze, path, config_dict)
            config_dict = new_config

        # 2: Show/Hide the shortest path
        elif command == "2":
            show_path = not show_path

        # 3: Rotate the wall colours
        elif command == "3":
            wall_color_index = (
                wall_color_index + 1
            ) % len(WALL_COLORS)
            wall_color = WALL_COLORS[wall_color_index]

        # 4: Quit
        elif command == "4":
            break

        elif command:
            print("\nInvalid choice. Please enter a number between 1 and 4.")
            input("Press Enter to continue...")

    clear_terminal()


if __name__ == "__main__":

    # ---------------------------------------------------------
    # Original argument handling
    # ---------------------------------------------------------
    if len(sys.argv) != 2:
        print(
            "Usage: python3 a_maze_ing.py <config_file>"
        )
        sys.exit(1)

    config_file = sys.argv[1]

    # ---------------------------------------------------------
    # Original configuration parsing
    # ---------------------------------------------------------
    try:
        file_content = read_maze_file(config_file)

        config_dict = parse_to_dict(file_content)

    except ConfigError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    # ---------------------------------------------------------
    # Interactive maze
    # ---------------------------------------------------------
    try:
        interactive_mode(config_dict)

    except ConfigError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)