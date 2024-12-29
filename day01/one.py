"""
https://adventofcode.com/2023/day/1
28359
"""

from typing import Iterable


def find_first_num(line: Iterable[str]) -> int:
    """Return first int in iterable"""
    for char in line:
        try:
            int_val = int(char)
        except (ValueError, TypeError):  # TODO exception-driven logic
            continue
        return int_val

    return -1


def main() -> int:
    """main"""
    final_sum = 0
    with open('input.txt', 'r') as f_in:
        lines = f_in.readlines()
    for line in lines:
        first = find_first_num(line)
        last = find_first_num(reversed(line))
        final_sum += int(f'{first}{last}')

    return final_sum


if __name__ == '__main__':
    print(main())  # 53651
