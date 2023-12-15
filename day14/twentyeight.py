from typing import Dict

import numpy as np
import pandas as pd

from twentyseven import calc_load, north_gravity

MAX_CYCLE = 1_000_000_000


def full_spin(platform: pd.DataFrame) -> pd.DataFrame:
    """Rotate the platform 360 degrees"""
    for _ in range(4):
        north_gravity(platform)
        platform = pd.DataFrame(np.rot90(platform, 1, axes=(1, 0)))

    return platform


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        input_file = f_in.read()
    platform = pd.DataFrame(list(iter(row)) for row in input_file.splitlines())

    platform_hashes: Dict[tuple, int] = {}
    cycle_len = 0
    for count in range(MAX_CYCLE):
        platform = full_spin(platform)
        hash_ = tuple(pd.util.hash_pandas_object(platform).to_list())
        if hash_ in platform_hashes:
            cycle_len = count - platform_hashes[hash_]
            break
        platform_hashes[hash_] = count

    # TODO I could just do the math here, but I'm lazy, so I iterate again
    if cycle_len:
        for _ in range((MAX_CYCLE - count - 1) % cycle_len):
            full_spin(platform)

    return calc_load(platform)


if __name__ == '__main__':
    print(main())
