"""
46521
"""

from typing import Iterable


def get_input_map(lines: Iterable) -> dict:
    """get_input_map"""
    input_map = {}
    ints = set(str(num) for num in range(10))
    for line in lines:
        if not line.strip():
            continue
        if line[0] not in ints:
            current_map = line.split()[0]
            input_map[current_map] = []
            continue
        input_map[current_map].append([int(num) for num in line.split()])

    return input_map


def get_transformed_map(input_map: dict) -> tuple:
    transformed_map = {}
    reversed_map = {}
    for key, val in input_map.items():
        from_, to_ = key.split('-to-')
        transformed_map[from_] = {'to': to_, 'lines': []}
        reversed_map[to_] = from_
        for line in val:
            start1, start2, length = line
            transformed_map[from_]['lines'].append([
                range(start1, start1 + length), range(start2, start2 + length),
            ])

    return transformed_map, reversed_map


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        lines = f_in.readlines()

    locations = []
    seeds = [int(num) for num in lines[0].split()[1:]]
    input_map = get_input_map(lines[2:])
    transformed_map, _ = get_transformed_map(input_map)

    for seed in seeds:
        key = 'seed'
        while key != 'location':
            # iteratively transform seed to location
            inner_key = transformed_map.get(key).get('to')
            for line in transformed_map[key]['lines']:
                if seed in line[1]:
                    idx = line[1].index(seed)
                    seed = line[0][idx]
                    break
            key = inner_key
        locations.append(seed)

    return min(locations)


if __name__ == '__main__':
    print(main())
