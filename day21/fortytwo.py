"""
Valid solution, just will run for several years maybe for the input size
"""

from functools import cache
from itertools import product

from fortyone import ROCK, START

with open('input.txt', 'r') as f_in:
    rows = [row.strip() for row in f_in.readlines()]
len_x = len(rows[0])
len_y = len(rows)


@cache
def not_rock(i_mod: int, j_mod: int) -> bool:
    """Check if location is not rock"""
    return rows[i_mod][j_mod] != ROCK


@cache
def get_adjacent(idx: tuple[int, int]) -> set:
    """Add adjacent locations to set"""
    new = set()
    for i, j in (
        (idx[0] - 1, idx[1]),
        (idx[0] + 1, idx[1]),
        (idx[0], idx[1] - 1),
        (idx[0], idx[1] + 1),
    ):
        i_mod = i % len_x
        j_mod = j % len_y
        if not_rock(i_mod, j_mod):
            new.add((i, j))

    return new


def main() -> int:
    """main"""
    for idx in product(range(len_x), range(len_y)):
        if rows[idx[0]][idx[1]] == START:
            break
    else:
        raise ValueError('No starting point found')

    locations: set[tuple[int, int]] = set()
    new = get_adjacent(idx)
    for _ in range(50):  # 26_501_365
        for item in locations:
            new.update(get_adjacent(item))
        locations = new
        new = set()

    return len(locations)


if __name__ == '__main__':
    print(main())
