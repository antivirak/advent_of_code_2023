"""
29644
"""

from nine import get_input_map, get_transformed_map


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        lines = f_in.readlines()

    seed_ranges = []
    seed_range_bounds = [int(num) for num in lines[0].split()[1:]]
    for start, length in zip(seed_range_bounds[::2], seed_range_bounds[1::2]):
        seed_ranges.append(range(start, start + length))

    input_map = get_input_map(lines[2:])
    transformed_map, reversed_map = get_transformed_map(input_map)

    # Start from the end (sorted locations) and go backwards
    lines = transformed_map['humidity'].get('lines')
    # Add range from 0 to the lowest range bound
    lowest_start = min(line[0][0] for line in lines)
    if lowest_start > 0:
        lines.append([range(0, lowest_start), range(0, lowest_start)])
    count = 0  # for counting iterations only
    for location_range, humidity_range in sorted(lines, key=lambda line: line[0][0]):
        for location, humidity in zip(location_range, humidity_range):
            #
            count += 1
            if count % 100_000 == 0:
                print(count)
            #
            key = 'temperature'
            while key:  # reversed_map.get('seed') = None
                # iteratively transform humidity to seed
                for line in transformed_map[key]['lines']:
                    if humidity in line[0]:
                        idx = line[0].index(humidity)
                        humidity = line[1][idx]
                        break
                key = reversed_map.get(key)

            if any(humidity in seed_range for seed_range in seed_ranges):
                return location

    raise ValueError('No seed')


if __name__ == '__main__':
    print(main())
