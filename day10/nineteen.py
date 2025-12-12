"""
29569
"""

import numpy as np
import pandas as pd

START_SYMBOL = 'S'
SYMBOLS = {
    'L': [np.array((1, 0)), np.array((0, -1))],
    '7': [np.array((0, 1)), np.array((-1, 0))],
    'F': [np.array((0, 1)), np.array((1, 0))],
    'J': [np.array((0, -1)), np.array((-1, 0))],
    '-': [np.array((1, 0)), np.array((-1, 0))],
    '|': [np.array((0, 1)), np.array((0, -1))],
}


def update_current_index(
    symbol_idx: list[np.ndarray], prev_increment: np.ndarray, idx: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """update_current_index"""
    for count, index in enumerate(symbol_idx):
        if all(index + prev_increment == 0):
            # equivalent to [np.array(a), np.array(b)].index(np.array(b))
            # comparing np arrays: if (array1 == array2).all():
            prev_increment = symbol_idx[1 - count]
            idx += prev_increment
            return idx, prev_increment

    raise ValueError('Symbol index not found')


def path_length_to_furtherst() -> tuple[int, list[tuple[int, int]], pd.DataFrame]:
    """Return path length to the furthest point and objects needed for part2"""
    sketch = pd.DataFrame(list(iter(row[1][0])) for row in pd.read_csv(
        'input.txt', dtype=str, header=None,
    ).iterrows())

    path_vertices = []
    # start symbol index in sketch
    idx = np.array(list(reversed([index[0] for index in np.where(sketch == START_SYMBOL)])))
    break_outer = False
    for increment in (
        np.array([1, 0]), np.array([-1, 0]), np.array([0, 1]), np.array([0, -1]),
    ):
        symbol_idx = SYMBOLS.get(sketch.loc[idx[1] + increment[1], idx[0] + increment[0]])
        if not symbol_idx:  # START_SYMBOL on the edge of sketch
            continue
        for index in symbol_idx:
            if all(index + increment == 0):
                prev_increment = increment
                idx += increment
                path_vertices.append(tuple(idx.tolist()))
                break_outer = True
                break
        if break_outer:
            break  # from start lead 2 paths, choose one

    total = 0
    while True:
        symbol_idx = SYMBOLS.get(sketch.loc[idx[1], idx[0]])
        idx, prev_increment = update_current_index(symbol_idx, prev_increment, idx)
        path_vertices.append(tuple(idx.tolist()))
        total += 1
        if sketch.loc[idx[1], idx[0]] == START_SYMBOL:
            break  # loop closed

    return total // 2 + 1, path_vertices, sketch  # the furthest point is the middle of the loop


def main() -> int:
    """main"""
    total, *_ = path_length_to_furtherst()
    return total


if __name__ == '__main__':
    print(main())
