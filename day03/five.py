"""
33357
"""

from itertools import product
from typing import Iterable

NUMBERS = tuple(str(num) for num in range(10))
INERT_SYMBOL = '.'


def indices(lst: Iterable, element: str) -> list:
    """https://stackoverflow.com/a/18669080"""
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset + 1)
        except ValueError:
            return result  # TODO exception-driven logic
        result.append(offset)


class Matrix:
    """Perform computations on schematic"""
    def __init__(self, matrix: Iterable) -> None:
        self.matrix = matrix
        self.variations = [var for var in product([-1, 0, 1], repeat=2) if var != (0, 0)]

    def standalone(self, idx1: int, idx2: int, skip_left: bool = False) -> bool:
        """Recursively check number neighborhood. Return true if no symbol is in it."""
        res = True
        for variation in self.variations:
            if skip_left and variation == (0, -1):
                continue
            try:
                item = self.matrix[idx1 + variation[0]][idx2 + variation[1]]
            except IndexError:
                continue
            if item in NUMBERS:
                if variation == (0, 1):
                    res = self.standalone(idx1 + variation[0], idx2 + variation[1], skip_left=True)
            elif item != INERT_SYMBOL:
                return False

        return res

    def total(self, numbers_in_schema: Iterable) -> int:
        """Calculate sum of 'part numbers'"""
        total = 0
        for num in set(numbers_in_schema):
            for count, line in enumerate(self.matrix):
                # add edge cases - there are only '.', ',' and numbers in the matrix
                indexes = indices(line, INERT_SYMBOL + num + INERT_SYMBOL)
                indexes.extend(indices(line, ',' + num + INERT_SYMBOL))
                indexes.extend(indices(line, INERT_SYMBOL + num + ','))
                indexes.extend(indices(line, ',' + num + ','))
                for idx in indexes:
                    # sum numbers with at least one adjacent symbol
                    if not self.standalone(count, idx + 1):
                        total += int(num)
        return total


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        schematic = f_in.read()

    # get distinct symbols
    symbols = set()
    for char in schematic:
        if char not in (*NUMBERS, INERT_SYMBOL, '\n'):
            symbols.add(char)

    # replace the symbols with one ',' symbol to make it easier
    schema_replaced = schematic
    for delim in symbols:  # could be faster with RegEx
        schema_replaced = schema_replaced.replace(delim, ',')
    # extract all numbers from schematic
    schema_split = schema_replaced.replace(INERT_SYMBOL, ',').replace('\n', ',').split(',')
    numbers_in_schema = [num for num in schema_split if num != '']
    matrix = Matrix([INERT_SYMBOL + line + INERT_SYMBOL for line in schema_replaced.split('\n')])

    return matrix.total(numbers_in_schema)


if __name__ == '__main__':
    print(main())
