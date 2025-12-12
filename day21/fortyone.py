"""
11529
"""

from itertools import product

START = 'S'
ROCK = '#'

with open('input.txt', 'r') as f_in:
    rows = [row.strip() for row in f_in.readlines()]  # TODO to class attributes
len_x = len(rows[0])
len_y = len(rows)


def get_adjacent(idx: tuple[int, int]) -> set:
    """Add adjacent locations to set"""
    new = set()
    # this would be ok with 8 directions
    # for i in range(idx[0] - 1, idx[0] + 2):
    #     for j in range(idx[1] - 1, idx[1] + 2):
    #         if i == idx[0] and j == idx[1]:
    #             continue
    for i, j in (
        (idx[0] - 1, idx[1]),
        (idx[0] + 1, idx[1]),
        (idx[0], idx[1] - 1),
        (idx[0], idx[1] + 1),
    ):
        if 0 <= i < len_x and 0 <= j < len_y:
            if rows[i][j] != ROCK:
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
    for _ in range(64):
        for item in locations:
            new.update(get_adjacent(item))
        locations = new
        new = set()

    # for row_count, row in enumerate(rows):
    #     print(''.join([item if tuple([row_count, count]) not in locations else 'O' for count, item in enumerate(row)]))

    return len(locations)


if __name__ == '__main__':
    print(main())
