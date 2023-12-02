"""
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?
"""

from one import find_first_num

NUMBERS = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}


def deal_with_spelled_nums(line: str) -> str:
    """Return edited string without spelled nums"""
    # beware, eightwo4 -> 84, not 24
    # beware, eightwo -> 82, not 88 - not covered by examples
    for num, num_int in NUMBERS.items():
        # eight -> e8t - do not replace chars that could overlap
        line = line.replace(num, f'{num[0]}{num_int}{num[-1]}')

    return line


def main() -> int:
    """main"""
    final_sum = 0
    with open('input.txt', 'r') as f_in:
        lines = f_in.readlines()
    for line in lines:
        line = deal_with_spelled_nums(line)
        # Fallback to implementation one
        first = find_first_num(line)
        last = find_first_num(reversed(line))
        final_sum += int(f'{first}{last}')

    return final_sum


if __name__ == '__main__':
    print(main())
