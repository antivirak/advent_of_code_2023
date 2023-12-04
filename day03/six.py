"""
The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
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
