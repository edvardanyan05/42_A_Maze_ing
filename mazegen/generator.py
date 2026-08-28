import random
from typing import Any, Tuple, List, Set
from utils import is_42_cell, is_valid_cell, PATTERN_42, DIRECTIONS


class MazeGenerator:
    width: int
    height: int
    perfect: bool
    seed: Any

    def __init__(
            self,
            dict_config: dict[str, Any]
    ) -> None:
        self.width = dict_config["WIDTH"]
        self.height = dict_config["HEIGHT"]
        self.perfect = dict_config["PERFECT"]
        self.seed = dict_config.get("SEED", None)

    def generate(self) -> List[List[int]]:
        grid = [[15] * self.width for _ in range(self.height)]
        visited = [[False] * self.width for _ in range(self.height)]

        if self.seed is not None:
            random.seed(self.seed)

        if not self._has_42():
            print("Error: Maze size is too small to fit the '42' pattern.")
        else:
            self._place_42_pattern(visited)

        while True:
            start_r = random.randrange(self.height)
            start_c = random.randrange(self.width)

            if not visited[start_r][start_c]:
                break  # exclude the 42 path

        visited[start_r][start_c] = True

        frontier: Set[Tuple[int, int]] = set()
        frontier.update(self._get_valid_neighbors(
            start_r, start_c, visited, False)
            )

        while frontier:
            cur_r, cur_c = random.choice(tuple(frontier))
            frontier.remove((cur_r, cur_c))
            valid_neighbors = self._get_valid_neighbors(
                cur_r, cur_c, visited, True
                )
            if valid_neighbors:
                connect_to_r, connect_to_c = random.choice(valid_neighbors)
                self._remove_wall(
                    cur_r, cur_c, connect_to_r, connect_to_c, grid
                    )
            visited[cur_r][cur_c] = True
            unvisited_neighbors = self._get_valid_neighbors(
                cur_r, cur_c, visited, False
                                                      )
            frontier.update(unvisited_neighbors)

        if not self.perfect:
            self._remove_dead_ends(grid)

        return grid

    def _remove_dead_ends(self, grid: list[list[int]]) -> None:
        for r in range(self.height):
            for c in range(self.width):
                # Skip the 42 pattern cells
                if is_42_cell(self.width, self.height, r, c):
                    continue

                if self._is_dead_end(grid[r][c]):
                    neighbors = []
                    cell_val = grid[r][c]

                    # Directions: (dr, dc, wall_bit)
                    directions = [
                        (-1, 0, 1),  # Nort
                        (1, 0, 4),   # South
                        (0, -1, 8),  # West
                        (0, 1, 2)    # East
                    ]

                    for dr, dc, wall_bit in directions:
                        nr, nc = r + dr, c + dc
                        if (
                            is_valid_cell(self.height, self.width, nr, nc)
                            and not is_42_cell(
                                self.width, self.height, nr, nc
                            )
                        ):
                            if cell_val & wall_bit:
                                neighbors.append((nr, nc))

                    # Pick a valid closed neighbor and knock down the wall
                    if neighbors:
                        nr, nc = random.choice(neighbors)
                        self._remove_wall(r, c, nr, nc, grid)

    def _is_dead_end(self, cell_value: int) -> bool:
        return cell_value in {7, 11, 13, 14}

    def _remove_wall(
        self,
        r1: int,
        c1: int,
        r2: int,
        c2: int,
        grid: List[List[int]]
    ) -> None:
        if r2 == r1 - 1:  # north
            grid[r1][c1] &= ~1
            grid[r2][c2] &= ~4
        elif r2 == r1 + 1:  # south
            grid[r1][c1] &= ~4
            grid[r2][c2] &= ~1
        elif c2 == c1 - 1:  # west
            grid[r1][c1] &= ~8
            grid[r2][c2] &= ~2
        elif c2 == c1 + 1:  # east
            grid[r1][c1] &= ~2
            grid[r2][c2] &= ~8

    def _get_valid_neighbors(
        self,
        r: int,
        c: int,
        visited: List[List[bool]],
        want_visited: bool
    ) -> List[Tuple[int, int]]:
        neighbors: List[Tuple[int, int]] = []

        for dr, dc in DIRECTIONS:
            neighbor_r = r + dr
            neighbor_c = c + dc

            if (
                is_valid_cell(self.height, self.width, neighbor_r, neighbor_c)
                and visited[neighbor_r][neighbor_c] == want_visited
            ):
                neighbors.append((neighbor_r, neighbor_c))

        return [
            (r, c)
            for r, c in neighbors
            if not is_42_cell(self.width, self.height, r, c)
        ]

    def _place_42_pattern(
            self,
            visited: List[List[bool]]
    ) -> None:
        start_row = (self.height - 5) // 2
        start_col = (self.width - 7) // 2

        for r_idx, row_vals in enumerate(PATTERN_42):
            for c_idx, val in enumerate(row_vals):
                r = start_row + r_idx
                c = start_col + c_idx

                if val == 1:
                    visited[r][c] = True

    def _has_42(self) -> bool:
        return self.width >= 9 and self.height >= 7
