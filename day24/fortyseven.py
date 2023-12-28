"""
--- 
"""

import numpy as np

POS_BOUNDS = [7, 27]
POS_BOUNDS = [200_000_000_000_000, 400_000_000_000_000]  # closed interval


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        vectors = f_in.readlines()

    pos = []
    vel = []
    for vector in vectors:
        pos_str, vel_str = vector.strip().split(' @ ')
        pos.append(list(map(int, pos_str.split(', '))))
        vel.append(list(map(int, vel_str.split(', '))))

    total = 0
    # TODO vectorize
    for idx, (pos1, vel1) in enumerate(zip(pos, vel), start=1):
        for pos2, vel2 in zip(pos[idx:], vel[idx:]):
            slope1, intercept1 = np.polyfit(
                [pos1[0], pos1[0] + vel1[0]],
                [pos1[1], pos1[1] + vel1[1]], 1,
            )
            slope2, intercept2 = np.polyfit(
                [pos2[0], pos2[0] + vel2[0]],
                [pos2[1], pos2[1] + vel2[1]], 1,
            )
            if slope1 == slope2:
                if intercept1 == intercept2:
                    total += 1  # identical lines, they "cross" everywhere
                continue  # parallel lines
            x = (intercept2 - intercept1) / (slope1 - slope2)
            y = slope1 * x + intercept1
            # print(x, y)
            if POS_BOUNDS[0] <= x <= POS_BOUNDS[1] and POS_BOUNDS[0] <= y <= POS_BOUNDS[1]:
                if (x >= pos1[0] and vel1[0] >= 0) or (x <= pos1[0] and vel1[0] <= 0):
                    if (y >= pos1[1] and vel1[1] >= 0) or (y <= pos1[1] and vel1[1] <= 0):
                        if (x >= pos2[0] and vel2[0] >= 0) or (x <= pos2[0] and vel2[0] <= 0):
                            if (y >= pos2[1] and vel2[1] >= 0) or (y <= pos2[1] and vel2[1] <= 0):
                                total += 1
                                # print(True, vel1, vel2, pos1, pos2)

    return total


if __name__ == '__main__':
    print(main())
