"""
20737
"""

from seven import get_score


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        lines = f_in.readlines()

    copy_next = {}
    for count, line in enumerate(lines):
        intersect_len = get_score(line)

        if count == 0:  # store the first card
            copy_next[0] = 1 + intersect_len

        for win in range(1, intersect_len + 1):
            idx = win + count
            copy_next[idx] = copy_next.get(idx, 1) + copy_next.get(count, 1)

    return sum(copy_next.values())


if __name__ == '__main__':
    print(main())
