"""
18458
"""

from functools import lru_cache
from itertools import cycle
from typing import Iterable, Mapping


class MappingCounter:
    """Store unhashable parameters in class attributes and implement main method with lru_cache"""
    def __init__(self, input_map: Mapping, instructions: Iterable, end_condition: str) -> None:
        self.input_map = input_map
        self.instructions = instructions
        self.end_condition = end_condition

    @lru_cache()
    def path_len(self, item: str) -> int:
        """Return number of steps needed to exit"""
        for count, instruction in enumerate(self.instructions, start=1):
            item = self.input_map[item][instruction]
            if item.endswith(self.end_condition):
                return count
        return 0


def get_input_map(lines: Iterable) -> dict:
    """Fancy one-liner, could be more readable"""
    return {
        line.split(' = ')[0]: dict(zip(
            ('L', 'R'),
            line.split(' = ')[1].lstrip('(').rstrip(')\n').split(', '),
        )) for line in lines
    }


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        lines = f_in.readlines()

    instructions = cycle(lines[0].strip('\n'))
    input_map = get_input_map(lines[2:])

    return MappingCounter(input_map, instructions, 'ZZZ').path_len('AAA')


if __name__ == '__main__':
    print(main())
