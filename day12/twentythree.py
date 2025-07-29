"""
--- 
"""

from more_itertools import distinct_permutations

SPACE = '.'
FILL = '#'
DOF = '?'  # degree of freedom


# @lru_cache()
def check(to_add: str, nums: list) -> bool:
    filled_space = to_add.replace(SPACE, ' ').split()
    if len(filled_space) != len(nums):
        return False
    for num, filled in zip(nums, filled_space):
        if len(filled) != num:
            return False

    return True


def main() -> int:
    """main"""
    with open('input.txt') as f_in:
        lines = f_in.read().splitlines()

    total = 0
    for line in lines:
        if DOF not in line:
            total += 1
            continue
        field, nums = [item.strip() for item in line.split(' ')]
        # TODO pokud je jen jedna platna variace pro neprodlouzeny input, bude asi jen jedna i pro prodlouzeny
        # TODO "smart brute force" => dynamic programming
        # nums = tuple([int(num) for num in nums.split(',')] * 5)
        nums = tuple([int(num) for num in nums.split(',')])
        # field = '?'.join([field] * 5)
        dof = field.count(DOF)
        # print(dof)
        fill = field.count(FILL)
        sum_nums = sum(nums)
        variations = distinct_permutations(''.join([SPACE * (dof - sum_nums + fill), FILL * (sum_nums - fill)]))
        # print(SPACE * (dof - sum_nums + fill))
        # print(FILL * (sum_nums - fill))
        for count, variation in enumerate(variations):
            variation = iter(variation)
            # assert len(list(variation)) == dof
            to_add = ''.join(next(variation) if item == DOF else item for item in field)
            # for item in field:
            #     if item == DOF:
            #         # TODO This creates new string every time. Could be faster with list
            #         to_add += next(variation)
            #     else:
            #         to_add += item
            if check(to_add, nums):
                total += 1
            # if total + 1 % 10 == 0:
            #     print(total)
            # if count % 1000 == 0:
            #     print(count, total)
        # input('line finished')

    return total


if __name__ == '__main__':
    print(main())
