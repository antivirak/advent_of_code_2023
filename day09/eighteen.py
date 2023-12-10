import numpy as np


def main() -> int:
    """main"""
    matrix = np.loadtxt('input.txt', dtype=int)

    total = 0
    for row in matrix:
        placeholder_increments = [row[0]]
        while not all(item == 0 for item in row):
            row = np.diff(row)
            placeholder_increments.append(row[0])

        decrement = 0
        for item in reversed(placeholder_increments[:-1]):
            decrement = item - decrement
        total += decrement

    return total


if __name__ == '__main__':
    print(main())
