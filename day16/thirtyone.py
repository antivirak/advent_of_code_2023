"""
23731
"""

from typing import Dict, Self

import pandas as pd

# TODO mode enum


class BeamPath:
    """DFS ray tracing, recursive"""
    def __init__(self, layout: pd.DataFrame) -> None:
        self.layout = layout
        # self.energized_layout = layout.copy()
        self.visited: Dict[tuple, tuple] = {}  # {(row_idx, col_idx): (mode, count_idx))} map to keep track of visited cells

    def __call__(self, offset) -> Self:
        """Calculate beam path from top left corner"""
        self.horizontal(offset, 0, 'right', first_call=True)
        return self

    def horizontal(self, y_idx: int, offset: int, mode: str, first_call=False) -> None:
        """Horizontal ray tracing"""
        row = self.layout.iloc[y_idx, offset:] if mode == 'right' else reversed(self.layout.iloc[y_idx, :offset + 1])
        counts = range(offset, len(row) + offset) if mode == 'right' else reversed(range(offset + 1))
        for count_idx, (count, symbol) in enumerate(zip(counts, row)):
            if self.visited.get((y_idx, count)) == (mode, count_idx):
                return
            self.visited[(y_idx, count)] = (mode, count_idx)
            # self.energized_layout.iat[y_idx, count] = '#'
            if count_idx == 0 and not first_call:
                continue
            if symbol in ('.', '-'):
                continue
            if (symbol == '\\' and mode == 'right') or (symbol == '/' and mode == 'left'):
                self.vertical(count, y_idx, 'down')
                return
            if (symbol == '\\' and mode == 'left') or (symbol == '/' and mode == 'right'):
                self.vertical(count, y_idx, 'up')
                return
            if symbol == '|':
                self.vertical(count, y_idx, 'down')
                self.vertical(count, y_idx, 'up')
                return
            raise ValueError('Unknown symbol')

    # TODO I know the code for vertical and horizontal is almost identical
    # (transposition, I've made similar in previous days), but I'm too lazy to refactor it
    def vertical(self, x_idx: int, offset: int, mode: str, first_call=False) -> None:
        """Vertical ray tracing"""
        row = self.layout.iloc[offset:, x_idx] if mode == 'down' else reversed(self.layout.iloc[:offset + 1, x_idx])
        counts = range(offset, len(row) + offset) if mode == 'down' else reversed(range(offset + 1))
        for count_idx, (count, symbol) in enumerate(zip(counts, row)):
            if self.visited.get((count, x_idx)) == (mode, count_idx):
                return
            self.visited[(count, x_idx)] = (mode, count_idx)
            # self.energized_layout.iat[count, x_idx] = '#'
            if count_idx == 0 and not first_call:
                continue
            if symbol in ('.', '|'):
                continue
            if (symbol == '\\' and mode == 'down') or (symbol == '/' and mode == 'up'):
                self.horizontal(count, x_idx, 'right')
                return
            if (symbol == '\\' and mode == 'up') or (symbol == '/' and mode == 'down'):
                self.horizontal(count, x_idx, 'left')
                return
            if symbol == '-':
                self.horizontal(count, x_idx, 'left')
                self.horizontal(count, x_idx, 'right')
                return
            raise ValueError('Unknown symbol')


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        layout = pd.DataFrame(list(iter(row)) for row in f_in.read().splitlines())

    beam = BeamPath(layout)
    return len(beam(0).visited)


if __name__ == '__main__':
    print(main())
