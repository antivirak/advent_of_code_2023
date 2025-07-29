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

    locations: set[tuple[int, int]] = set()
    new = get_adjacent(idx)
    print(main_alg(new, locations))
    # idx calculation not needed, the row and col of S is without obstacles
    # maybe will be needed of next fields
    locations = set()
    # idx = find_start_left(new, locations)
    idx = tuple([0, len_y // 2])
    new = get_adjacent(idx)
    print(main_alg(new, locations))
    locations = set()
    # idx = find_start_right(new, locations)
    idx = tuple([len_x // 2, 0])
    new = get_adjacent(idx)
    print(main_alg(new, locations))
    locations = set()
    # idx = find_start_up(new, locations)
    idx = tuple([len_x, len_y // 2])
    new = get_adjacent(idx)
    print(main_alg(new, locations))
    locations = set()
    # idx = find_start_down(new, locations)
    idx = tuple([len_x // 2, len_y])
    new = get_adjacent(idx)
    oscilation, steps_num = main_alg(new, locations)
    print(oscilation, steps_num)
    # print((STEPS - len_x // 2) % len_x + 1 - 4)  # number of filled boards, that oscilate between 2 numbers (hopefully in-synch)
    num_layers = (STEPS - len_x // 2) // len_x + 1  # - 4
    reminder = (STEPS - len_x // 2) % len_x
    result = 1
    for layer in range(1, num_layers):
        result += 4 * layer
    result *= oscilation[1]  # + the steps on incomplete boards, so the answer is between this and this + oscilation[] * 4
    print(result)
    upper_bound = result + oscilation[1] * 4 * num_layers
    print(upper_bound)
    # Now add the incomplete boards
    # start with bruteforcing
    # TODO now we will also need to calculate the possibility when the start is at 2 edges at once (for 3rd and later layer of boards)
    # well, instead of 2 strats, the start is in the corner
    # but in that case we still need, now 3 starts, but the 2 former delayed
    # TODO the boards have intezmezzo phases of "square" instead of diamond shape (there will be missing ONLY 4 boards: top, bottom, left, right)
    # start with intermezzo only
    # (num_layers - 1) will be the same. Iterate only in range(4) and then multiply the result by (num_layers - 1)
    to_add = 0
    for idx in (
        tuple([0, 0]),
        tuple([0, len_y]),
        tuple([len_x, 0]),
        tuple([len_x, len_y]),
    ):
        # this is main_alg for 2 starts
        # locations1 = set()
        # locations2 = set()
        # new1 = get_adjacent(idx[0])
        # new2 = get_adjacent(idx[1])
        # for _ in range(reminder):
        #     for item in locations1:
        #         new1.update(get_adjacent(item))
        #     for item in locations2:
        #         new2.update(get_adjacent(item))
        #     locations2 = new2
        #     locations1 = new1
        #     new1 = set()
        #     new2 = set()
        # to_add += len(locations1.union(locations2))
        # now from corner, correctly
        locations = set()
        new = get_adjacent(idx)
        for _ in range(reminder):
            for item in locations:
                new.update(get_adjacent(item))
            locations = new
            new = set()
        to_add += len(locations)
    to_add *= (max(num_layers - 1, 1))  # 1 is lower bound

    total = result + to_add
    if total > upper_bound:
        raise ValueError(f'{total} Too high')

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
