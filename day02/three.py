"""
22329
"""

from typing import Iterable

COLORS = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


def get_colored_number(cubes: Iterable, color: str) -> int:  # TODO color enum
    """Return number associated with input number"""
    # cubes = cubes.lower()
    for cube in cubes:
        if color in cube:
            return int(cube.rstrip(color))

    return 0


def line_to_possible_game_id(line: str) -> int:
    """Process line and return game id if game was possible. Return 0 otherwise."""
    line = line.rstrip('\n')
    draws = line.split(';')
    game_id_unstripped, draws[0] = draws[0].split(':')
    game_id = int(game_id_unstripped.lstrip('Game'))
    color_to_cubes = {color: [] for color in COLORS}
    for draw in draws:  # draw is one subset of cubes revealed
        cubes = draw.split(',')
        for color in COLORS:
            color_to_cubes[color].append(get_colored_number(cubes, color))
    for color, threshold in COLORS.items():
        if max(color_to_cubes[color]) > threshold:
            break
    else:
        return game_id

    return 0


def main() -> int:
    """main"""
    final_sum = 0
    with open('input.txt', 'r') as f_in:
        lines = f_in.readlines()
    for line in lines:
        final_sum += line_to_possible_game_id(line)

    return final_sum


if __name__ == '__main__':
    print(main())
