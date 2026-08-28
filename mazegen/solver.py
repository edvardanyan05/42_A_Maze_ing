from collections import deque
from utils import DIRECTIONS, has_wall, is_42_cell, is_valid_cell


def everything_is_okay(
        grid: list[list[int]],
        width: int,
        height: int,
        cur_r: int,
        cur_c: int,
        neigh_r: int,
        neigh_c: int,
        parent: list[list[tuple[int, int] | None]] = []
) -> bool:
    return (
        is_valid_cell(height, width, neigh_r, neigh_c)
        and not is_42_cell(width, height, neigh_r, neigh_c)
        and not has_wall(cur_c, cur_r, neigh_c, neigh_r, grid[cur_r][cur_c])
        and parent[neigh_r][neigh_c] == (-1, -1)
    )


def reconstruct_path(
        parent_fwd: list[list[tuple[int, int] | None]],
        parent_bwd: list[list[tuple[int, int] | None]],
        meet_point: tuple[int, int]
) -> list[tuple[int, int]]:
    path: list[tuple[int, int]] = []

    curr: tuple[int, int] | None = meet_point
    while curr is not None:
        path.append(curr)
        curr = parent_fwd[curr[0]][curr[1]]

    path.reverse()

    curr = parent_bwd[meet_point[0]][meet_point[1]]
    while curr is not None:
        path.append(curr)
        curr = parent_bwd[curr[0]][curr[1]]

    return path


def shortest_path(
        grid: list[list[int]],
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
) -> list[tuple[int, int]]:
    q_fwd: deque[tuple[int, int]] = deque()
    parent_fwd: list[list[tuple[int, int] | None]]
    parent_fwd = [[(-1, -1) for _ in range(width)] for _ in range(height)]
    q_bwd: deque[tuple[int, int]] = deque()
    parent_bwd: list[list[tuple[int, int] | None]]
    parent_bwd = [[(-1, -1) for _ in range(width)] for _ in range(height)]

    entry_r = entry[0]
    entry_c = entry[1]
    exit_r = exit[0]
    exit_c = exit[1]

    q_fwd.append(entry)
    parent_fwd[entry_r][entry_c] = None
    q_bwd.append(exit)
    parent_bwd[exit_r][exit_c] = None

    while q_fwd or q_bwd:
        # --- Expand Forward Step ---
        if q_fwd:
            fwd_r, fwd_c = q_fwd.popleft()
            for dr, dc in DIRECTIONS:
                neigh_fwd_r = fwd_r + dr
                neigh_fwd_c = fwd_c + dc

                if everything_is_okay(
                    grid,
                    width,
                    height,
                    fwd_r,
                    fwd_c,
                    neigh_fwd_r,
                    neigh_fwd_c,
                    parent_fwd
                ):
                    parent_fwd[neigh_fwd_r][neigh_fwd_c] = (fwd_r, fwd_c)
                    q_fwd.append((neigh_fwd_r, neigh_fwd_c))
                    if parent_bwd[neigh_fwd_r][neigh_fwd_c] != (-1, -1):
                        meet_point = (neigh_fwd_r, neigh_fwd_c)
                        return reconstruct_path(
                            parent_fwd,
                            parent_bwd,
                            meet_point
                        )

        # --- Expand Backward Step ---
        if q_bwd:
            bwd_r, bwd_c = q_bwd.popleft()
            for dr, dc in DIRECTIONS:
                neigh_bwd_r = bwd_r + dr
                neigh_bwd_c = bwd_c + dc

                if everything_is_okay(
                    grid,
                    width,
                    height,
                    bwd_r,
                    bwd_c,
                    neigh_bwd_r,
                    neigh_bwd_c,
                    parent_bwd
                ):
                    parent_bwd[neigh_bwd_r][neigh_bwd_c] = (bwd_r, bwd_c)
                    q_bwd.append((neigh_bwd_r, neigh_bwd_c))
                    if parent_fwd[neigh_bwd_r][neigh_bwd_c] != (-1, -1):
                        meet_point = (neigh_bwd_r, neigh_bwd_c)
                        return reconstruct_path(
                            parent_fwd,
                            parent_bwd,
                            meet_point
                        )

    # No path found
    print("Error: Random generation created an unreachable maze!")
    # sys.exit(1)
    return []


# Path to directions - > W N E S
def path_to_directions(path: list[tuple[int, int]]) -> str:
    directions: str = ""
    for i in range(1, len(path)):
        prev_r, prev_c = path[i - 1]
        curr_r, curr_c = path[i]

        if curr_r == prev_r and curr_c == prev_c + 1:
            directions += "E"
        elif curr_r == prev_r and curr_c == prev_c - 1:
            directions += "W"
        elif curr_r == prev_r + 1 and curr_c == prev_c:
            directions += "S"
        elif curr_r == prev_r - 1 and curr_c == prev_c:
            directions += "N"
    return directions
