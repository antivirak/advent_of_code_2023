from typing import List

from shapely import Polygon

from thirtyfive import append_vertex

DIRECTION_MAP = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U',
}


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        plan = [line.strip().rstrip(')') for line in f_in.read().splitlines()]

    len_plan = len(plan)

    idx = [int(len_plan // 2.7), int(len_plan // 2.7)]
    path_vertices: List[tuple] = []
    total = 0
    for instruction in plan:
        rgb = instruction.split()[2]
        direction = DIRECTION_MAP[rgb[-1]]
        length = int(rgb[2:-1], 16)  # get rid of leading '(#'
        total += length
        append_vertex(path_vertices, idx, direction, length)

    # Compute filled area.
    layout_poly = Polygon(path_vertices)
    return int(layout_poly.area) + total // 2 + 1


if __name__ == '__main__':
    print(main())
