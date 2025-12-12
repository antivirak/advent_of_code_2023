"""
30644
"""

import pandas as pd


def find_reflection(matrix: pd.DataFrame, len_y: int) -> int:
    """Return number of rows above the mirror plane"""
    to_add = 0
    for count in range(len_y):
        idx = 0
        cond = True
        while cond:
            upper_row_index = count - 1 - idx
            if upper_row_index < 0 or count + idx + 1 > len_y:
                to_add += count
                break
            cond = (matrix.iloc[:, count + idx] == matrix.iloc[:, upper_row_index]).all()
            idx += 1

    return to_add


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        input_file = f_in.read().split('\n\n')
    maze = [pd.DataFrame(list(iter(row)) for row in matrix.splitlines()) for matrix in input_file]

    total = 0
    for matrix in maze:
        len_x, len_y = matrix.shape
        # cols first
        to_add = find_reflection(matrix, len_y)
        if not to_add:
            to_add = find_reflection(matrix.T, len_x)
            to_add *= 100
        total += to_add

    return total


if __name__ == '__main__':
    print(main())
