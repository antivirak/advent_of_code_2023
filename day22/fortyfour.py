import numpy as np

from fortythree import create_space, gravity


def main() -> int:
    """main"""
    with open('test_input.txt', 'r') as f_in:
        brick_indices = f_in.readlines()

    space, bricks_ = create_space(brick_indices)
    space = gravity(space, bricks_)
    print(space[:, 0, :])
    print()
    print(space[:, 1, :])
    print()
    print(space[:, 2, :])

    bricks_to_impact = {}
    for z_idx, prev in zip(reversed(range(space.shape[2] - 1)), reversed(range(1, space.shape[2]))):
        prev_slice = space[:, :, prev]
        slice_ = space[:, :, z_idx]
        # all bricks, that could support some in prev_slice
        for prev_brick in set(prev_slice.flatten()) - {0}:
            idx = np.where(prev_slice == prev_brick)
            bricks = set(slice_[idx].flatten()) - {0, prev_brick}
            len_bricks = len(bricks)
            if len_bricks == 1:
                brick = next(iter(bricks))
                to_add = bricks_to_impact.get(brick, [0, set()])[1]
                to_add.add(prev_brick)
                bricks_to_impact[brick] = [
                    bricks_to_impact.get(brick, [0])[0] + 1,
                    to_add,
                ]
            elif len_bricks > 1:
                print([bricks_to_impact.get(brick, [0, set()])[1] for brick in bricks])
                # if len(set().union(*(bricks_to_impact.get(brick, [0, set()])[1] for brick in bricks))) == 1:
                if len(bricks_to_impact.get(prev_brick, [0, set()])[1]) == 1:
                    for brick in bricks:
                        to_add = bricks_to_impact.get(brick, [0, set()])[1]
                        to_add.add(prev_brick),
                        bricks_to_impact[brick] = [
                            bricks_to_impact.get(brick, [0])[0] + 1,
                            to_add,
                        ]
                # else:
                #     for brick in bricks:
                #         bricks_to_impact[brick] = [
                #             0,
                #             ,
                #         ]

    print(bricks_to_impact)
    return sum(map(lambda item: item[0], bricks_to_impact.values()))


if __name__ == '__main__':
    print(main())
