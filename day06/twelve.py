"""
22116
"""

from elf import num_ways_multiplied


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        lines = f_in.readlines()

    input_map = {}
    for key, line in zip(('time', 'distance'), lines):
        input_map[key] = [int(''.join(line.split(':')[1].split()))]

    return num_ways_multiplied(input_map)


if __name__ == '__main__':
    print(main())
