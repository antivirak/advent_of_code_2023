"""
28355
"""


def hash_alg(char_group: str) -> int:
    """Run the HASH algorithm on a string"""
    current = 0
    for char in char_group:
        current += ord(char)
        current = (current * 17) % 256

    return current


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        return sum(map(hash_alg, f_in.read().strip().split(',')))


if __name__ == '__main__':
    print(main())
