"""
23016
"""

import numpy as np
import pandas as pd

ROCK = 'O'
EMPTY = '.'


def north_gravity(platform: pd.DataFrame) -> None:
    """Move all rocks north as far as they will go"""
    _, len_y = platform.shape
    for count in range(len_y):
        row = platform.iloc[count, :]
        if not count:
            continue
        idxs = np.where(row == ROCK)[0]
        for idx in idxs:
            inner_count = count - 1
            while inner_count > -1:
                if platform.iloc[inner_count, idx] != EMPTY:
                    break
                platform.iat[inner_count, idx] = ROCK
                platform.iat[inner_count + 1, idx] = EMPTY
                inner_count -= 1


def calc_load(platform: pd.DataFrame) -> int:
    """Calculate the total load on the north support beams"""
    total = 0
    _, len_y = platform.shape
    for count, row in reversed(tuple(platform.iterrows())):
        total += len(np.where(row == ROCK)[0]) * (len_y - count)

    return total


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        input_file = f_in.read()  # .split('\n\n')
    # platforms = [pd.DataFrame(list(iter(row)) for row in matrix.splitlines()) for matrix in input_file]
    platform = pd.DataFrame(list(iter(row)) for row in input_file.splitlines())

    north_gravity(platform)

    # with open('validate_turn.txt', 'r') as f_in:
    #     test_file = f_in.read()
    # platform_check = pd.DataFrame(list(iter(row)) for row in test_file.splitlines())
    # assert (platform == platform_check).all().all()

    return calc_load(platform)


if __name__ == '__main__':
    print(main())
