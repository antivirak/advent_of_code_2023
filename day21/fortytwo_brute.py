from functools import cache
from itertools import product

START = 'S'
ROCK = '#'

with open('test_input2.txt', 'r') as f_in:
    rows = [row.strip() for row in f_in.readlines()]
len_x = len(rows[0])
len_y = len(rows)


@cache
def not_rock(i_mod: int, j_mod: int) -> bool:
    if rows[i_mod][j_mod] != ROCK:
        return True

    return False


@cache
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
        i_mod = i % len_x
        j_mod = j % len_y
        # if i < len(rows[0]) and j < len(rows):
            # locations.add((i, j))
        if not_rock(i_mod, j_mod):
            new.add((i, j))

    return new


def _():
    last_total = [-1, -1]
    while True:
        # if _ > len_x + 1:
        #     for row_count, row in enumerate(rows):
        #         locations_mod = set(item for item in locations if 0 <= item[0] < len_x and 0 <= item[1] < len_y)
        #         print(''.join([item if tuple([row_count, count]) not in locations_mod else 'O' for count, item in enumerate(row)]))
        #     print()
        total = 0
        for row_count, row in enumerate(rows):
            locations_mod = set(item for item in locations if 0 <= item[0] < len_x and 0 <= item[1] < len_y)
            total += ''.join([item if tuple([row_count, count]) not in locations_mod else 'O' for count, item in enumerate(row)]).count('O')
        print(total)
        if total == last_total[1]:
            print('repeated', _)
            break
        last_total[1] = last_total[0]
        last_total[0] = total

        for item in locations:
            new.update(get_adjacent(item))
        locations = new
        new = set()


def main() -> int:
    """main"""
    for idx in product(range(len_x), range(len_y)):
        if rows[idx[0]][idx[1]] == START:
            break
    else:
        raise ValueError('No starting point found')

    locations = set()
    new = get_adjacent(idx)
    for _ in range(500):  # 26_501_365
        for item in locations:
            new.update(get_adjacent(item))
        locations = new
        new = set()

    # for row_count, row in enumerate(rows):
    #     print(''.join([item if tuple([row_count, count]) not in locations else 'O' for count, item in enumerate(row)]))

    return len(locations)


if __name__ == '__main__':
    from datetime import datetime
    now = datetime.now()
    print(main())
    print(datetime.now() - now)
