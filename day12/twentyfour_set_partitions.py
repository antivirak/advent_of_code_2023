from functools import lru_cache, cache

# from more_itertools import set_partitions

SPACE = '.'
FILL = '#'
DOF = '?'  # degree of freedom


@cache
def set_partitions(iterable, k):
    """
    Yield the set partitions of *iterable* into *k* parts. Set partitions are
    not order-preserving.

    >>> iterable = 'abc'
    >>> for part in set_partitions(iterable, 2):
    ...     print([''.join(p) for p in part])
    ['a', 'bc']
    ['ab', 'c']
    ['b', 'ac']
    """
    L = tuple(iterable)
    n = len(L)
    if k < 1:
        raise ValueError(
            "Can't partition in a negative or zero number of groups"
        )
    if k > n:
        return

    @cache
    def set_partitions_helper(L, k):
        n = len(L)
        if k == 1:
            yield tuple([L])
        elif n == k:
            yield tuple(tuple([s]) for s in L)
        else:
            e, *M = L
            for p in set_partitions_helper(tuple(M), k - 1):
                yield tuple([tuple([e]), *p])
            for p in set_partitions_helper(tuple(M), k):
                for i in range(len(p)):
                    yield tuple(p[:i]) + tuple([tuple([e]) + p[i]]) + tuple(p[i + 1:])

    yield from set_partitions_helper(L, k)


# @lru_cache()
# def get_arrangements(spaces: int, nums: tuple) -> set:
#     arrangements = set()
#     for count, num in enumerate(nums):
#         if count == 0:
#             arrangements.add((SPACE * (spaces - num), FILL * num))
#         elif count == len(nums) - 1:
#             arrangements.add((FILL * num, SPACE * (spaces - num)))
#         else:
#             arrangements.add((FILL * num, SPACE * (spaces - num), FILL * num))
# 
#     return arrangements


@cache
def _set_partitions(spaces: int, len_nums: int) -> set:
    return set(tuple(''.join(p) for p in part) for part in set_partitions(SPACE * spaces, len_nums))


@cache
def get_arrangements(spaces: int, len_nums: int) -> set:
    """kolikrat poskladat tecky do mezer pred, za a mezi bloky (len(nums) + 1)"""
    # arrangements0 = set(tuple(''.join(p) for p in part)            for part in set_partitions(SPACE * spaces, len_nums))
    # arrangements =  set(tuple(''.join(p) for p in part)            for part in set_partitions(SPACE * spaces, len_nums + 1))
    # arrangements.update(tuple(''.join(p) for p in [[], *part, []]) for part in set_partitions(SPACE * spaces, len_nums - 1))
    # arrangements.update(tuple(('', *arr)) for arr in arrangements0)
    # arrangements.update(tuple((*arr, '')) for arr in arrangements0)

    arrangements =                                       _set_partitions(spaces, len_nums + 1)
    intermed = set(tuple(('', *arr, '')) for arr in _set_partitions(spaces, len_nums - 1) if arr[0] and arr[-1])
    arrangements.update(intermed)  # needs to be in 2 steps
    intermed = set(tuple(('', *arr))     for arr in _set_partitions(spaces, len_nums) if arr[0])
    arrangements.update(intermed)#  tuple(('', *arr))     for arr in _set_partitions(spaces, len_nums))
    intermed = set(tuple((*arr, ''))     for arr in _set_partitions(spaces, len_nums) if arr[-1])
    arrangements.update(intermed)#tuple((*arr, ''))     for arr in _set_partitions(spaces, len_nums))

    return arrangements


@lru_cache()
def check(to_add: str, field: str) -> bool:
    for item1, item2 in zip(to_add, field):
        if (item1 == SPACE and item2 == FILL) or (item1 == FILL and item2 == SPACE):
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
        # TODO "smart brute force" => dynamic programming
        nums = tuple([int(num) for num in nums.split(',')] * 5)
        # nums = tuple([int(num) for num in nums.split(',')])
        field = '?'.join([field] * 5)
        sum_nums = sum(nums)
        len_nums = len(nums)
        spaces = len(field) - sum_nums
        arrangements = get_arrangements(spaces, len_nums)
        # print(arrangements)
        if len(arrangements) == 1:
            total += 1
            continue
        # those commented out are all possibilities of separate ? blocks replacements. In reality still brute force.
        # variations = [product([SPACE, FILL], repeat=block.count(DOF)) for block in field.replace(SPACE, ' ').split()]
        # for variation in arrangements:
        #     print([list(var) for var in variation])
        #     raise
        for count, variation in enumerate(arrangements):
            variation = iter(variation)
            to_add = next(variation)
            for num in nums:
                to_add += FILL * num + next(variation)
            if check(to_add, field):
                total += 1
            if count % 10000 == 0:
                print(count, total)
        print('line finish')
        # input(total)

    return total


if __name__ == '__main__':
    print(main())
