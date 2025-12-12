"""
6148
"""

from typing import List

from shapely import Polygon


def append_vertex(path_vertices: list, idx: list, direction: str, length: int) -> None:
    """Append x-y coordinates to path_vertices and update them for next step"""
    if direction == 'U':
        idx[0] -= length
        path_vertices.append(idx.copy())
    elif direction == 'D':
        idx[0] += length
        path_vertices.append(idx.copy())
    elif direction == 'R':
        idx[1] += length
        path_vertices.append(idx.copy())
    elif direction == 'L':
        idx[1] -= length
        path_vertices.append(idx.copy())
    else:
        raise ValueError('Unknown direction')


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        plan = [line.strip() for line in f_in.read().splitlines()]

    len_plan = len(plan)
    # layout = np.zeros((len_plan, len_plan), dtype=bool)

    idx = [int(len_plan // 2.7), int(len_plan // 2.7)]  # 2.7 ad-hoc constant
    # layout[*idx] = True
    path_vertices: List[tuple] = []
    total = 0
    for instruction in plan:
        direction, length_str, _ = instruction.split()
        length = int(length_str)
        total += length
        append_vertex(path_vertices, idx, direction, length)

    # Compute filled area. Yes, I could have implemented bucket fill / shoelace, but this is python
    layout_poly = Polygon(path_vertices)
    return int(layout_poly.area) + total // 2 + 1


if __name__ == '__main__':
    print(main())
