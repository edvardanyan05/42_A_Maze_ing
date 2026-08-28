PATTERN_42 = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1]
]

DIRECTIONS = (
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0)
        )


def is_42_cell(width: int, height: int, r: int, c: int) -> bool:
    if width < 9 or height < 7:
        return False

    start_row = (height - 5) // 2
    start_col = (width - 7) // 2

    pattern_r = r - start_row
    pattern_c = c - start_col

    if not (0 <= pattern_r < 5 and 0 <= pattern_c < 7):
        return False

    return PATTERN_42[pattern_r][pattern_c] == 1


def is_valid_cell(height: int, width: int, r: int, c: int) -> bool:
    return 0 <= r < height and 0 <= c < width


def has_wall(
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    val: int
) -> bool:
    dx, dy = x2 - x1, y2 - y1

    if dx == 1:
        return bool(val & 2)   # East
    if dx == -1:
        return bool(val & 8)   # West
    if dy == 1:
        return bool(val & 4)   # South
    if dy == -1:
        return bool(val & 1)   # North

    return True
