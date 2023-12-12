import numpy as np
import pandas as pd

from twentyone import expand_universe

GALAXY = '#'


def sum_increments(space_map: pd.DataFrame, row: int, inner_row: int, col: int) -> int:
    """Sum all integer fields along the line between two galaxies"""
    return sum(
        space_map.iloc[row_iter, col] - 1 for row_iter in range(
            *sorted([row, inner_row])
        ) if space_map.iloc[row_iter, col] not in ['.', GALAXY]
    )


def main() -> int:
    """main"""
    space_map = pd.DataFrame(list(iter(row[1][0])) for row in pd.read_csv(
        'input.txt', dtype=str, header=None,
    ).iterrows())

    space_map = expand_universe(space_map, 1_000_000 - 1)
    galaxies = np.where(space_map == GALAXY)
    indices = list(zip(*galaxies))
    total = 0
    for count, (row, col) in enumerate(indices):
        for inner_row, inner_col in indices[count + 1:]:
            total += abs(row - inner_row) + abs(col - inner_col)
            # Add all expanse-crossings
            total += sum_increments(space_map, row, inner_row, col)
            total += sum_increments(space_map.T, col, inner_col, row)

    return total


if __name__ == '__main__':
    print(main())
