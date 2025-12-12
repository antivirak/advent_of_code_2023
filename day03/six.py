"""
39109
"""

from five import INERT_SYMBOL, NUMBERS, Matrix, indices

GEAR = '*'


class MatrixGears(Matrix):
    """Perform computations on schematic"""
    def _gears(self, idx1: int, idx2: int) -> bool:
        """Check gear neighborhood. Return true if exactly 2 numbers are in it."""
        num_variations = []
        for variation in self.variations:
            try:
                item = self.matrix[idx1 + variation[0]][idx2 + variation[1]]
            except IndexError:
                continue
            if item in NUMBERS:
                num_variations.append((variation[0], variation[1]))

        count = len(num_variations)
        if count > 1:
            # get rid of duplicates
            # 111
            # .*.
            # .11
            remove_duplicates(num_variations, -1)  # one line up
            remove_duplicates(num_variations, 1)  # one line down

        count = len(num_variations)
        if count != 2:
            return 0

        ratio = 1
        for variation in num_variations:
            # find starting index of the number in the row
            start = idx2 + variation[1]
            ax_x = idx1 + variation[0]
            while self.matrix[ax_x][start - 1] in NUMBERS:
                start -= 1
            ratio = ratio * int(self.matrix[ax_x][start:].replace(GEAR, '.').split('.')[0])
        return ratio

    def sum_gear_ratios(self) -> int:
        """Calculate sum of 'part numbers'"""
        total = 0
        for count, line in enumerate(self.matrix):
            indexes = indices(line, GEAR)
            for idx in indexes:
                total += self._gears(count, idx)
        return total


def remove_duplicates(num_variations: list, idx2: int) -> None:
    """Remove indexes of digits that all make up one number"""
    # this is kinda ugly
    if (idx2, -1) in num_variations and (idx2, 0) in num_variations:
        # 11.
        # .*. case
        if (idx2, 1) in num_variations:
            # 111
            # .*. case
            num_variations.remove((idx2, 1))
        num_variations.remove((idx2, 0))
    elif (idx2, 1) in num_variations and (idx2, 0) in num_variations:
        # .11
        # .*. case
        if (idx2, -1) in num_variations:
            num_variations.remove((idx2, 0))
        num_variations.remove((idx2, 1))


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        schematic = f_in.read()

    symbols = set()
    for char in schematic:
        if char not in (*NUMBERS, INERT_SYMBOL, GEAR, '\n'):
            symbols.add(char)

    schema_replaced = schematic
    for delim in symbols:
        schema_replaced = schema_replaced.replace(delim, INERT_SYMBOL)
    schema_split = schema_replaced.split('\n')
    matrix = MatrixGears(schema_split)

    return matrix.sum_gear_ratios()


if __name__ == '__main__':
    print(main())
