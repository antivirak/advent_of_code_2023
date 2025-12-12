"""
19193
"""


def get_score(line: str) -> int:
    """get score"""
    line = line.split(':')[1].strip()
    winning, scratched = line.split('|')
    winning = set((num for num in winning.split()))
    scratched = set((num for num in scratched.split()))

    return len(winning.intersection(scratched))


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        lines = f_in.readlines()

    total = 0
    for line in lines:
        intersect_len = get_score(line)
        if intersect_len > 0:
            total += 2 ** (intersect_len - 1)

    return total


if __name__ == '__main__':
    print(main())
