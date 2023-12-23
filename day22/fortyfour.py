import numpy as np

from fortythree import create_space, gravity


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        brick_indices = f_in.readlines()

    space, bricks_ = create_space(brick_indices)
    space = gravity(space, bricks_)
    # len_z_half = space.shape[2] // 2
    # print(space[:, 0, :len_z_half])
    # print()
    # print(space[:, 1, :len_z_half])
    # print()
    # print(space[:, 2, :len_z_half])

    support = {}  # brick -> set of bricks, that support it
    to_reiterate = []
    bricks_to_impact = 0
    for z_idx, prev in zip(reversed(range(space.shape[2] - 1)), reversed(range(1, space.shape[2]))):
        prev_slice = space[:, :, prev]
        slice_ = space[:, :, z_idx]
        # all bricks, that could support some in prev_slice
        for prev_brick in set(prev_slice.flatten()) - {0}:
            idx = np.where(prev_slice == prev_brick)
            bricks = set(slice_[idx].flatten()) - {0, prev_brick}
            len_bricks = len(bricks)
            support[prev_brick] = bricks
            if len_bricks == 1:
                # print(bricks)
                bricks_to_impact += 1
                # break
            #     support[prev_brick] = bricks
            if len_bricks > 1:
                to_reiterate.append([prev_brick, prev_slice, slice_, idx])

    # print(bricks_to_impact)
    for prev_brick, prev_slice, slice_, idx in reversed(to_reiterate):
        idx = np.where(prev_slice == prev_brick)
        bricks = set(slice_[idx].flatten()) - {0, prev_brick}
        real_support = set().union(*(support.get(brick, set()) for brick in bricks))
        # print(real_support)
        if len(real_support) == 1:
            support[prev_brick] = real_support
            bricks_to_impact += 1 + sum(val == {prev_brick} for val in support.values())
            # if {prev_brick} in support.values():  # if already counted, count it again
            #     # this is good direction, but we'll need to multiply by number of supporting again
            #     bricks_to_impact += 1

    print(support)
    return bricks_to_impact


if __name__ == '__main__':
    print(main())
