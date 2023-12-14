from itertools import product

import numpy as np
from matplotlib import path

from nineteen import path_length_to_furtherst


def main() -> int:
    """main"""
    _, path_vertices, sketch = path_length_to_furtherst()

    total = 0
    poly = path.Path(np.asarray(path_vertices), closed=True)
    path_vertices = set(path_vertices)  # for fast lookup
    len_x, len_y = sketch.shape
    for x_id, y_id in product(range(len_x), range(len_y)):
        idx = tuple((y_id, x_id))
        if idx in path_vertices:
            continue
        if poly.contains_point(idx):
            total += 1

    return total


if __name__ == '__main__':
    print(main())
