from functools import cache
from itertools import product

from fortyone import ROCK, START

# TODO revert to bruteforce and commit
# btw there is no obstacle on row and column of S. It should be possible to do my way

STEPS = 50
"""
For oscillation[0] the 500 fails, so I assume that we use the lower (oscillation[1]) value
   6:      36 (     44,     220)  # too low to be correct, do not care, edge case
  10:      90 (     44,     220)  # too low for the (brute) correction, also edge case
  50:   1_940 (  1_804,   2_684)  # got 1_932, because I only caunt the intermezzo
 100:   7_645 (  6_380,   7_964)  # getting too high, there is an error in my alg
 500: 188_756 (182_204, 190_300)  # takes 1 min already
1000:         (720_764, 736_780)  # takes 4 min
"""

with open('test_input2.txt', 'r') as f_in:
    rows = [row.strip() for row in f_in.readlines()]
len_x = len(rows[0])
len_y = len(rows)


def four_series():
    """Generate multiples of 4"""
    num = 0
    while True:
        yield num
        num += 4


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


def find_start_right(new, locations):
    while True:
        for item in locations:
            updates = get_adjacent(item)
            for update in updates:
                if update[0] < 0:
                    return update
            new.update(updates)
        locations = new
        new = set()


def find_start_left(new, locations):
    while True:
        for item in locations:
            updates = get_adjacent(item)
            for update in updates:
                if update[0] == len_x:
                    return update
            new.update(updates)
        locations = new
        new = set()


def find_start_up(new, locations):
    while True:
        for item in locations:
            updates = get_adjacent(item)
            for update in updates:
                if update[1] < 0:
                    return update
            new.update(updates)
        locations = new
        new = set()


def find_start_down(new, locations):
    # TODO those functions are the same, just the condition is different
    while True:
        for item in locations:
            updates = get_adjacent(item)
            for update in updates:
                if update[1] == len_y:
                    return update
            new.update(updates)
        locations = new
        new = set()


def main_alg(new, locations):
    last_total = [-1, -1]
    count = 0
    while True:
        # if _ > len_x + 1:
        #     for row_count, row in enumerate(rows):
        #         locations_mod = set(item for item in locations if 0 <= item[0] < len_x and 0 <= item[1] < len_y)
        #         print(''.join([item if tuple([row_count, count]) not in locations_mod else 'O' for count, item in enumerate(row)]))
        #     print()
        total = 0
        for row_count in range(len_x):
            locations_mod = set(item for item in locations if 0 <= item[0] < len_x and 0 <= item[1] < len_y)
            total += sum([1 if tuple([row_count, count]) in locations_mod else 0 for count in range(len_x)])
        if total == last_total[1] and total:
            return last_total, count
        last_total[1] = last_total[0]
        last_total[0] = total

        for item in locations:
            updates = get_adjacent(item)
            new.update(updates)
        locations = new
        new = set()
        count += 1


def main() -> int:
    """main"""
    for idx in product(range(len_x), range(len_y)):
        if rows[idx[0]][idx[1]] == START:
            break
    else:
        raise ValueError('No starting point found')

    # The problem can be solved mathematically by formula:
    # o*(n-1)**2 + e*n**2 + a*(n-1) + b*n + t = 0
    # a = 

    # new = get_adjacent(idx)
    # print(_(new, locations))

    # for row_count, row in enumerate(rows):
    #     print(''.join([item if tuple([row_count, count]) not in locations else 'O' for count, item in enumerate(row)]))

    return total


if __name__ == '__main__':
    from datetime import datetime
    now = datetime.now()
    print(main())
    print(datetime.now() - now)
