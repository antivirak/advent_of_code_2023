"""
12709
"""

import numpy as np
import pandas as pd

GALAXY = '#'


def expand_universe(space_map: pd.DataFrame, increment: int) -> pd.DataFrame:
    """Add int(increment)-filled row and col next to every empty row and col"""
    df = space_map.copy()
    length = len(df.columns)
    to_expand = []
    for idx, col in df.items():
        if all(col == '.'):
            to_expand.append(idx)

    for count, idx in enumerate(reversed(to_expand)):  # reversed, because the index increments
        # increment index
        for col_name in reversed(range(idx, length + count)):
            df = df.rename(columns={col_name: col_name + 1})
        # insert col
        df[idx] = [increment] * length
    length += len(to_expand)
    df = df.reindex(columns=range(length))

    # the same for rows
    to_expand = []
    for idx, row in space_map.iterrows():
        if all(row == '.'):
            to_expand.append(idx)

    space_map = df.copy()
    for idx in reversed(to_expand):
        line = pd.DataFrame(dict(zip(range(length), [increment] * length)), index=[idx])
        space_map = pd.concat([space_map.iloc[:idx], line, space_map.iloc[idx:]]).reset_index(drop=True)

    return space_map


def main() -> int:
    """main"""
    space_map = pd.DataFrame(list(iter(row[1][0])) for row in pd.read_csv(
        'input.txt', dtype=str, header=None,
    ).iterrows())

    space_map = expand_universe(space_map, 1)
    # verify_map = pd.DataFrame(list(iter(row[1][0])) for row in pd.read_csv(
    #     'verify_expansion.txt', dtype=str, header=None,
    # ).iterrows())
    # for idx, row in space_map.iterrows():
    #     assert (row == verify_map.iloc[idx]).all()
    galaxies = np.where(space_map == GALAXY)
    indices = list(zip(*galaxies))
    total = 0
    for count, (row, col) in enumerate(indices):
        for inner_row, inner_col in indices[count + 1:]:
            # vector norm in discrete squared space
            total += abs(row - inner_row) + abs(col - inner_col)

    return total


if __name__ == '__main__':
    print(main())
