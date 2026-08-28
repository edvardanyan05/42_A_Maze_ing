import os
from typing import Optional, Any
from utils import is_42_cell

# Terminal colours
COLORS = {
    "BLUE": "\033[94m",
    "CYAN": "\033[96m",
    "MAGENTA": "\033[95m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[33m",
    "RED": "\033[91m",
    "WHITE": "\033[97m",
    "RESET": "\033[0m",
}

WALL_COLORS = [
    "BLUE",
    "CYAN",
    "GREEN",
    "MAGENTA",
    "WHITE",
]


def clear_terminal() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_maze(
    grid: list[list[int]],
    width: int,
    height: int,
    path: Optional[list[tuple[int, int]]] = None,
    entry: Optional[tuple[int, int]] = None,
    exit_: Optional[tuple[int, int]] = None,
    show_path: bool = True,
    wall_color_name: str = "BLUE",
) -> None:
    """Display the maze using coloured ASCII/Unicode characters."""

    wall_color = COLORS[wall_color_name]
    reset = COLORS["RESET"]

    entry_color = COLORS["GREEN"]
    exit_color = COLORS["RED"]
    path_color = COLORS["MAGENTA"]
    pattern_color = COLORS["YELLOW"]

    path_set = set(path) if path and show_path else set()

    # Characters used to draw the maze.
    horizontal = "───"
    vertical = "│"

    lines: list[str] = []

    # ---------------------------------------------------------
    # Top border
    # ---------------------------------------------------------
    top = wall_color + "┌"

    for c in range(width):
        top += horizontal

        if c < width - 1:
            top += "┬"
        else:
            top += "┐"

    top += reset
    lines.append(top)

    # ---------------------------------------------------------
    # Maze rows
    # ---------------------------------------------------------
    for r in range(height):

        middle = wall_color + vertical

        for c in range(width):
            cell = (r, c)

            # Cell contents
            if cell == entry:
                content = f"{entry_color} S {reset}"

            elif cell == exit_:
                content = f"{exit_color} E {reset}"

            elif cell in path_set:
                content = f"{path_color} • {reset}"

            elif is_42_cell(width, height, r, c):
                content = f"{pattern_color}42 {reset}"

            else:
                content = "   "

            middle += content

            # East wall
            if grid[r][c] & 2:
                middle += wall_color + vertical + reset
            else:
                middle += " "

        lines.append(middle)

        # -----------------------------------------------------
        # Horizontal wall between this row and the next
        # -----------------------------------------------------
        if r < height - 1:
            separator = wall_color + "├"

            for c in range(width):

                if grid[r][c] & 4:
                    separator += horizontal
                else:
                    separator += "   "

                if c < width - 1:
                    separator += "┼"
                else:
                    separator += "┤"

            separator += reset
            lines.append(separator)

    # ---------------------------------------------------------
    # Bottom border
    # ---------------------------------------------------------
    bottom = wall_color + "└"

    for c in range(width):
        bottom += horizontal

        if c < width - 1:
            bottom += "┴"
        else:
            bottom += "┘"

    bottom += reset
    lines.append(bottom)

    print("\n".join(lines))

def display_maze(
    maze: list[list[int]],
    path: list[tuple[int, int]],
    config_dict: dict[str, Any],
    show_path: bool,
    wall_color: str,
) -> None:
    """Display the maze and the available controls matching the 42 subject."""

    clear_terminal()

    print("=== A-Maze-ing ===")
    print(
        f"Size: {config_dict['WIDTH']} x {config_dict['HEIGHT']} | "
        f"Entry: {config_dict['ENTRY']} | Exit: {config_dict['EXIT']}"
    )
    print()

    print_maze(
        maze,
        config_dict["WIDTH"],
        config_dict["HEIGHT"],
        path,
        config_dict["ENTRY"],
        config_dict["EXIT"],
        show_path,
        wall_color,
    )

    print()
    if show_path:
        print("Solution path: SHOWN")
    else:
        print("Solution path: HIDDEN")

    print()
    print("1. Re-generate a new maze")
    print("2. Show/Hide the shortest path")
    print("3. Rotate the wall colours")
    print("4. Quit")