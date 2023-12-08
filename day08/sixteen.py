from itertools import cycle
from math import lcm

from fifteen import MappingCounter, get_input_map


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        lines = f_in.readlines()

    instructions = cycle(lines[0].strip('\n'))
    input_map = get_input_map(lines[2:])

    # return least common multiple of all paths lengths
    # generally could be solved by CRT, but that would take long time
    counter = MappingCounter(input_map, instructions, 'Z')
    return lcm(*[counter.path_len(item)
                 for item in input_map.keys() if item.endswith('A')])


if __name__ == '__main__':
    print(main())
