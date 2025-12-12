"""
23134
"""

from math import floor
from typing import Mapping

import numpy as np


def num_ways_multiplied(input_map: Mapping) -> int:
    product = 1
    for tim, dist in zip(input_map['time'], input_map['distance']):
        # quadratic eq: speed1,2 = sort((tim +- (tim ** 2 - 4 * dist) ** .5) / 2)
        max_speed, best_elf_speed = (floor(root) for root in np.roots([1, -tim, dist]))
        while max_speed * (tim - max_speed) <= dist:
            max_speed -= 1  # correction to consider the boundary

        product *= max_speed - best_elf_speed

    return product


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        lines = f_in.readlines()

    input_map = {}
    for key, line in zip(('time', 'distance'), lines):
        input_map[key] = [int(num) for num in line.split(':')[1].split()]

    return num_ways_multiplied(input_map)


if __name__ == '__main__':
    print(main())
