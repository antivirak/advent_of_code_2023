"""
21552
"""

from three import COLORS, get_colored_number


def main() -> int:
    """main"""
    final_sum = 0
    with open('input.txt', 'r') as f_in:
        lines = f_in.readlines()
    for line in lines:
        line = line.rstrip('\n')
        draws = line.split(';')
        game_power = 0  # reset game power for new line
        _, draws[0] = draws[0].split(':')  # get rid of game ID
        color_to_cubes = {color: [] for color in COLORS}
        for draw in draws:
            cubes = draw.split(',')
            for color in COLORS:
                color_to_cubes[color].append(get_colored_number(cubes, color))
        for color in COLORS:
            colored_max = max(color_to_cubes[color])
            game_power = game_power * colored_max or colored_max
        final_sum += game_power

    return final_sum


if __name__ == '__main__':
    print(main())
